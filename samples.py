#!/usr/bin/python

samples = {
'DataEPRD':'SingleElectron_PRD',
'DataMPRD':'SingleMuon_PRD',
'DataEPRB':'SingleElectron_PRB',
'DataEPRC':'SingleElectron_PRC',
'DataMPRB':'SingleMuon_PRB',
'DataMPRC':'SingleMuon_PRC',

'DataEPRH':'SingleElectron_PRH',
'DataMPRH':'SingleMuon_PRH',
'DataERRBCDEFG':'SingleElectron_RRBCDEFG',
'DataMRRBCDEFG':'SingleMuon_RRBCDEFG',

'HTBM180':'ChargedHiggs_HplusTB_HplusToTB_M-180_13TeV_amcatnlo_pythia8',
'HTBM200':'ChargedHiggs_HplusTB_HplusToTB_M-200_13TeV_amcatnlo_pythia8',
'HTBM220':'ChargedHiggs_HplusTB_HplusToTB_M-220_13TeV_amcatnlo_pythia8',
'HTBM250':'ChargedHiggs_HplusTB_HplusToTB_M-250_13TeV_amcatnlo_pythia8',
'HTBM300':'ChargedHiggs_HplusTB_HplusToTB_M-300_13TeV_amcatnlo_pythia8',
'HTBM350':'ChargedHiggs_HplusTB_HplusToTB_M-350_13TeV_amcatnlo_pythia8',
'HTBM400':'ChargedHiggs_HplusTB_HplusToTB_M-400_13TeV_amcatnlo_pythia8',
'HTBM450':'ChargedHiggs_HplusTB_HplusToTB_M-450_13TeV_amcatnlo_pythia8',
'HTBM500':'ChargedHiggs_HplusTB_HplusToTB_M-500_13TeV_amcatnlo_pythia8',

'TTM700BWBW':'TprimeTprime_M-700_TuneCUETP8M1_13TeV-madgraph-pythia8_BWBW',
'TTM800BWBW':'TprimeTprime_M-800_TuneCUETP8M1_13TeV-madgraph-pythia8_BWBW',
'TTM900BWBW':'TprimeTprime_M-900_TuneCUETP8M1_13TeV-madgraph-pythia8_BWBW',
'TTM1000BWBW':'TprimeTprime_M-1000_TuneCUETP8M1_13TeV-madgraph-pythia8_BWBW',
'TTM1100BWBW':'TprimeTprime_M-1100_TuneCUETP8M1_13TeV-madgraph-pythia8_BWBW',
'TTM1200BWBW':'TprimeTprime_M-1200_TuneCUETP8M1_13TeV-madgraph-pythia8_BWBW',
'TTM1300BWBW':'TprimeTprime_M-1300_TuneCUETP8M1_13TeV-madgraph-pythia8_BWBW',
'TTM1400BWBW':'TprimeTprime_M-1400_TuneCUETP8M1_13TeV-madgraph-pythia8_BWBW',
'TTM1500BWBW':'TprimeTprime_M-1500_TuneCUETP8M1_13TeV-madgraph-pythia8_BWBW',
'TTM1600BWBW':'TprimeTprime_M-1600_TuneCUETP8M1_13TeV-madgraph-pythia8_BWBW',
'TTM1700BWBW':'TprimeTprime_M-1700_TuneCUETP8M1_13TeV-madgraph-pythia8_BWBW',
'TTM1800BWBW':'TprimeTprime_M-1800_TuneCUETP8M1_13TeV-madgraph-pythia8_BWBW',

'TTM700THBW':'TprimeTprime_M-700_TuneCUETP8M1_13TeV-madgraph-pythia8_THBW',
'TTM800THBW':'TprimeTprime_M-800_TuneCUETP8M1_13TeV-madgraph-pythia8_THBW',
'TTM900THBW':'TprimeTprime_M-900_TuneCUETP8M1_13TeV-madgraph-pythia8_THBW',
'TTM1000THBW':'TprimeTprime_M-1000_TuneCUETP8M1_13TeV-madgraph-pythia8_THBW',
'TTM1100THBW':'TprimeTprime_M-1100_TuneCUETP8M1_13TeV-madgraph-pythia8_THBW',
'TTM1200THBW':'TprimeTprime_M-1200_TuneCUETP8M1_13TeV-madgraph-pythia8_THBW',
'TTM1300THBW':'TprimeTprime_M-1300_TuneCUETP8M1_13TeV-madgraph-pythia8_THBW',
'TTM1400THBW':'TprimeTprime_M-1400_TuneCUETP8M1_13TeV-madgraph-pythia8_THBW',
'TTM1500THBW':'TprimeTprime_M-1500_TuneCUETP8M1_13TeV-madgraph-pythia8_THBW',
'TTM1600THBW':'TprimeTprime_M-1600_TuneCUETP8M1_13TeV-madgraph-pythia8_THBW',
'TTM1700THBW':'TprimeTprime_M-1700_TuneCUETP8M1_13TeV-madgraph-pythia8_THBW',
'TTM1800THBW':'TprimeTprime_M-1800_TuneCUETP8M1_13TeV-madgraph-pythia8_THBW',

'TTM700TZBW':'TprimeTprime_M-700_TuneCUETP8M1_13TeV-madgraph-pythia8_TZBW',
'TTM800TZBW':'TprimeTprime_M-800_TuneCUETP8M1_13TeV-madgraph-pythia8_TZBW',
'TTM900TZBW':'TprimeTprime_M-900_TuneCUETP8M1_13TeV-madgraph-pythia8_TZBW',
'TTM1000TZBW':'TprimeTprime_M-1000_TuneCUETP8M1_13TeV-madgraph-pythia8_TZBW',
'TTM1100TZBW':'TprimeTprime_M-1100_TuneCUETP8M1_13TeV-madgraph-pythia8_TZBW',
'TTM1200TZBW':'TprimeTprime_M-1200_TuneCUETP8M1_13TeV-madgraph-pythia8_TZBW',
'TTM1300TZBW':'TprimeTprime_M-1300_TuneCUETP8M1_13TeV-madgraph-pythia8_TZBW',
'TTM1400TZBW':'TprimeTprime_M-1400_TuneCUETP8M1_13TeV-madgraph-pythia8_TZBW',
'TTM1500TZBW':'TprimeTprime_M-1500_TuneCUETP8M1_13TeV-madgraph-pythia8_TZBW',
'TTM1600TZBW':'TprimeTprime_M-1600_TuneCUETP8M1_13TeV-madgraph-pythia8_TZBW',
'TTM1700TZBW':'TprimeTprime_M-1700_TuneCUETP8M1_13TeV-madgraph-pythia8_TZBW',
'TTM1800TZBW':'TprimeTprime_M-1800_TuneCUETP8M1_13TeV-madgraph-pythia8_TZBW',

'TTM700TZTZ':'TprimeTprime_M-700_TuneCUETP8M1_13TeV-madgraph-pythia8_TZTZ',
'TTM800TZTZ':'TprimeTprime_M-800_TuneCUETP8M1_13TeV-madgraph-pythia8_TZTZ',
'TTM900TZTZ':'TprimeTprime_M-900_TuneCUETP8M1_13TeV-madgraph-pythia8_TZTZ',
'TTM1000TZTZ':'TprimeTprime_M-1000_TuneCUETP8M1_13TeV-madgraph-pythia8_TZTZ',
'TTM1100TZTZ':'TprimeTprime_M-1100_TuneCUETP8M1_13TeV-madgraph-pythia8_TZTZ',
'TTM1200TZTZ':'TprimeTprime_M-1200_TuneCUETP8M1_13TeV-madgraph-pythia8_TZTZ',
'TTM1300TZTZ':'TprimeTprime_M-1300_TuneCUETP8M1_13TeV-madgraph-pythia8_TZTZ',
'TTM1400TZTZ':'TprimeTprime_M-1400_TuneCUETP8M1_13TeV-madgraph-pythia8_TZTZ',
'TTM1500TZTZ':'TprimeTprime_M-1500_TuneCUETP8M1_13TeV-madgraph-pythia8_TZTZ',
'TTM1600TZTZ':'TprimeTprime_M-1600_TuneCUETP8M1_13TeV-madgraph-pythia8_TZTZ',
'TTM1700TZTZ':'TprimeTprime_M-1700_TuneCUETP8M1_13TeV-madgraph-pythia8_TZTZ',
'TTM1800TZTZ':'TprimeTprime_M-1800_TuneCUETP8M1_13TeV-madgraph-pythia8_TZTZ',

'TTM700TZTH':'TprimeTprime_M-700_TuneCUETP8M1_13TeV-madgraph-pythia8_TZTH',
'TTM800TZTH':'TprimeTprime_M-800_TuneCUETP8M1_13TeV-madgraph-pythia8_TZTH',
'TTM900TZTH':'TprimeTprime_M-900_TuneCUETP8M1_13TeV-madgraph-pythia8_TZTH',
'TTM1000TZTH':'TprimeTprime_M-1000_TuneCUETP8M1_13TeV-madgraph-pythia8_TZTH',
'TTM1100TZTH':'TprimeTprime_M-1100_TuneCUETP8M1_13TeV-madgraph-pythia8_TZTH',
'TTM1200TZTH':'TprimeTprime_M-1200_TuneCUETP8M1_13TeV-madgraph-pythia8_TZTH',
'TTM1300TZTH':'TprimeTprime_M-1300_TuneCUETP8M1_13TeV-madgraph-pythia8_TZTH',
'TTM1400TZTH':'TprimeTprime_M-1400_TuneCUETP8M1_13TeV-madgraph-pythia8_TZTH',
'TTM1500TZTH':'TprimeTprime_M-1500_TuneCUETP8M1_13TeV-madgraph-pythia8_TZTH',
'TTM1600TZTH':'TprimeTprime_M-1600_TuneCUETP8M1_13TeV-madgraph-pythia8_TZTH',
'TTM1700TZTH':'TprimeTprime_M-1700_TuneCUETP8M1_13TeV-madgraph-pythia8_TZTH',
'TTM1800TZTH':'TprimeTprime_M-1800_TuneCUETP8M1_13TeV-madgraph-pythia8_TZTH',

'TTM700THTH':'TprimeTprime_M-700_TuneCUETP8M1_13TeV-madgraph-pythia8_THTH',
'TTM800THTH':'TprimeTprime_M-800_TuneCUETP8M1_13TeV-madgraph-pythia8_THTH',
'TTM900THTH':'TprimeTprime_M-900_TuneCUETP8M1_13TeV-madgraph-pythia8_THTH',
'TTM1000THTH':'TprimeTprime_M-1000_TuneCUETP8M1_13TeV-madgraph-pythia8_THTH',
'TTM1100THTH':'TprimeTprime_M-1100_TuneCUETP8M1_13TeV-madgraph-pythia8_THTH',
'TTM1200THTH':'TprimeTprime_M-1200_TuneCUETP8M1_13TeV-madgraph-pythia8_THTH',
'TTM1300THTH':'TprimeTprime_M-1300_TuneCUETP8M1_13TeV-madgraph-pythia8_THTH',
'TTM1400THTH':'TprimeTprime_M-1400_TuneCUETP8M1_13TeV-madgraph-pythia8_THTH',
'TTM1500THTH':'TprimeTprime_M-1500_TuneCUETP8M1_13TeV-madgraph-pythia8_THTH',
'TTM1600THTH':'TprimeTprime_M-1600_TuneCUETP8M1_13TeV-madgraph-pythia8_THTH',
'TTM1700THTH':'TprimeTprime_M-1700_TuneCUETP8M1_13TeV-madgraph-pythia8_THTH',
'TTM1800THTH':'TprimeTprime_M-1800_TuneCUETP8M1_13TeV-madgraph-pythia8_THTH',

'X53X53M700left':'X53X53_M-700_LH_TuneCUETP8M1_13TeV-madgraph-pythia8',
'X53X53M800left':'X53X53_M-800_LH_TuneCUETP8M1_13TeV-madgraph-pythia8',
'X53X53M900left':'X53X53_M-900_LH_TuneCUETP8M1_13TeV-madgraph-pythia8',
'X53X53M1000left':'X53X53_M-1000_LH_TuneCUETP8M1_13TeV-madgraph-pythia8',
'X53X53M1100left':'X53X53_M-1100_LH_TuneCUETP8M1_13TeV-madgraph-pythia8',
'X53X53M1200left':'X53X53_M-1200_LH_TuneCUETP8M1_13TeV-madgraph-pythia8',
'X53X53M1300left':'X53X53_M-1300_LH_TuneCUETP8M1_13TeV-madgraph-pythia8',
'X53X53M1400left':'X53X53_M-1400_LH_TuneCUETP8M1_13TeV-madgraph-pythia8',
'X53X53M1500left':'X53X53_M-1500_LH_TuneCUETP8M1_13TeV-madgraph-pythia8',
'X53X53M1600left':'X53X53_M-1600_LH_TuneCUETP8M1_13TeV-madgraph-pythia8',

'X53X53M700right':'X53X53_M-700_RH_TuneCUETP8M1_13TeV-madgraph-pythia8',
'X53X53M800right':'X53X53_M-800_RH_TuneCUETP8M1_13TeV-madgraph-pythia8',
'X53X53M900right':'X53X53_M-900_RH_TuneCUETP8M1_13TeV-madgraph-pythia8',
'X53X53M1000right':'X53X53_M-1000_RH_TuneCUETP8M1_13TeV-madgraph-pythia8',
'X53X53M1100right':'X53X53_M-1100_RH_TuneCUETP8M1_13TeV-madgraph-pythia8',
'X53X53M1200right':'X53X53_M-1200_RH_TuneCUETP8M1_13TeV-madgraph-pythia8',
'X53X53M1300right':'X53X53_M-1300_RH_TuneCUETP8M1_13TeV-madgraph-pythia8',
'X53X53M1400right':'X53X53_M-1400_RH_TuneCUETP8M1_13TeV-madgraph-pythia8',
'X53X53M1500right':'X53X53_M-1500_RH_TuneCUETP8M1_13TeV-madgraph-pythia8',
'X53X53M1600right':'X53X53_M-1600_RH_TuneCUETP8M1_13TeV-madgraph-pythia8',

'DY':'DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8',
'DYMG':'DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
'DYMG100':'DYJetsToLL_M-50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
'DYMG200':'DYJetsToLL_M-50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
'DYMG400':'DYJetsToLL_M-50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
'DYMG600':'DYJetsToLL_M-50_HT-600to800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
'DYMG800':'DYJetsToLL_M-50_HT-800to1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
'DYMG1200':'DYJetsToLL_M-50_HT-1200to2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
'DYMG2500':'DYJetsToLL_M-50_HT-2500toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',

'WJetsMG':'WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
'WJetsMG100':'WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
'WJetsMG200':'WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
'WJetsMG400':'WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
'WJetsMG600':'WJetsToLNu_HT-600To800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
'WJetsMG800':'WJetsToLNu_HT-800To1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
'WJetsMG1200':'WJetsToLNu_HT-1200To2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
'WJetsMG2500':'WJetsToLNu_HT-2500ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
'WJetsMGPt100':'WJetsToLNu_Pt-100To250_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8',
'WJetsMGPt250':'WJetsToLNu_Pt-250To400_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8',
'WJetsMGPt400':'WJetsToLNu_Pt-400To600_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8',
'WJetsMGPt600':'WJetsToLNu_Pt-600ToInf_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8',

'WW':'WW_TuneCUETP8M1_13TeV-pythia8',
'WZ':'WZ_TuneCUETP8M1_13TeV-pythia8',
'ZZ':'ZZ_TuneCUETP8M1_13TeV-pythia8',

'TTJets':'TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8',
'WJets':'WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8',

'TTJetsMG':'TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
'TTJetsPH':'TT_TuneCUETP8M2T4_13TeV-powheg-pythia8',
'TTJetsPHorig':'TT_TuneCUETP8M2T4_13TeV-powheg-pythia8_orig',
'TTJetsPHQ2U':'TT_TuneCUETP8M1_13TeV-powheg-scaleup-pythia8',
'TTJetsPHQ2D':'TT_TuneCUETP8M1_13TeV-powheg-scaledown-pythia8',
'TTJetsPH0to700inc':'TT_TuneCUETP8M2T4_13TeV-powheg-pythia8_Mtt0to700',
'TTJetsPH700to1000inc':'TT_TuneCUETP8M2T4_13TeV-powheg-pythia8_Mtt700to1000',
'TTJetsPH1000toINFinc':'TT_TuneCUETP8M2T4_13TeV-powheg-pythia8_Mtt1000toInf',
'TTJetsPH700mtt':'TT_Mtt-700to1000_TuneCUETP8M2T4_13TeV-powheg-pythia8',
'TTJetsPH1000mtt':'TT_Mtt-1000toInf_TuneCUETP8M2T4_13TeV-powheg-pythia8',

'TTWl':'TTWJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8',
'TTWq':'TTWJetsToQQ_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8',
'TTZl':'TTZToLLNuNu_M-10_TuneCUETP8M1_13TeV-amcatnlo-pythia8',
'TTZq':'TTZToQQ_TuneCUETP8M1_13TeV-amcatnlo-pythia8',
'Tt':'ST_t-channel_top_4f_inclusiveDecays_13TeV-powhegV2-madspin-pythia8_TuneCUETP8M1', 
'Tbt':'ST_t-channel_antitop_4f_inclusiveDecays_13TeV-powhegV2-madspin-pythia8_TuneCUETP8M1', 
'TtQ2U':'ST_t-channel_4f_scaleup_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1',
'TtQ2D':'ST_t-channel_4f_scaledown_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1',
'Ts':'ST_s-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1',
'TtW':'ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1',    #pow-pyth t -> tW
'TtWQ2U':'ST_tW_top_5f_scaleup_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1',
'TtWQ2D':'ST_tW_top_5f_scaledown_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1',
'TbtW':'ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1',  #pow-pyth tbar -> tW
'TbtWQ2U':'ST_tW_antitop_5f_scaleup_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1',
'TbtWQ2D':'ST_tW_antitop_5f_scaledown_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1',

'QCDht100':'QCD_HT100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
'QCDht200':'QCD_HT200to300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
'QCDht300':'QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
'QCDht500':'QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
'QCDht700':'QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
'QCDht1000':'QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
'QCDht1500':'QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
'QCDht2000':'QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
}
samples['WJetsMG100JSF']  = samples['WJetsMG100']
samples['WJetsMG200JSF']  = samples['WJetsMG200']
samples['WJetsMG400JSF']  = samples['WJetsMG400']
samples['WJetsMG600JSF']  = samples['WJetsMG600']
samples['WJetsMG800JSF']  = samples['WJetsMG800']
samples['WJetsMG1200JSF'] = samples['WJetsMG1200']
samples['WJetsMG2500JSF'] = samples['WJetsMG2500']
samples['QCDht100JSF']  = samples['QCDht100']
samples['QCDht200JSF']  = samples['QCDht200']
samples['QCDht300JSF']  = samples['QCDht300']
samples['QCDht500JSF']  = samples['QCDht500']
samples['QCDht700JSF']  = samples['QCDht700']
samples['QCDht1000JSF'] = samples['QCDht1000']
samples['QCDht1500JSF'] = samples['QCDht1500']
samples['QCDht2000JSF'] = samples['QCDht2000']



