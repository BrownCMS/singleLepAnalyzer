#!/usr/bin/python

import os,sys,time,math,pickle
from ROOT import *
from weights import *

gROOT.SetBatch(1)
start_time = time.time()

# INPUT SETTINGS
templateDir=os.getcwd()+'/kinematics_JetSFCalc0bMoreBins_Pileup69mb'
lumiInTemplates='12p892'
plotLabel = '_Apply2x'

#isEMlist=['E','M','All']
isEMlist=['All']

# SIGNAL SETTINGS
sig='ttm1000' # choose the 1st signal to plot
sigleg='TT(1.0 TeV)'
scaleSignals = True
scaleFact1 = 800
if 'Final' in templateDir or 'CR' in templateDir: scaleFact1 = 80
scaleFact1Str = ' x'+str(scaleFact1)
if not scaleSignals: scaleFact1Str = ''

# SYSTEMATICS SETTINGS
doAllSys = True
doQ2sys = True
doJetRwt = False
if not doAllSys: doQ2sys = False
systematicList = ['pileup','jec','jer','btag','tau21','muRFcorrdNew','mistag','pdfNew','trigeff']
if doJetRwt: systematicList.append('jsf')

# NORMALIZATION UNCERTAINTIES
lumiSys = 0.062 # lumi uncertainty
trigSys = 0.03 # trigger uncertainty
lepIdSys = 0.01 # lepton id uncertainty
lepIsoSys = 0.011 # lepton isolation uncertainty
corrdSys = math.sqrt(lumiSys**2+trigSys**2+lepIdSys**2+lepIsoSys**2)

def getNormUnc(hist,ibin,modelingUnc):
	contentsquared = hist.GetBinContent(ibin)**2
	error = corrdSys*corrdSys*contentsquared  #correlated uncertainties
	error += modelingUnc*modelingUnc*contentsquared #background modeling uncertainty from CRs
	return error	
		
CRuncert = {
	'topE':0.0,#0.085,#
	'topM':0.0,#0.222,#
	'topAll':0.0,#0.163,#
	'ewkE':0.0,#0.064,#
	'ewkM':0.0,#0.126,#
	'ewkAll':0.0,#0.100,#
	}

# PLOT SETTINGS
lumi=12.9
isRebinned=''#post fix for file names if the name changed b/c of rebinning or some other process
doNormByBinWidth = False # not tested, may not work out of the box
doOneBand = False
blind = False
yLog = True
doRealPull = False
fit = True
if not doAllSys: doOneBand = True # Don't change this!
if doRealPull: doOneBand=False

do2ColLegend = False

totBkgTemp1 = {}
totBkgTemp2 = {}
totBkgTemp3 = {}

plotList = [#distribution name as defined in "makeTemplates.py"
	#'HT'    ,
	#'ST'    ,
	#'MET'   ,
	#'NJets' ,
	'JetPtBins' ,
	#'Jet1PtBins',
	#'Jet2PtBins',
	#'Jet3PtBins',
	#'Jet4PtBins',
	#'JetPtBinsAK8',

	]

def formatUpperHist(histogram):
	histogram.GetXaxis().SetLabelSize(0)
	if blind == True:
		histogram.GetXaxis().SetLabelSize(0.045)
		histogram.GetXaxis().SetTitleSize(0.055)
		histogram.GetYaxis().SetLabelSize(0.045)
		histogram.GetYaxis().SetTitleSize(0.055)
		histogram.GetYaxis().SetTitleOffset(1.15)
		histogram.GetXaxis().SetNdivisions(506)
	else:
		histogram.GetYaxis().SetLabelSize(0.058)
		histogram.GetYaxis().SetTitleSize(0.08)
		histogram.GetYaxis().SetTitleOffset(.79)
		histogram.GetXaxis().SetRangeUser(0,2500)

	if 'JetPt' in histogram.GetName() or 'JetEta' in histogram.GetName() or 'JetPhi' in histogram.GetName() or 'Pruned' in histogram.GetName() or 'Tau' in histogram.GetName(): histogram.GetYaxis().SetTitle("Jets")
	histogram.GetYaxis().CenterTitle()
	histogram.SetMinimum(0.001)
	if not yLog: 
		histogram.SetMinimum(0.25)
	if yLog:
		uPad.SetLogy()
		histogram.SetMinimum(0.1)
		if not doNormByBinWidth: histogram.SetMaximum(100*histogram.GetMaximum())
		
def formatLowerHist(histogram):
	histogram.GetXaxis().SetLabelSize(.12)
	histogram.GetXaxis().SetTitleSize(0.15)
	histogram.GetXaxis().SetTitleOffset(0.95)
	histogram.GetXaxis().SetNdivisions(506)
	histogram.GetXaxis().SetRangeUser(0,2500)

	histogram.GetYaxis().SetLabelSize(0.10)
	histogram.GetYaxis().SetTitleSize(0.14)
	histogram.GetYaxis().SetTitleOffset(.41)
	histogram.GetYaxis().SetTitle('Data/Bkg')
	histogram.GetYaxis().SetNdivisions(5)
	if doRealPull: histogram.GetYaxis().SetRangeUser(min(-2.99,0.8*histogram.GetBinContent(histogram.GetMaximumBin())),max(2.99,1.2*histogram.GetBinContent(histogram.GetMaximumBin())))
	else: histogram.GetYaxis().SetRangeUser(0,2.99)
	histogram.GetYaxis().CenterTitle()

def normByBinWidth(result):
	result.SetBinContent(0,0)
	result.SetBinContent(result.GetNbinsX()+1,0)
	result.SetBinError(0,0)
	result.SetBinError(result.GetNbinsX()+1,0)
	
	for bin in range(1,result.GetNbinsX()+1):
		width=result.GetBinWidth(bin)
		content=result.GetBinContent(bin)
		error=result.GetBinError(bin)
		
		result.SetBinContent(bin, content/width)
		result.SetBinError(bin, error/width)

################################################################
#################### RUN PLOT LOOP #############################
################################################################

for discriminant in plotList:
	
	fileTemp='kinematics_'+discriminant+'_'+lumiInTemplates+'fb'+isRebinned+'.root'
	print templateDir+'/'+fileTemp
	if not os.path.exists(templateDir+'/'+fileTemp): 
		print 'not found, skipping'
		continue
	RFile = TFile(templateDir+'/'+fileTemp)

	systHists={}
	for isEM in isEMlist:
		histPrefix=discriminant+'_'+lumiInTemplates+'fb_'+isEM
		
		hTOP = RFile.Get(histPrefix+'__top').Clone()
		try: hEWK = RFile.Get(histPrefix+'__ewk').Clone()
		except: 
			print "There is no EWK!!!!!!!!"
			print "Skipping EWK....."
			pass
		try: hQCD = RFile.Get(histPrefix+'__qcd').Clone()
		except: 
			print "There is no QCD!!!!!!!!"
			print "Skipping QCD....."
			pass
		
		print discriminant,isEM, "TOP", hTOP.Integral()
		print discriminant,isEM, "EWK", hEWK.Integral()
		try: print discriminant,isEM, "QCD", hQCD.Integral()
		except: pass
		
		hData = RFile.Get(histPrefix+'__DATA').Clone()
		hsig1 = RFile.Get(histPrefix+'__'+sig+'bwbw').Clone()
		hsig2 = RFile.Get(histPrefix+'__'+sig+'tztz').Clone()
		hsig3 = RFile.Get(histPrefix+'__'+sig+'thth').Clone()

		hsig = RFile.Get(histPrefix+'__'+sig+'bwbw').Clone(histPrefix+'__'+sig+'nominal')
		decays = ['tztz','thth','tzbw','thbw','tzth']
		for decay in decays:
			htemp = RFile.Get(histPrefix+'__'+sig+decay).Clone()
			hsig.Add(htemp)

		# original scale = lumi * xsec * BR(50/25/25) / N(33/33/33)
		hsig1.Scale(1.0/BR['TTBWBW'])
		hsig2.Scale(1.0/BR['TTTZTZ'])
		hsig3.Scale(1.0/BR['TTTHTH'])

		if doNormByBinWidth:
			normByBinWidth(hTOP)
			normByBinWidth(hEWK)
			normByBinWidth(hQCD)
			normByBinWidth(hsig1)
			normByBinWidth(hsig2)
			normByBinWidth(hData)
		
		if doAllSys:
			for sys in systematicList:
				for ud in ['minus','plus']:
					systHists['top'+sys+ud] = RFile.Get(histPrefix+'__top__'+sys+'__'+ud).Clone()
					try: systHists['ewk'+sys+ud] = RFile.Get(histPrefix+'__ewk__'+sys+'__'+ud).Clone()
					except: pass
					try: systHists['qcd'+sys+ud] = RFile.Get(histPrefix+'__qcd__'+sys+'__'+ud).Clone()
					except: pass
		if doQ2sys:
			for ud in ['minus','plus']:
				systHists['topq2'+ud] = RFile.Get(histPrefix+'__top__q2__'+ud).Clone()
				systHists['q2'+ud] = systHists['topq2'+ud].Clone()
				systHists['ewkq2'+ud] = RFile.Get(histPrefix+'__ewk').Clone()
				systHists['q2'+ud].Add(systHists['ewkq2'+ud])
				try:
					systHists['qcdq2'+ud] = RFile.Get(histPrefix+'__qcd').Clone()
					systHists['q2'+ud].Add(systHists['qcdq2'+ud])
				except: pass

		hTOPstatOnly = hTOP.Clone(hTOP.GetName()+'statOnly')
		try: hEWKstatOnly= hEWK.Clone(hEWK.GetName()+'statOnly')
		except: pass
		try: hQCDstatOnly = hQCD.Clone(hQCD.GetName()+'statOnly')
		except: pass

		bkgHT = hTOP.Clone()
		try: bkgHT.Add(hEWK)
		except: pass
		try: bkgHT.Add(hQCD)
		except: pass

		totBkgTemp1[isEM] = TGraphAsymmErrors(bkgHT.Clone(bkgHT.GetName()+'shapeOnly'))
		totBkgTemp2[isEM] = TGraphAsymmErrors(bkgHT.Clone(bkgHT.GetName()+'shapePlusNorm'))
		totBkgTemp3[isEM] = TGraphAsymmErrors(bkgHT.Clone(bkgHT.GetName()+'All'))
			
		for ibin in range(1,hTOP.GetNbinsX()+1):
			errorUp = 0.
			errorDn = 0.
			errorSym = 0.

			errorStatOnly = bkgHT.GetBinError(ibin)**2
			errorCheck = hTOP.GetBinError(ibin)**2 + hEWK.GetBinError(ibin)**2
			try: errorCheck += hQCD.GetBinError(ibin)**2
			except: pass

			errorStatCheck = hTOPstatOnly.GetBinError(ibin)**2 + hEWKstatOnly.GetBinError(ibin)**2
			try: errorStatCheck += hQCDstatOnly.GetBinError(ibin)**2
			except: pass

			errorNorm = getNormUnc(hTOPstatOnly,ibin,CRuncert['top'+isEM])
			try: errorNorm += getNormUnc(hEWKstatOnly,ibin,CRuncert['ewk'+isEM])
			except: pass
			try: errorNorm += getNormUnc(hQCDstatOnly,ibin,0.0)
			except: pass

			for sys in systematicList:
				if doAllSys:	
					errorSym += (0.5*abs(systHists['top'+sys+'plus'].GetBinContent(ibin)-systHists['top'+sys+'minus'].GetBinContent(ibin)))**2				
					errorPlus = systHists['top'+sys+'plus'].GetBinContent(ibin)-hTOP.GetBinContent(ibin)
					errorMinus = hTOP.GetBinContent(ibin)-systHists['top'+sys+'minus'].GetBinContent(ibin)
					if errorPlus > 0: errorUp += errorPlus**2
					else: errorDn += errorPlus**2
					if errorMinus > 0: errorDn += errorMinus**2
					else: errorUp += errorMinus**2
					if sys!='toppt':
						try:
							errorSym += (0.5*abs(systHists['ewk'+sys+'plus'].GetBinContent(ibin)-systHists['ewk'+sys+'minus'].GetBinContent(ibin)))**2				
							errorPlus = systHists['ewk'+sys+'plus'].GetBinContent(ibin)-hEWK.GetBinContent(ibin)
							errorMinus = hEWK.GetBinContent(ibin)-systHists['ewk'+sys+'minus'].GetBinContent(ibin)
							if errorPlus > 0: errorUp += errorPlus**2
							else: errorDn += errorPlus**2
							if errorMinus > 0: errorDn += errorMinus**2
							else: errorUp += errorMinus**2
						except: pass
						try:
							errorSym += (0.5*abs(systHists['qcd'+sys+'plus'].GetBinContent(ibin)-systHists['qcd'+sys+'minus'].GetBinContent(ibin)))**2				
							errorPlus = systHists['qcd'+sys+'plus'].GetBinContent(ibin)-hQCD.GetBinContent(ibin)
							errorMinus = hQCD.GetBinContent(ibin)-systHists['qcd'+sys+'minus'].GetBinContent(ibin)
							if errorPlus > 0: errorUp += errorPlus**2
							else: errorDn += errorPlus**2
							if errorMinus > 0: errorDn += errorMinus**2
							else: errorUp += errorMinus**2
						except: pass													
			if doQ2sys: 
				errorSym += (0.5*abs(systHists['topq2plus'].GetBinContent(ibin)-systHists['topq2minus'].GetBinContent(ibin)))**2				
				errorPlus = systHists['topq2plus'].GetBinContent(ibin)-hTOP.GetBinContent(ibin)
				errorMinus = hTOP.GetBinContent(ibin)-systHists['topq2minus'].GetBinContent(ibin)
				if errorPlus > 0: errorUp += errorPlus**2
				else: errorDn += errorPlus**2
				if errorMinus > 0: errorDn += errorMinus**2
				else: errorUp += errorMinus**2
				
			totBkgTemp1[isEM].SetPointEYhigh(ibin-1,math.sqrt(errorUp))
			totBkgTemp1[isEM].SetPointEYlow(ibin-1,math.sqrt(errorDn))
			totBkgTemp2[isEM].SetPointEYhigh(ibin-1,math.sqrt(errorUp+errorNorm))
			totBkgTemp2[isEM].SetPointEYlow(ibin-1,math.sqrt(errorDn+errorNorm))
			totBkgTemp3[isEM].SetPointEYhigh(ibin-1,math.sqrt(errorUp+errorNorm+errorStatOnly))
			totBkgTemp3[isEM].SetPointEYlow(ibin-1,math.sqrt(errorDn+errorNorm+errorStatOnly))
			
		bkgHTgerr = totBkgTemp3[isEM].Clone()

		hsig1.Scale(scaleFact1)
		hsig2.Scale(scaleFact1)
		hsig3.Scale(scaleFact1)
		hsig.Scale(scaleFact1)

		stackbkgHT = THStack("stackbkgHT","")
		try: stackbkgHT.Add(hTOP)
		except: pass
		try: stackbkgHT.Add(hEWK)
		except: pass
		try: 
			if hQCD.Integral()/bkgHT.Integral()>.005: stackbkgHT.Add(hQCD) #don't plot QCD if it is less than 0.5%
		except: pass

		# COLORS AND STYLES
		hTOP.SetLineColor(kAzure+8)
		hTOP.SetFillColor(kAzure+8)
		hTOP.SetLineWidth(2)
		try: 
			hEWK.SetLineColor(kMagenta-2)
			hEWK.SetFillColor(kMagenta-2)
			hEWK.SetLineWidth(2)
		except: pass
		try:
			hQCD.SetLineColor(kOrange+5)
			hQCD.SetFillColor(kOrange+5)
			hQCD.SetLineWidth(2)
		except: pass

		hsig.SetLineColor(kBlack)
		hsig.SetLineWidth(3)
		hsig1.SetLineColor(kBlue+2)
		hsig1.SetLineStyle(2)
		hsig1.SetLineWidth(3)
		hsig2.SetLineColor(kGreen+3)
		hsig2.SetLineStyle(5)
		hsig2.SetLineWidth(3)
		hsig3.SetLineColor(kRed+2)
		hsig3.SetLineStyle(7)
		hsig3.SetLineWidth(3)

		hData.SetMarkerStyle(20)
		hData.SetMarkerSize(1.2)
		hData.SetLineWidth(2)

		bkgHTgerr.SetFillStyle(3004)
		bkgHTgerr.SetFillColor(kBlack)

		# CANVAS AND PADS
		gStyle.SetOptStat(0)
		c1 = TCanvas("c1","c1",1200,1000)
		gStyle.SetErrorX(0.5)
		yDiv=0.35
		if blind == True: yDiv=0.0
		uMargin = 0
		if blind == True: uMargin = 0.12
		rMargin=.04
		uPad=TPad("uPad","",0,yDiv,1,1) #for actual plots
		uPad.SetTopMargin(0.10)
		uPad.SetBottomMargin(uMargin)
		uPad.SetRightMargin(rMargin)
		uPad.SetLeftMargin(.12)
		uPad.Draw()
		if blind == False:
			lPad=TPad("lPad","",0,0,1,yDiv) #for sigma runner
			lPad.SetTopMargin(0)
			lPad.SetBottomMargin(.4)
			lPad.SetRightMargin(rMargin)
			lPad.SetLeftMargin(.12)
			lPad.SetGridy()
			lPad.Draw()

		if not doNormByBinWidth: hData.SetMaximum(1.2*max(hData.GetMaximum(),bkgHT.GetMaximum()))

		hData.SetMinimum(0.015)
		hData.SetTitle("")
		if doNormByBinWidth: hData.GetYaxis().SetTitle("Events / 1 GeV")
		else: hData.GetYaxis().SetTitle("Events")
		formatUpperHist(hData)
		uPad.cd()
		hData.SetTitle("")

		# DRAW
		if not blind: hData.Draw("E1 X0")
		if blind: 
			hsig1.SetMinimum(0.015)
			if doNormByBinWidth: hsig1.GetYaxis().SetTitle("Events / 1 GeV")
			else: hsig1.GetYaxis().SetTitle("Events")
			formatUpperHist(hsig1)
			hsig1.SetMaximum(hData.GetMaximum())
			hsig1.Draw("HIST")

		stackbkgHT.Draw("SAME HIST")

		#hsig.Draw("SAME HIST")
		#hsig1.Draw("SAME HIST")
		#hsig2.Draw("SAME HIST")
		#hsig3.Draw("SAME HIST")

		if not blind: hData.Draw("SAME E1 X0") #redraw data so its not hidden
		uPad.RedrawAxis()
		bkgHTgerr.Draw("SAME E2")

		# LEGEND
		leg = {}
		if do2ColLegend: 
			leg = TLegend(0.25,0.50,0.95,0.88)
			leg.SetNColumns(2)
		else:
			if 'Tau21' in discriminant or 'Tau32' in discriminant or 'deltaRjet1' in discriminant:
				leg = TLegend(0.15,0.53,0.45,0.90)
			elif 'NPV' in discriminant or 'Eta' in discriminant or 'deltaRjet2' in discriminant:
				leg = TLegend(0.72,0.43,0.95,0.90)
			elif blind: leg = TLegend(0.43,0.35,0.97,0.88)
			#else: leg = TLegend(0.43,0.22,0.97,0.88)
			else: leg = TLegend(0.43,0.43,0.97,0.88)
		leg.SetShadowColor(0)
		leg.SetFillColor(0)
		leg.SetFillStyle(0)
		leg.SetLineColor(0)
		leg.SetLineStyle(0)
		leg.SetBorderSize(0) 
		leg.SetTextFont(42)

		if do2ColLegend:
			leg.AddEntry(hsig,sigleg+'nominal'+scaleFact1Str,"l")
			if not blind: leg.AddEntry(hData,"DATA")			
			leg.AddEntry(hsig1,sigleg+'bWbW'+scaleFact1Str,"l")
			try: 
				if hQCD.Integral()/bkgHT.Integral()>.005: leg.AddEntry(hQCD,"QCD","f") #don't plot QCD if it is less than 0.5%
			except: pass
			leg.AddEntry(hsig2,sigleg+'tZtZ'+scaleFact1Str,"l")
			try: leg.AddEntry(hEWK,"EWK","f")
			except: pass
			leg.AddEntry(hsig3,sigleg+'tHtH'+scaleFact1Str,"l")
			try: leg.AddEntry(hTOP,"TOP","f")
			except: pass
			leg.AddEntry(hTOP,"","")
			leg.AddEntry(bkgHTgerr,"Bkg uncert.","f")
		else:
			if not blind: leg.AddEntry(hData,"DATA")

			#leg.AddEntry(hsig,sigleg+' nominal BRs'+scaleFact1Str,"l")
			#leg.AddEntry(hsig1,sigleg+' #rightarrow bWbW'+scaleFact1Str,"l")
			#leg.AddEntry(hsig2,sigleg+' #rightarrow tZtZ'+scaleFact1Str,"l")
			#leg.AddEntry(hsig3,sigleg+' #rightarrow tHtH'+scaleFact1Str,"l")

			try: 
				if hQCD.Integral()/bkgHT.Integral()>.005: leg.AddEntry(hQCD,"QCD","f") #don't plot QCD if it is less than 0.5%
			except: pass
			try: leg.AddEntry(hEWK,"EWK","f")
			except: pass
			try: leg.AddEntry(hTOP,"TOP","f")
			except: pass
			leg.AddEntry(bkgHTgerr,"Bkg uncert.","f")

		leg.Draw("same")

		# TITLES
		prelimTex=TLatex()
		prelimTex.SetNDC()
		prelimTex.SetTextAlign(31) # align right
		prelimTex.SetTextFont(42)
		prelimTex.SetTextSize(0.07)
		if blind: prelimTex.SetTextSize(0.05)
		prelimTex.SetLineWidth(2)
		prelimTex.DrawLatex(0.95,0.92,str(lumi)+" fb^{-1} (13 TeV)")

		prelimTex2=TLatex()
		prelimTex2.SetNDC()
		prelimTex2.SetTextFont(61)
		prelimTex2.SetLineWidth(2)
		prelimTex2.SetTextSize(0.10)
		if blind: prelimTex2.SetTextSize(0.08)
		prelimTex2.DrawLatex(0.12,0.92,"CMS")

		prelimTex3=TLatex()
		prelimTex3.SetNDC()
		prelimTex3.SetTextAlign(13)
		prelimTex3.SetTextFont(52)
		prelimTex3.SetTextSize(0.075)
		if blind: prelimTex3.SetTextSize(0.055)
		prelimTex3.SetLineWidth(2)
		if not blind: prelimTex3.DrawLatex(0.24,0.975,"Preliminary")
		if blind: prelimTex3.DrawLatex(0.26,0.96,"Preliminary")

		# RATIO OR PULL PANEL
		if blind == False and not doRealPull:
			lPad.cd()
			pull=hData.Clone("pull")
			pull.Divide(hData, bkgHT)

			for binNo in range(0,hData.GetNbinsX()+2):
				if bkgHT.GetBinContent(binNo)!=0:
					pull.SetBinError(binNo,hData.GetBinError(binNo)/bkgHT.GetBinContent(binNo))
			pull.SetMaximum(3)
			pull.SetMinimum(0)
			pull.SetFillColor(1)
			pull.SetLineColor(1)
			formatLowerHist(pull)
			pull.Draw("E1")

			if fit and discriminant == 'JetPtBins':

				flat = TF1("flat","pol0",700,2500);
				line = TF1("line","pol1",150,800);
				line.SetLineWidth(2);

#				pull.Fit("flat","R")
				'''
				fitresult = pull.Fit("line","RS")
				cov = fitresult.GetCovarianceMatrix()
				p0p0cov = cov(0,0)
				p0p1cov = cov(0,1)
				p1p1cov = cov(1,1)
				print 'covariance p0-p0 =',p0p0cov
				print 'covariance p0-p1 =',p0p1cov
				print 'covariance p1-p1 =',p1p1cov
				fitresult = pull.Fit("flat","R+S")
				cov = fitresult.GetCovarianceMatrix()
				p0p0cov = cov(0,0)
				p0p1cov = cov(0,1)
				p1p1cov = cov(1,1)
				print 'covariance p0-p0 =',p0p0cov
				print 'covariance p0-p1 =',p0p1cov
				print 'covariance p1-p1 =',p1p1cov
				'''
#				jsf0b = TF1("jsf0b","1.24507 - 0.000664768*x",350,1030)
#				jsf20b = TF1("jsf20b","0.568135",1015,1500);
#				jsfup0b = TF1("jsfup0b","max(0.568135 + 0.052292,1.24507 - 0.000664768*x + sqrt(0.000506216376592 + 3.1532423475e-09*x*x - 2*x*1.17981363543e-06))",350,1500)
#				jsfdn0b = TF1("jsfdn0b","max(0.568135 - 0.052292,1.24507 - 0.000664768*x - sqrt(0.000506216376592 + 3.1532423475e-09*x*x - 2*x*1.17981363543e-06))",350,1500)
#				jsfup0b = TF1("jsfup0b","max(max(0.747382 + 0.164524,1.09383 - 0.000477777*x + sqrt(0.00314541714554 + 2.18390370364e-08*x*x - 2*x*7.85447860996e-06)),max(0.568135 + 0.052292,1.24507 - 0.000664768*x + sqrt(0.000506216376592 + 3.1532423475e-09*x*x - 2*x*1.17981363543e-06)))",350,1500)
#				jsfdn0b = TF1("jsfdn0b","min(max(0.747382 - 0.164524,1.09383 - 0.000477777*x - sqrt(0.00314541714554 + 2.18390370364e-08*x*x - 2*x*7.85447860996e-06)),max(0.568135 - 0.052292,1.24507 - 0.000664768*x - sqrt(0.000506216376592 + 3.1532423475e-09*x*x - 2*x*1.17981363543e-06)))",350,1500)
#				jsfup20b =TF1("jsfup20b","0.568135 + 0.052292",1020,1500);
#				jsfdn20b =TF1("jsfdn20b","0.568135 - 0.052292",1020,1500);

				jsf0b = TF1("jsf0b","1.09502 - 0.00045995*x",150,820)
				jsf20b = TF1("jsf20b","0.726255",800,2500);
				#jsfup0b = TF1("jsfup0b","max(max(0.747382 + 0.164524,1.09383 - 0.000477777*x + sqrt(0.00314541714554 + 2.18390370364e-08*x*x - 2*x*7.85447860996e-06)),max(0.726255 + 0.0190384,1.09502 - 0.00045995*x + sqrt(2.41563501145e-05 + 3.64859173927e-10*x*x - 2*x*8.66909413702e-08)))",150,2500)
				#jsfdn0b = TF1("jsfdn0b","min(max(0.747382 - 0.164524,1.09383 - 0.000477777*x - sqrt(0.00314541714554 + 2.18390370364e-08*x*x - 2*x*7.85447860996e-06)),max(0.726255 - 0.0190384,1.09502 - 0.00045995*x - sqrt(2.41563501145e-05 + 3.64859173927e-10*x*x - 2*x*8.66909413702e-08)))",150,2500)
				jsfup0b = TF1("jsfup0b","1",150,2500)
				jsfdn0b = TF1("jsfdn0b","max((0.726255 - 0.0190384)*(0.726255 - 0.0190384),(1.09502 - 0.00045995*x)*(1.09502 - 0.00045995*x))",150,2500)
#				jsfup0b = TF1("jsfup0b","max(0.726255 + 0.0190384,1.09502 - 0.00045995*x + sqrt(2.41563501145e-05 + 3.64859173927e-10*x*x - 2*x*8.66909413702e-08))",150,2500)
#				jsfdn0b = TF1("jsfdn0b","max(0.726255 - 0.0190384,1.09502 - 0.00045995*x - sqrt(2.41563501145e-05 + 3.64859173927e-10*x*x - 2*x*8.66909413702e-08))",150,2500)
#				jsfup20b =TF1("jsfup20b","0.726255 + 0.0190384",1020,1500);
#				jsfdn20b =TF1("jsfdn20b","0.726255 - 0.0190384",1020,1500);

				jsf0b.SetLineColor(kRed)
				jsf0b.SetLineWidth(2)
				jsfup0b.SetLineColor(kBlue)
				jsfdn0b.SetLineColor(kBlue)
				jsfup0b.SetLineWidth(2)
				jsfdn0b.SetLineWidth(2)
				#jsf20b.SetLineColor(kRed)
				#jsf20b.SetLineWidth(2)
				#jsfup20b.SetLineColor(kBlue)
				#jsfdn20b.SetLineColor(kBlue)
				#jsfup20b.SetLineWidth(2)
				#jsfdn20b.SetLineWidth(2)

				pull.Draw("E1")

		
			BkgOverBkg = pull.Clone("bkgOverbkg")
			BkgOverBkg.Divide(bkgHT, bkgHT)
			pullUncBandTot=TGraphAsymmErrors(BkgOverBkg.Clone("pulluncTot"))
			for binNo in range(0,hData.GetNbinsX()+2):
				if bkgHT.GetBinContent(binNo)!=0:
					pullUncBandTot.SetPointEYhigh(binNo-1,totBkgTemp3[isEM].GetErrorYhigh(binNo-1)/bkgHT.GetBinContent(binNo))
					pullUncBandTot.SetPointEYlow(binNo-1,totBkgTemp3[isEM].GetErrorYlow(binNo-1)/bkgHT.GetBinContent(binNo))			
			if not doOneBand: pullUncBandTot.SetFillStyle(3001)
			else: pullUncBandTot.SetFillStyle(3344)
			pullUncBandTot.SetFillColor(1)
			pullUncBandTot.SetLineColor(1)
			pullUncBandTot.SetMarkerSize(0)
			gStyle.SetHatchesLineWidth(1)
			pullUncBandTot.Draw("SAME E2")
				
			pullUncBandNorm=TGraphAsymmErrors(BkgOverBkg.Clone("pulluncNorm"))
			for binNo in range(0,hData.GetNbinsX()+2):
				if bkgHT.GetBinContent(binNo)!=0:
					pullUncBandNorm.SetPointEYhigh(binNo-1,totBkgTemp2[isEM].GetErrorYhigh(binNo-1)/bkgHT.GetBinContent(binNo))
					pullUncBandNorm.SetPointEYlow(binNo-1,totBkgTemp2[isEM].GetErrorYlow(binNo-1)/bkgHT.GetBinContent(binNo))			
			pullUncBandNorm.SetFillStyle(3001)
			pullUncBandNorm.SetFillColor(2)
			pullUncBandNorm.SetLineColor(2)
			pullUncBandNorm.SetMarkerSize(0)
			gStyle.SetHatchesLineWidth(1)
			if not doOneBand: pullUncBandNorm.Draw("SAME E2")
			
			pullUncBandStat=TGraphAsymmErrors(BkgOverBkg.Clone("pulluncStat"))
			for binNo in range(0,hData.GetNbinsX()+2):
				if bkgHT.GetBinContent(binNo)!=0:
					pullUncBandStat.SetPointEYhigh(binNo-1,totBkgTemp1[isEM].GetErrorYhigh(binNo-1)/bkgHT.GetBinContent(binNo))
					pullUncBandStat.SetPointEYlow(binNo-1,totBkgTemp1[isEM].GetErrorYlow(binNo-1)/bkgHT.GetBinContent(binNo))			
			pullUncBandStat.SetFillStyle(3001)
			pullUncBandStat.SetFillColor(3)
			pullUncBandStat.SetLineColor(3)
			pullUncBandStat.SetMarkerSize(0)
			gStyle.SetHatchesLineWidth(1)
			if not doOneBand: pullUncBandStat.Draw("SAME E2")
		
			pullLegend=TLegend(0.14,0.87,0.85,0.96)
			SetOwnership( pullLegend, 0 )   # 0 = release (not keep), 1 = keep
			pullLegend.SetShadowColor(0)
			pullLegend.SetNColumns(3)
			pullLegend.SetFillColor(0)
			pullLegend.SetFillStyle(0)
			pullLegend.SetLineColor(0)
			pullLegend.SetLineStyle(0)
			pullLegend.SetBorderSize(0)
			pullLegend.SetTextFont(42)
			if not doOneBand: pullLegend.AddEntry(pullUncBandStat , "Bkg shape syst." , "f")
			if not doOneBand: pullLegend.AddEntry(pullUncBandNorm , "Bkg shape #oplus norm. syst." , "f")
			if not doOneBand: pullLegend.AddEntry(pullUncBandTot , "Bkg stat. #oplus all syst." , "f")
			else: 
				pullLegend.AddEntry(pullUncBandTot , "Bkg stat. #oplus syst." , "f")
				if fit and discriminant == 'JetPtBins':
					pullLegend.AddEntry(jsf0b, "Fit","l")
					pullLegend.AddEntry(jsfup0b, "#pm 1#sigma","l")

			pullLegend.Draw("SAME")
			pull.Draw("SAME")
			jsf0b.Draw("same")
			jsfup0b.Draw("same")
			jsfdn0b.Draw("same")
			jsf20b.Draw("same")
			lPad.RedrawAxis()

		if blind == False and doRealPull:
			lPad.cd()
			pull=hData.Clone("pull")
			for binNo in range(0,hData.GetNbinsX()+2):
				if hData.GetBinContent(binNo)!=0:
					MCerror = 0.5*(totBkgTemp3[isEM].GetErrorYhigh(binNo-1)+totBkgTemp3[isEM].GetErrorYlow(binNo-1))
					pull.SetBinContent(binNo,(hData.GetBinContent(binNo)-bkgHT.GetBinContent(binNo))/math.sqrt(MCerror**2+hData.GetBinError(binNo)**2))
				else: pull.SetBinContent(binNo,0.)
			pull.SetMaximum(3)
			pull.SetMinimum(-3)
			pull.SetFillColor(2)
			pull.SetLineColor(2)
			formatLowerHist(pull)
			pull.GetYaxis().SetTitle('Pull')
			pull.Draw("HIST")

		# SAVE FILES
		savePrefix = templateDir.split('/')[-1]+'/plots/'
		if not os.path.exists(os.getcwd()+'/'+savePrefix): os.system('mkdir '+savePrefix)
		savePrefix+=histPrefix+isRebinned
		if doRealPull: savePrefix+='_pull'
		if yLog: savePrefix+='_logy'
		savePrefix += plotLabel
		if doOneBand:
			c1.SaveAs(savePrefix+"_totBand.pdf")
			c1.SaveAs(savePrefix+"_totBand.png")
			c1.SaveAs(savePrefix+"_totBand.C")
		else:
			c1.SaveAs(savePrefix+".pdf")
			c1.SaveAs(savePrefix+".png")
			c1.SaveAs(savePrefix+".C")
			
			

	RFile.Close()

print("--- %s minutes ---" % (round(time.time() - start_time, 2)/60))


