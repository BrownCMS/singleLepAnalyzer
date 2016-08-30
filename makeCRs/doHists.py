#!/usr/bin/python

import os,sys,time,math,datetime,pickle,itertools
from numpy import linspace
from weights import *
from samples import *
import ROOT as R

R.gROOT.SetBatch(1)
start_time = time.time()

lumiStr = str(targetlumi/1000).replace('.','p') # 1/fb
step1Dir = '/user_data/ssagir/LJMet_1lepTT_031816_step2AllNewSFs/nominal/'
"""
Note: 
--Each process in step1 (or step2) directories should have the root files hadded! 
--The code will look for <step1Dir>/<process>_hadd.root for nominal trees.
The uncertainty shape shifted files will be taken from <step1Dir>/../<shape>/<process>_hadd.root,
where <shape> is for example "JECUp". hadder.py can be used to prepare input files this way! 
--Each process given in the lists below must have a definition in "samples.py"
--Check the set of cuts in "analyze.py"
"""

if len(sys.argv)>2: isTTbarCR=int(sys.argv[2])
else: isTTbarCR = False # else it is Wjets

if isTTbarCR: 
	from analyzeTTJetsCR import *
else:
	from analyzeWJetsCR import *

bkgList = [
		   'DY50',
# 		   'WJets',
# 		   'WJetsMG',
		   'WJetsMG100',
		   'WJetsMG200',
		   'WJetsMG400',
		   'WJetsMG600',
		   'WJetsMG800',
		   'WJetsMG1200',
		   'WJetsMG2500',
		   'WW','WZ','ZZ',
# 		   'TTJets',
#  		   'TTJetsMG',
#  		   'TTJetsPH',
 		   'TTJetsPH0to700inc',
 		   'TTJetsPH700to1000inc',
 		   'TTJetsPH1000toINFinc',
 		   'TTJetsPH700mtt',
 		   'TTJetsPH1000mtt',
		   'TTWl','TTWq',
		   'TTZl','TTZq',
		   'Tt','Ts',
		   'TtW','TbtW',
 		   'QCDht100','QCDht200','QCDht300','QCDht500','QCDht700','QCDht1000','QCDht1500','QCDht2000',
		   ]

dataList = ['DataERRC','DataERRD','DataEPRD','DataMRRC','DataMRRD','DataMPRD']

whichSignal = 'TT' #TT, BB, or T53T53
signalMassRange = [700,1800]
sigList = [whichSignal+'M'+str(mass) for mass in range(signalMassRange[0],signalMassRange[1]+100,100)]
if whichSignal=='T53T53': sigList = [whichSignal+'M'+str(mass)+chiral for mass in range(signalMassRange[0],signalMassRange[1]+100,100) for chiral in ['left','right']]
if whichSignal=='TT': decays = ['BWBW','THTH','TZTZ','TZBW','THBW','TZTH'] #T' decays
if whichSignal=='BB': decays = ['TWTW','BHBH','BZBZ','BZTW','BHTW','BZBH'] #B' decays
if whichSignal=='T53T53': decays = [''] #decays to tWtW 100% of the time

doAllSys= True
doQ2sys = True
q2List  = [#energy scale sample to be processed
	      'TTJetsPHQ2U','TTJetsPHQ2D',
	      'TtWQ2U','TbtWQ2U',
	      'TtWQ2D','TbtWQ2D',
	      ]

cutList = {
		   'lepPtCut':40,
           'metCut':75,
		   'jet1PtCut':300,
		   'jet2PtCut':150,
		   'jet3PtCut':100,
		   'njetsCut':0,
		   'nbjetsCut':0,
		   'jet4PtCut':0,
		   'jet5PtCut':0,
		   'drCut':1,
		   'Wjet1PtCut':0,
		   'bjet1PtCut':0,
		   'htCut':0,
		   'stCut':0,
		   'minMlbCut':0,
		   }

cutString = 'lep'+str(int(cutList['lepPtCut']))+'_MET'+str(int(cutList['metCut']))+'_1jet'+str(int(cutList['jet1PtCut']))+'_2jet'+str(int(cutList['jet2PtCut']))+'_NJets'+str(int(cutList['njetsCut']))+'_NBJets'+str(int(cutList['nbjetsCut']))+'_3jet'+str(int(cutList['jet3PtCut']))+'_4jet'+str(int(cutList['jet4PtCut']))+'_5jet'+str(int(cutList['jet5PtCut']))+'_DR'+str(cutList['drCut'])+'_1Wjet'+str(cutList['Wjet1PtCut'])+'_1bjet'+str(cutList['bjet1PtCut'])+'_HT'+str(cutList['htCut'])+'_ST'+str(cutList['stCut'])+'_minMlb'+str(cutList['minMlbCut'])

cTime=datetime.datetime.now()
datestr='%i_%i_%i'%(cTime.year,cTime.month,cTime.day)
timestr='%i_%i_%i'%(cTime.hour,cTime.minute,cTime.second)
if isTTbarCR: pfix='ttbar_'
else: pfix='wjets_'
pfix+='tptp_'
pfix+=datestr#+'_'+timestr

if len(sys.argv)>1: outDir=sys.argv[1]
else: 
	outDir = os.getcwd()+'/'
	outDir+=pfix
	if not os.path.exists(outDir): os.system('mkdir '+outDir)
	if not os.path.exists(outDir+'/'+cutString): os.system('mkdir '+outDir+'/'+cutString)
	outDir+='/'+cutString

if len(sys.argv)>3: isEMlist=[str(sys.argv[3])]
else: isEMlist=['E','M']
if len(sys.argv)>4: nttaglist=[str(sys.argv[4])]
else: 
	if isTTbarCR: nttaglist=['0p'] #if '0p', the cut will not be applied
	else: nttaglist=['0p'] #if '0p', the cut will not be applied
if len(sys.argv)>5: nWtaglist=[str(sys.argv[5])]
else: 
	if isTTbarCR: nWtaglist=['0p']
	else: nWtaglist=['0','1p']
if len(sys.argv)>6: nbtaglist=[str(sys.argv[6])]
else: 
	if isTTbarCR: nbtaglist=['0','1','2p']
	else: nbtaglist=['0']

def negBinCorrection(hist): #set negative bin contents to zero and adjust the normalization
	norm0=hist.Integral()
	for iBin in range(0,hist.GetNbinsX()+2):
		if hist.GetBinContent(iBin)<0: hist.SetBinContent(iBin,0)
	if hist.Integral()!=0 and norm0>0: hist.Scale(norm0/hist.Integral())

def overflow(hist):
	nBinsX=hist.GetXaxis().GetNbins()
	content=hist.GetBinContent(nBinsX)+hist.GetBinContent(nBinsX+1)
	error=math.sqrt(hist.GetBinError(nBinsX)**2+hist.GetBinError(nBinsX+1)**2)
	hist.SetBinContent(nBinsX,content)
	hist.SetBinError(nBinsX,error)
	hist.SetBinContent(nBinsX+1,0)
	hist.SetBinError(nBinsX+1,0)
		
def readTree(file):
	if not os.path.exists(file): 
		print "Error: File does not exist! Aborting ...",file
		os._exit(1)
	tFile = R.TFile(file,'READ')
	tTree = tFile.Get('ljmet')
	return tFile, tTree 

print "READING TREES"
shapesFiles = ['jec','jer','btag']
tTreeData = {}
tFileData = {}
for data in dataList:
	print "READING:", data
	tFileData[data],tTreeData[data]=readTree(step1Dir+'/'+samples[data]+'_hadd.root')

tTreeSig = {}
tFileSig = {}
for sig in sigList:
	for decay in decays:
		print "READING:", sig+decay
		print "        nominal"
		tFileSig[sig+decay],tTreeSig[sig+decay]=readTree(step1Dir+'/'+samples[sig+decay]+'_hadd.root')
		if doAllSys:
			for syst in shapesFiles:
				for ud in ['Up','Down']:
					print "        "+syst+ud
					tFileSig[sig+decay+syst+ud],tTreeSig[sig+decay+syst+ud]=readTree(step1Dir.replace('nominal',syst.upper()+ud.lower())+'/'+samples[sig+decay]+'_hadd.root')

tTreeBkg = {}
tFileBkg = {}
for bkg in bkgList+q2List:
	print "READING:",bkg
	print "        nominal"
	tFileBkg[bkg],tTreeBkg[bkg]=readTree(step1Dir+'/'+samples[bkg]+'_hadd.root')
	if doAllSys:
		for syst in shapesFiles:
			for ud in ['Up','Down']:
				if bkg in q2List:
					tFileBkg[bkg+syst+ud],tTreeBkg[bkg+syst+ud]=None,None
				else:
					print "        "+syst+ud
					tFileBkg[bkg+syst+ud],tTreeBkg[bkg+syst+ud]=readTree(step1Dir.replace('nominal',syst.upper()+ud.lower())+'/'+samples[bkg]+'_hadd.root')
print "FINISHED READING"

plotList = {#discriminantName:(discriminantLJMETName, binning, xAxisLabel)
			'HT':('AK4HT',linspace(0, 5000, 51).tolist(),';H_{T} (GeV);'),
			'ST':('AK4HTpMETpLepPt',linspace(0, 5000, 51).tolist(),';S_{T} (GeV);'),
			'minMlb':('minMleppBjet',linspace(0, 800, 51).tolist(),';min[M(l,b)] (GeV);'),
			'MallJetsPlusWleptonic':('M_AllJets_PlusWleptonic',linspace(0, 5000, 101).tolist(),';M (all jets + Wleptonic) (GeV);'),
			'x53Mass':('xftMass',linspace(0, 5000, 51).tolist(),';M (X_{5/3}) (GeV);'),
			}

iPlot='minMlb' #choose a discriminant from plotList!
print "PLOTTING:",iPlot
print "         LJMET Variable:",plotList[iPlot][0]
print "         X-AXIS TITLE  :",plotList[iPlot][2]
print "         BINNING USED  :",plotList[iPlot][1]

nCats  = len(isEMlist)*len(nWtaglist)*len(nbtaglist)
catInd = 1
for cat in list(itertools.product(isEMlist,nttaglist,nWtaglist,nbtaglist)):
	catDir = cat[0]+'_nT'+cat[1]+'_nW'+cat[2]+'_nB'+cat[3]
	datahists = {}
	bkghists  = {}
	sighists  = {}
	if len(sys.argv)>1: outDir=sys.argv[1]
	else: 
		outDir = os.getcwd()+'/'
		outDir+=pfix
		if not os.path.exists(outDir): os.system('mkdir '+outDir)
		#if not os.path.exists(outDir+'/'+cutString): os.system('mkdir '+outDir+'/'+cutString)
		#outDir+='/'+cutString
		if not os.path.exists(outDir+'/'+catDir): os.system('mkdir '+outDir+'/'+catDir)
		outDir+='/'+catDir
	category = {'isEM':cat[0],'nttag':cat[1],'nWtag':cat[2],'nbtag':cat[3]}
	for data in dataList: 
		datahists.update(analyze(tTreeData,data,cutList,False,iPlot,plotList[iPlot],category))
		if catInd==nCats: del tFileData[data]
	for bkg in bkgList: 
		bkghists.update(analyze(tTreeBkg,bkg,cutList,doAllSys,iPlot,plotList[iPlot],category))
		if catInd==nCats: del tFileBkg[bkg]
		if doAllSys and catInd==nCats:
			for syst in shapesFiles:
				for ud in ['Up','Down']: del tFileBkg[bkg+syst+ud]
	for sig in sigList: 
		for decay in decays: 
			sighists.update(analyze(tTreeSig,sig+decay,cutList,doAllSys,iPlot,plotList[iPlot],category))
			if catInd==nCats: del tFileSig[sig+decay]
			if doAllSys and catInd==nCats:
				for syst in shapesFiles:
					for ud in ['Up','Down']: del tFileSig[sig+decay+syst+ud]
	if doQ2sys: 
		for q2 in q2List: 
			bkghists.update(analyze(tTreeBkg,q2,cutList,False,iPlot,plotList[iPlot],category))
			if catInd==nCats: del tFileBkg[q2]

	#Negative Bin Correction
	for bkg in bkghists.keys(): negBinCorrection(bkghists[bkg])

	#OverFlow Correction
	for data in datahists.keys(): overflow(datahists[data])
	for bkg in bkghists.keys():   overflow(bkghists[bkg])
	for sig in sighists.keys():   overflow(sighists[sig])

	pickle.dump(datahists,open(outDir+'/datahists.p','wb'))
	pickle.dump(bkghists,open(outDir+'/bkghists.p','wb'))
	pickle.dump(sighists,open(outDir+'/sighists.p','wb'))
	catInd+=1

print("--- %s minutes ---" % (round((time.time() - start_time)/60,2)))


