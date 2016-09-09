#!/usr/bin/python

import os,sys,time,math,fnmatch
from array import array
from ROOT import *

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Run as:
# > python modifyBinning.py
# 
# Optional arguments:
# -- statistical uncertainty threshold (default is 30%)
#
# Notes:
# -- Finds certain root files in a given directory and rebins all histograms in each file
# -- A selection of subset of files in the input directory can be done below under "#Setup the selection ..."
# -- A custom binning choice can also be given below and this choice can be activated by giving a stat unc 
#    threshold larger than 100% (>1.) in the argument
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

cutString = 'lep80_MET100_1jet200_2jet90_NJets4_NBJets1_3jet0_4jet0_5jet0_DR1_1Wjet0_1bjet0_HT0_ST0_minMlb0'
templateDir = os.getcwd()+'/templates_minMlb_noJSF_2016_9_8/'+cutString

rebinHists = True
xbinsList = {}
#Binning for Inclusive WJets sample:
xbinsList['isE_nT0_nW0_nB0']    = [0.0, 32.0, 48.0, 64.0, 80.0, 96.0, 112.0, 128.0, 144.0, 160.0, 176.0, 192.0, 208.0, 224.0, 240.0, 256.0, 272.0, 288.0, 304.0, 320.0, 336.0, 352.0, 368.0, 384.0, 400.0, 416.0, 432.0, 464.0, 480.0, 512.0, 528.0, 800.0]
xbinsList['isM_nT0_nW0_nB0']    = xbinsList['isE_nT0_nW0_nB0']

xbinsList['isE_nT0_nW0_nB1']    = [0.0, 32.0, 48.0, 64.0, 80.0, 96.0, 112.0, 128.0, 144.0, 160.0, 176.0, 192.0, 208.0, 224.0, 240.0, 256.0, 272.0, 288.0, 304.0, 320.0, 336.0, 352.0, 368.0, 384.0, 400.0, 416.0, 432.0, 448.0, 464.0, 480.0, 496.0, 512.0, 528.0, 544.0, 560.0, 576.0, 592.0, 608.0, 624.0, 640.0, 656.0, 672.0, 688.0, 704.0, 720.0, 736.0, 752.0, 768.0, 784.0, 800.0]
xbinsList['isM_nT0_nW0_nB1']    = xbinsList['isE_nT0_nW0_nB1']

xbinsList['isE_nT0_nW0_nB2p']   = [0.0, 48.0, 64.0, 80.0, 96.0, 112.0, 128.0, 144.0, 160.0, 176.0, 192.0, 208.0, 224.0, 240.0, 256.0, 272.0, 288.0, 304.0, 320.0, 336.0, 352.0, 368.0, 384.0, 400.0, 416.0, 432.0, 448.0, 464.0, 480.0, 496.0, 512.0, 544.0, 560.0, 576.0, 592.0, 608.0, 640.0, 688.0, 752.0, 800.0]
xbinsList['isM_nT0_nW0_nB2p']   = xbinsList['isE_nT0_nW0_nB2p']

xbinsList['isE_nT0_nW1p_nB0']   = [0.0, 32.0, 48.0, 64.0, 80.0, 96.0, 112.0, 128.0, 144.0, 160.0, 176.0, 192.0, 208.0, 224.0, 240.0, 256.0, 272.0, 288.0, 304.0, 320.0, 336.0, 352.0, 368.0, 384.0, 400.0, 416.0, 432.0, 448.0, 800.0]
xbinsList['isM_nT0_nW1p_nB0']   = xbinsList['isE_nT0_nW1p_nB0']

xbinsList['isE_nT0_nW1p_nB1']   = [0.0, 32.0, 48.0, 64.0, 80.0, 96.0, 112.0, 128.0, 144.0, 160.0, 176.0, 192.0, 208.0, 224.0, 240.0, 256.0, 272.0, 288.0, 304.0, 320.0, 336.0, 352.0, 368.0, 384.0, 400.0, 416.0, 432.0, 448.0, 464.0, 480.0, 496.0, 512.0, 528.0, 544.0, 560.0, 576.0, 592.0, 608.0, 624.0, 640.0, 656.0, 672.0, 688.0, 704.0, 720.0, 736.0, 752.0, 768.0, 784.0, 800.0]
xbinsList['isM_nT0_nW1p_nB1']   = xbinsList['isE_nT0_nW1p_nB1']

xbinsList['isE_nT0_nW1p_nB2p']  = [0.0, 48.0, 64.0, 80.0, 96.0, 112.0, 128.0, 144.0, 160.0, 176.0, 192.0, 208.0, 224.0, 240.0, 256.0, 272.0, 288.0, 304.0, 320.0, 336.0, 352.0, 368.0, 384.0, 400.0, 416.0, 432.0, 448.0, 464.0, 480.0, 496.0, 512.0, 528.0, 560.0, 592.0, 624.0, 688.0, 800.0]
xbinsList['isM_nT0_nW1p_nB2p']  = xbinsList['isE_nT0_nW1p_nB2p']

xbinsList['isE_nT1p_nW0_nB0']   = [0.0, 48.0, 64.0, 80.0, 96.0, 112.0, 128.0, 144.0, 160.0, 176.0, 192.0, 208.0, 224.0, 240.0, 256.0, 272.0, 288.0, 304.0, 320.0, 336.0, 352.0, 368.0, 384.0, 400.0, 416.0, 464.0, 800.0]
xbinsList['isM_nT1p_nW0_nB0']   = xbinsList['isE_nT1p_nW0_nB0']

xbinsList['isE_nT1p_nW0_nB1']   = [0.0, 48.0, 64.0, 80.0, 96.0, 112.0, 128.0, 144.0, 160.0, 176.0, 192.0, 208.0, 224.0, 240.0, 256.0, 272.0, 288.0, 304.0, 320.0, 336.0, 352.0, 368.0, 384.0, 400.0, 416.0, 432.0, 448.0, 464.0, 480.0, 496.0, 512.0, 528.0, 544.0, 560.0, 576.0, 592.0, 608.0, 624.0, 640.0, 656.0, 672.0, 688.0, 704.0, 720.0, 736.0, 752.0, 768.0, 784.0, 800.0]
xbinsList['isM_nT1p_nW0_nB1']   = xbinsList['isE_nT1p_nW0_nB1']

xbinsList['isE_nT1p_nW0_nB2p']  = [0.0, 48.0, 64.0, 80.0, 96.0, 112.0, 128.0, 144.0, 160.0, 176.0, 192.0, 208.0, 224.0, 240.0, 256.0, 272.0, 288.0, 304.0, 320.0, 336.0, 352.0, 368.0, 384.0, 400.0, 416.0, 432.0, 448.0, 464.0, 496.0, 528.0, 544.0, 560.0, 592.0, 640.0, 800.0]
xbinsList['isM_nT1p_nW0_nB2p']  = xbinsList['isE_nT1p_nW0_nB2p']

xbinsList['isE_nT1p_nW1p_nB0']  = [0.0, 48.0, 64.0, 80.0, 96.0, 112.0, 128.0, 144.0, 160.0, 176.0, 192.0, 208.0, 224.0, 240.0, 256.0, 288.0, 336.0, 800.0]
xbinsList['isM_nT1p_nW1p_nB0']  = xbinsList['isE_nT1p_nW1p_nB0']

xbinsList['isE_nT1p_nW1p_nB1']  = [0.0, 64.0, 80.0, 96.0, 112.0, 128.0, 144.0, 160.0, 176.0, 192.0, 208.0, 224.0, 240.0, 256.0, 272.0, 288.0, 304.0, 320.0, 336.0, 352.0, 368.0, 384.0, 400.0, 416.0, 432.0, 448.0, 464.0, 480.0, 496.0, 512.0, 528.0, 544.0, 560.0, 576.0, 592.0, 608.0, 624.0, 640.0, 656.0, 672.0, 688.0, 736.0, 768.0, 784.0, 800.0]
xbinsList['isM_nT1p_nW1p_nB1']  = xbinsList['isE_nT1p_nW1p_nB1']

xbinsList['isE_nT1p_nW1p_nB2p'] = [0.0, 48.0, 64.0, 80.0, 96.0, 112.0, 128.0, 144.0, 160.0, 176.0, 192.0, 208.0, 224.0, 240.0, 256.0, 272.0, 288.0, 304.0, 336.0, 384.0, 400.0, 528.0, 672.0, 800.0]
xbinsList['isM_nT1p_nW1p_nB2p'] = xbinsList['isE_nT1p_nW1p_nB2p']

# Binning for no top tag:
xbinsList['isE_nT0p_nW0_nB0']    = [0.0, 32.0, 48.0, 64.0, 80.0, 96.0, 112.0, 128.0, 144.0, 160.0, 176.0, 192.0, 208.0, 224.0, 240.0, 256.0, 272.0, 288.0, 304.0, 320.0, 336.0, 352.0, 368.0, 384.0, 400.0, 416.0, 432.0, 464.0, 480.0, 512.0, 528.0, 800.0]
xbinsList['isM_nT0p_nW0_nB0']    = xbinsList['isE_nT0p_nW0_nB0']

xbinsList['isE_nT0p_nW0_nB1']    = [0.0, 32.0, 48.0, 64.0, 80.0, 96.0, 112.0, 128.0, 144.0, 160.0, 176.0, 192.0, 208.0, 224.0, 240.0, 256.0, 272.0, 288.0, 304.0, 320.0, 336.0, 352.0, 368.0, 384.0, 400.0, 416.0, 432.0, 448.0, 464.0, 480.0, 496.0, 512.0, 528.0, 544.0, 560.0, 576.0, 592.0, 608.0, 624.0, 640.0, 656.0, 672.0, 688.0, 704.0, 720.0, 736.0, 752.0, 768.0, 784.0, 800.0]
xbinsList['isM_nT0p_nW0_nB1']    = xbinsList['isE_nT0p_nW0_nB1']

xbinsList['isE_nT0p_nW0_nB2p']   = [0.0, 48.0, 64.0, 80.0, 96.0, 112.0, 128.0, 144.0, 160.0, 176.0, 192.0, 208.0, 224.0, 240.0, 256.0, 272.0, 288.0, 304.0, 320.0, 336.0, 352.0, 368.0, 384.0, 400.0, 416.0, 432.0, 448.0, 464.0, 480.0, 496.0, 512.0, 528.0, 544.0, 560.0, 576.0, 592.0, 608.0, 624.0, 640.0, 656.0, 672.0, 704.0, 752.0, 800.0]
xbinsList['isM_nT0p_nW0_nB2p']   = xbinsList['isE_nT0p_nW0_nB2p']

xbinsList['isE_nT0p_nW1p_nB0']   = [0.0, 32.0, 48.0, 64.0, 80.0, 96.0, 112.0, 128.0, 144.0, 160.0, 176.0, 192.0, 208.0, 224.0, 240.0, 256.0, 272.0, 288.0, 304.0, 320.0, 336.0, 352.0, 368.0, 384.0, 400.0, 416.0, 432.0, 448.0, 800.0]
xbinsList['isM_nT0p_nW1p_nB0']   = xbinsList['isE_nT0p_nW1p_nB0']

xbinsList['isE_nT0p_nW1p_nB1']   = [0.0, 32.0, 48.0, 64.0, 80.0, 96.0, 112.0, 128.0, 144.0, 160.0, 176.0, 192.0, 208.0, 224.0, 240.0, 256.0, 272.0, 288.0, 304.0, 320.0, 336.0, 352.0, 368.0, 384.0, 400.0, 416.0, 432.0, 448.0, 464.0, 480.0, 496.0, 512.0, 528.0, 544.0, 560.0, 576.0, 592.0, 608.0, 624.0, 640.0, 656.0, 672.0, 688.0, 704.0, 720.0, 736.0, 752.0, 768.0, 784.0, 800.0]
xbinsList['isM_nT0p_nW1p_nB1']   = xbinsList['isE_nT0p_nW1p_nB1']

xbinsList['isE_nT0p_nW1p_nB2p']  = [0.0, 48.0, 64.0, 80.0, 96.0, 112.0, 128.0, 144.0, 160.0, 176.0, 192.0, 208.0, 224.0, 240.0, 256.0, 272.0, 288.0, 304.0, 320.0, 336.0, 352.0, 368.0, 384.0, 400.0, 416.0, 432.0, 448.0, 464.0, 480.0, 496.0, 512.0, 528.0, 560.0, 592.0, 624.0, 656.0, 688.0, 800.0]
xbinsList['isM_nT0p_nW1p_nB2p']  = xbinsList['isE_nT0p_nW1p_nB2p']

#Binning for HTbinned WJets sample:
# xbinsList['isE_nT0_nW0_nB0']    = [0.0, 32.0, 48.0, 64.0, 80.0, 96.0, 112.0, 128.0, 144.0, 160.0, 176.0, 192.0, 208.0, 224.0, 240.0, 256.0, 272.0, 288.0, 304.0, 320.0, 336.0, 352.0, 368.0, 384.0, 400.0, 416.0, 432.0, 448.0, 464.0, 480.0, 496.0, 512.0, 528.0, 544.0, 560.0, 576.0, 592.0, 608.0, 624.0, 640.0, 656.0, 672.0, 688.0, 704.0, 736.0, 752.0, 800.0]
# xbinsList['isM_nT0_nW0_nB0']    = xbinsList['isE_nT0_nW0_nB0']
# 
# xbinsList['isE_nT0_nW0_nB1']    = [0.0, 32.0, 48.0, 64.0, 80.0, 96.0, 112.0, 128.0, 144.0, 160.0, 176.0, 192.0, 208.0, 224.0, 240.0, 256.0, 272.0, 288.0, 304.0, 320.0, 336.0, 352.0, 368.0, 384.0, 400.0, 416.0, 432.0, 448.0, 464.0, 480.0, 496.0, 512.0, 528.0, 544.0, 560.0, 576.0, 592.0, 608.0, 624.0, 640.0, 656.0, 672.0, 688.0, 704.0, 720.0, 736.0, 752.0, 768.0, 784.0, 800.0]
# xbinsList['isM_nT0_nW0_nB1']    = xbinsList['isE_nT0_nW0_nB1']
# 
# xbinsList['isE_nT0_nW0_nB2p']   = [0.0, 48.0, 64.0, 80.0, 96.0, 112.0, 128.0, 144.0, 160.0, 176.0, 192.0, 208.0, 224.0, 240.0, 256.0, 272.0, 288.0, 304.0, 320.0, 336.0, 352.0, 368.0, 384.0, 400.0, 416.0, 432.0, 448.0, 464.0, 480.0, 496.0, 512.0, 528.0, 544.0, 560.0, 576.0, 592.0, 608.0, 624.0, 640.0, 656.0, 672.0, 688.0, 704.0, 720.0, 736.0, 752.0, 800.0]
# xbinsList['isM_nT0_nW0_nB2p']   = xbinsList['isE_nT0_nW0_nB2p']
# 
# xbinsList['isE_nT0_nW1p_nB0']   = [0.0, 32.0, 48.0, 64.0, 80.0, 96.0, 112.0, 128.0, 144.0, 160.0, 176.0, 192.0, 208.0, 224.0, 240.0, 256.0, 272.0, 288.0, 304.0, 320.0, 336.0, 352.0, 368.0, 384.0, 400.0, 416.0, 432.0, 448.0, 464.0, 480.0, 496.0, 512.0, 528.0, 544.0, 560.0, 576.0, 592.0, 608.0, 640.0, 656.0, 672.0, 736.0, 800.0]
# xbinsList['isM_nT0_nW1p_nB0']   = xbinsList['isE_nT0_nW1p_nB0']
# 
# xbinsList['isE_nT0_nW1p_nB1']   = [0.0, 32.0, 48.0, 64.0, 80.0, 96.0, 112.0, 128.0, 144.0, 160.0, 176.0, 192.0, 208.0, 224.0, 240.0, 256.0, 272.0, 288.0, 304.0, 320.0, 336.0, 352.0, 368.0, 384.0, 400.0, 416.0, 432.0, 448.0, 464.0, 480.0, 496.0, 512.0, 528.0, 544.0, 560.0, 576.0, 592.0, 608.0, 624.0, 640.0, 656.0, 672.0, 688.0, 704.0, 720.0, 736.0, 752.0, 768.0, 784.0, 800.0]
# xbinsList['isM_nT0_nW1p_nB1']   = xbinsList['isE_nT0_nW1p_nB1']
# 
# xbinsList['isE_nT0_nW1p_nB2p']  = [0.0, 48.0, 64.0, 80.0, 96.0, 112.0, 128.0, 144.0, 160.0, 176.0, 192.0, 208.0, 224.0, 240.0, 256.0, 272.0, 288.0, 304.0, 320.0, 336.0, 352.0, 368.0, 384.0, 400.0, 416.0, 432.0, 448.0, 464.0, 480.0, 496.0, 512.0, 528.0, 560.0, 592.0, 608.0, 624.0, 656.0, 688.0, 800.0]
# xbinsList['isM_nT0_nW1p_nB2p']  = xbinsList['isE_nT0_nW1p_nB2p']
# 
# xbinsList['isE_nT1p_nW0_nB0']   = [0.0, 48.0, 64.0, 80.0, 96.0, 112.0, 128.0, 144.0, 160.0, 176.0, 192.0, 208.0, 224.0, 240.0, 256.0, 272.0, 288.0, 304.0, 320.0, 336.0, 352.0, 368.0, 384.0, 400.0, 416.0, 464.0, 496.0, 528.0, 544.0, 576.0, 800.0]
# xbinsList['isM_nT1p_nW0_nB0']   = xbinsList['isE_nT1p_nW0_nB0']
# 
# xbinsList['isE_nT1p_nW0_nB1']   = [0.0, 48.0, 64.0, 80.0, 96.0, 112.0, 128.0, 144.0, 160.0, 176.0, 192.0, 208.0, 224.0, 240.0, 256.0, 272.0, 288.0, 304.0, 320.0, 336.0, 352.0, 368.0, 384.0, 400.0, 416.0, 432.0, 448.0, 464.0, 480.0, 496.0, 512.0, 528.0, 544.0, 560.0, 576.0, 592.0, 608.0, 624.0, 640.0, 656.0, 672.0, 688.0, 704.0, 720.0, 736.0, 752.0, 768.0, 784.0, 800.0]
# xbinsList['isM_nT1p_nW0_nB1']   = xbinsList['isE_nT1p_nW0_nB1']
# 
# xbinsList['isE_nT1p_nW0_nB2p']  = [0.0, 48.0, 64.0, 80.0, 96.0, 112.0, 128.0, 144.0, 160.0, 176.0, 192.0, 208.0, 224.0, 240.0, 256.0, 272.0, 288.0, 304.0, 320.0, 336.0, 352.0, 368.0, 384.0, 400.0, 416.0, 432.0, 448.0, 464.0, 496.0, 528.0, 544.0, 560.0, 576.0, 592.0, 640.0, 800.0]
# xbinsList['isM_nT1p_nW0_nB2p']  = xbinsList['isE_nT1p_nW0_nB2p']
# 
# xbinsList['isE_nT1p_nW1p_nB0']  = [0.0, 48.0, 64.0, 80.0, 96.0, 112.0, 128.0, 144.0, 160.0, 176.0, 192.0, 208.0, 224.0, 240.0, 256.0, 288.0, 336.0, 448.0, 800.0]
# xbinsList['isM_nT1p_nW1p_nB0']  = xbinsList['isE_nT1p_nW1p_nB0']
# 
# xbinsList['isE_nT1p_nW1p_nB1']  = [0.0, 64.0, 80.0, 96.0, 112.0, 128.0, 144.0, 160.0, 176.0, 192.0, 208.0, 224.0, 240.0, 256.0, 272.0, 288.0, 304.0, 320.0, 336.0, 352.0, 368.0, 384.0, 400.0, 416.0, 432.0, 448.0, 464.0, 480.0, 496.0, 512.0, 528.0, 544.0, 560.0, 576.0, 592.0, 608.0, 624.0, 640.0, 656.0, 672.0, 688.0, 736.0, 768.0, 784.0, 800.0]
# xbinsList['isM_nT1p_nW1p_nB1']  = xbinsList['isE_nT1p_nW1p_nB1']
# 
# xbinsList['isE_nT1p_nW1p_nB2p'] = [0.0, 48.0, 64.0, 80.0, 96.0, 112.0, 128.0, 144.0, 160.0, 176.0, 192.0, 208.0, 224.0, 240.0, 256.0, 272.0, 288.0, 304.0, 336.0, 384.0, 400.0, 528.0, 672.0, 800.0]
# xbinsList['isM_nT1p_nW1p_nB2p'] = xbinsList['isE_nT1p_nW1p_nB2p']
# 
# # Binning for no top tag:
# xbinsList['isE_nT0p_nW0_nB0']    = [0.0, 32.0, 48.0, 64.0, 80.0, 96.0, 112.0, 128.0, 144.0, 160.0, 176.0, 192.0, 208.0, 224.0, 240.0, 256.0, 272.0, 288.0, 304.0, 320.0, 336.0, 352.0, 368.0, 384.0, 400.0, 416.0, 432.0, 448.0, 464.0, 480.0, 496.0, 512.0, 528.0, 544.0, 560.0, 576.0, 592.0, 608.0, 624.0, 640.0, 656.0, 672.0, 688.0, 704.0, 736.0, 752.0, 800.0]
# xbinsList['isM_nT0p_nW0_nB0']    = xbinsList['isE_nT0p_nW0_nB0']
# 
# xbinsList['isE_nT0p_nW0_nB1']    = [0.0, 32.0, 48.0, 64.0, 80.0, 96.0, 112.0, 128.0, 144.0, 160.0, 176.0, 192.0, 208.0, 224.0, 240.0, 256.0, 272.0, 288.0, 304.0, 320.0, 336.0, 352.0, 368.0, 384.0, 400.0, 416.0, 432.0, 448.0, 464.0, 480.0, 496.0, 512.0, 528.0, 544.0, 560.0, 576.0, 592.0, 608.0, 624.0, 640.0, 656.0, 672.0, 688.0, 704.0, 720.0, 736.0, 752.0, 768.0, 784.0, 800.0]
# xbinsList['isM_nT0p_nW0_nB1']    = xbinsList['isE_nT0p_nW0_nB1']
# 
# xbinsList['isE_nT0p_nW0_nB2p']   = [0.0, 48.0, 64.0, 80.0, 96.0, 112.0, 128.0, 144.0, 160.0, 176.0, 192.0, 208.0, 224.0, 240.0, 256.0, 272.0, 288.0, 304.0, 320.0, 336.0, 352.0, 368.0, 384.0, 400.0, 416.0, 432.0, 448.0, 464.0, 480.0, 496.0, 512.0, 528.0, 544.0, 560.0, 576.0, 592.0, 608.0, 624.0, 640.0, 656.0, 672.0, 688.0, 704.0, 720.0, 736.0, 752.0, 800.0]
# xbinsList['isM_nT0p_nW0_nB2p']   = xbinsList['isE_nT0p_nW0_nB2p']
# 
# xbinsList['isE_nT0p_nW1p_nB0']   = [0.0, 32.0, 48.0, 64.0, 80.0, 96.0, 112.0, 128.0, 144.0, 160.0, 176.0, 192.0, 208.0, 224.0, 240.0, 256.0, 272.0, 288.0, 304.0, 320.0, 336.0, 352.0, 368.0, 384.0, 400.0, 416.0, 432.0, 448.0, 464.0, 480.0, 496.0, 512.0, 528.0, 544.0, 560.0, 576.0, 592.0, 608.0, 640.0, 656.0, 672.0, 736.0, 800.0]
# xbinsList['isM_nT0p_nW1p_nB0']   = xbinsList['isE_nT0p_nW1p_nB0']
# 
# xbinsList['isE_nT0p_nW1p_nB1']   = [0.0, 32.0, 48.0, 64.0, 80.0, 96.0, 112.0, 128.0, 144.0, 160.0, 176.0, 192.0, 208.0, 224.0, 240.0, 256.0, 272.0, 288.0, 304.0, 320.0, 336.0, 352.0, 368.0, 384.0, 400.0, 416.0, 432.0, 448.0, 464.0, 480.0, 496.0, 512.0, 528.0, 544.0, 560.0, 576.0, 592.0, 608.0, 624.0, 640.0, 656.0, 672.0, 688.0, 704.0, 720.0, 736.0, 752.0, 768.0, 784.0, 800.0]
# xbinsList['isM_nT0p_nW1p_nB1']   = xbinsList['isE_nT0p_nW1p_nB1']
# 
# xbinsList['isE_nT0p_nW1p_nB2p']  = [0.0, 48.0, 64.0, 80.0, 96.0, 112.0, 128.0, 144.0, 160.0, 176.0, 192.0, 208.0, 224.0, 240.0, 256.0, 272.0, 288.0, 304.0, 320.0, 336.0, 352.0, 368.0, 384.0, 400.0, 416.0, 432.0, 448.0, 464.0, 480.0, 496.0, 512.0, 528.0, 560.0, 592.0, 608.0, 624.0, 656.0, 688.0, 800.0]
# xbinsList['isM_nT0p_nW1p_nB2p']  = xbinsList['isE_nT0p_nW1p_nB2p']

xbinsListDec10 = [0.,48.,64.,96.,128.,160.,192.,224.,256.,288.,320.,352.,384.,416.,448.,480.,512.,560.,608.,650.,700.,750.,800.] #X5/3 binning -- Dec 10, 2015
#for cat in xbinsList.keys(): xbinsList[cat] = xbinsListDec10

normalizeRENORM = True #does it only for signals
normalizePDF    = True #does it only for signals
removalKeys = {} # True == keep, False == remove
removalKeys['muR__']       = False
removalKeys['muF__']       = False
removalKeys['muRFcorrd__'] = False
removalKeys['muRFenv__']   = False
removalKeys['toppt__']     = True
removalKeys['jmr__']       = True
removalKeys['jms__']       = True
removalKeys['tau21__']     = True
removalKeys['jsf__']       = True

def findfiles(path, filtre):
    for root, dirs, files in os.walk(path):
        for f in fnmatch.filter(files, filtre):
            yield os.path.join(root, f)

rfiles = [file for file in findfiles(templateDir, '*.root') if '00left_2p318fb.root' in file or '00right_2p318fb.root' in file]
rfiles = [file for file in rfiles if 'rebinned' not in file]

stat = 0.3 # 30% statistical uncertainty requirement
if len(sys.argv)>1: stat=float(sys.argv[1])

rebinTFile = TFile(rfiles[0])
datahists = [k.GetName() for k in rebinTFile.GetListOfKeys() if '__DATA' in k.GetName()]
totBkgHists = {}
for hist in datahists:
	channel = hist[hist.find('fb_')+3:hist.find('__')]
	totBkgHists[channel]=rebinTFile.Get(hist.replace('__DATA','__top')).Clone()
	try: totBkgHists[channel].Add(rebinTFile.Get(hist.replace('__DATA','__ewk')))
	except: pass
	try: totBkgHists[channel].Add(rebinTFile.Get(hist.replace('__DATA','__qcd')))
	except: pass
# 	for iBin in range(1,totBkgHists[channel].GetNbinsX()+1):
# 		if totBkgHists[channel].GetBinError(iBin)/totBkgHists[channel].GetBinContent(iBin)>0.15:
# 			print channel, iBin, totBkgHists[channel].GetBinError(iBin)/totBkgHists[channel].GetBinContent(iBin)

xbinsListTemp = {}
for chn in totBkgHists.keys():
	if 'isE' not in chn: continue
	xbinsListTemp[chn]=[rebinTFile.Get(datahists[0]).GetXaxis().GetBinUpEdge(rebinTFile.Get(datahists[0]).GetXaxis().GetNbins())]
	Nbins = rebinTFile.Get(datahists[0]).GetNbinsX()
	totTempBinContent_E = 0.
	totTempBinContent_M = 0.
	totTempBinErrSquared_E = 0.
	totTempBinErrSquared_M = 0.
	for iBin in range(1,Nbins+1):
		totTempBinContent_E += totBkgHists[chn].GetBinContent(Nbins+1-iBin)
		totTempBinContent_M += totBkgHists[chn.replace('isE','isM')].GetBinContent(Nbins+1-iBin)
		totTempBinErrSquared_E += totBkgHists[chn].GetBinError(Nbins+1-iBin)**2
		totTempBinErrSquared_M += totBkgHists[chn.replace('isE','isM')].GetBinError(Nbins+1-iBin)**2
		if totTempBinContent_E>0. and totTempBinContent_M>0.:
			if math.sqrt(totTempBinErrSquared_E)/totTempBinContent_E<=stat and math.sqrt(totTempBinErrSquared_M)/totTempBinContent_M<=stat:
				#print totTempBinContent_E, totTempBinContent_M
				#print math.sqrt(totTempBinErrSquared_E)/totTempBinContent_E, math.sqrt(totTempBinErrSquared_M)/totTempBinContent_M
				totTempBinContent_E = 0.
				totTempBinContent_M = 0.
				totTempBinErrSquared_E = 0.
				totTempBinErrSquared_M = 0.
				xbinsListTemp[chn].append(totBkgHists[chn].GetXaxis().GetBinLowEdge(Nbins+1-iBin))
	if xbinsListTemp[chn][-1]!=0: xbinsListTemp[chn].append(0)
	if totBkgHists[chn].GetBinContent(1)==0. or totBkgHists[chn.replace('isE','isM')].GetBinContent(1)==0.: 
		if len(xbinsListTemp[chn])>2: del xbinsListTemp[chn][-2]
	elif totBkgHists[chn].GetBinError(1)/totBkgHists[chn].GetBinContent(1)>stat or totBkgHists[chn.replace('isE','isM')].GetBinError(1)/totBkgHists[chn.replace('isE','isM')].GetBinContent(1)>stat: 
		if len(xbinsListTemp[chn])>2: del xbinsListTemp[chn][-2]
	xbinsListTemp[chn.replace('isE','isM')]=xbinsListTemp[chn]

if stat<=1.:
	xbinsList = {}
	for chn in xbinsListTemp.keys():
		xbinsList[chn] = []
		for bin in range(len(xbinsListTemp[chn])): xbinsList[chn].append(xbinsListTemp[chn][len(xbinsListTemp[chn])-1-bin])
		print chn,xbinsList[chn]
else: stat = 'Custom'

xbins = {}
for key in xbinsList.keys(): xbins[key] = array('d', xbinsList[key])

#os._exit(1)
tfile = {}
outputRfile = {}
iRfile=0
for file in rfiles:
	print file
	tfile[iRfile] = TFile(file)
	rebinnedHists = {}
	if rebinHists: outputRfile[iRfile] = TFile(file.replace('.root','_rebinned_stat'+str(stat).replace('.','p')+'.root'),'RECREATE')
	else: outputRfile[iRfile] = TFile(file.replace('.root','_modified.root'),'RECREATE')
	print outputRfile[iRfile]
	for k in tfile[iRfile].GetListOfKeys():
		histName = k.GetName()
		channel = histName[histName.find('is'):histName.find('__')]
		if rebinHists: rebinnedHists[histName]=tfile[iRfile].Get(histName).Rebin(len(xbins[channel])-1,histName,xbins[channel])
		else: rebinnedHists[histName]=tfile[iRfile].Get(histName).Clone()
		if 'sig__mu' in histName and normalizeRENORM: #normalize the renorm/fact shapes to nominal
			renormNomHist = tfile[iRfile].Get(histName[:histName.find('__mu')]).Clone()
			renormSysHist = tfile[iRfile].Get(histName).Clone()
			rebinnedHists[histName].Scale(renormNomHist.Integral()/renormSysHist.Integral())
		if 'sig__pdf' in histName and normalizePDF: #normalize the pdf shapes to nominal
			renormNomHist = tfile[iRfile].Get(histName[:histName.find('__pdf')]).Clone()
			renormSysHist = tfile[iRfile].Get(histName).Clone()
			rebinnedHists[histName].Scale(renormNomHist.Integral()/renormSysHist.Integral())
		if '__pdf' in histName:
			if '__pdf__' not in histName and '__pdfNew__' not in histName: continue
		if not any([item in histName and not removalKeys[item] for item in removalKeys.keys()]):
			rebinnedHists[histName].Write()

	muRUphists = [k.GetName() for k in tfile[iRfile].GetListOfKeys() if 'muR__plus' in k.GetName()]
	for hist in muRUphists:
		newMuRFName = 'muRFcorrdNew'
# 		if 'ewk' in hist: newMuRFName = 'muRFcorrdNewEWK'
# 		if 'top' in hist: newMuRFName = 'muRFcorrdNewTOP'
# 		if 'qcd' in hist: newMuRFName = 'muRFcorrdNewQCD'
# 		if 'sig' in hist: newMuRFName = 'muRFcorrdNewSIG'
		muRFcorrdNewUpHist = rebinnedHists[hist].Clone(hist.replace('muR__plus',newMuRFName+'__plus'))
		muRFcorrdNewDnHist = rebinnedHists[hist].Clone(hist.replace('muR__plus',newMuRFName+'__minus'))
		muRFdecorrdNewUpHist = rebinnedHists[hist].Clone(hist.replace('muR__plus','muRFdecorrdNew__plus'))
		muRFdecorrdNewDnHist = rebinnedHists[hist].Clone(hist.replace('muR__plus','muRFdecorrdNew__minus'))
		histList = [
			rebinnedHists[hist[:hist.find('__mu')]], #nominal
			rebinnedHists[hist], #renormWeights[4]
			rebinnedHists[hist.replace('muR__plus','muR__minus')], #renormWeights[2]
			rebinnedHists[hist.replace('muR__plus','muF__plus')], #renormWeights[1]
			rebinnedHists[hist.replace('muR__plus','muF__minus')], #renormWeights[0]
			rebinnedHists[hist.replace('muR__plus','muRFcorrd__plus')], #renormWeights[5]
			rebinnedHists[hist.replace('muR__plus','muRFcorrd__minus')] #renormWeights[3]
			]
		for ibin in range(1,histList[0].GetNbinsX()+1):
			weightList = [histList[ind].GetBinContent(ibin) for ind in range(len(histList))]
			indCorrdUp = weightList.index(max(weightList))
			indCorrdDn = weightList.index(min(weightList))
			indDeCorrdUp = weightList.index(max(weightList[:-2]))
			indDeCorrdDn = weightList.index(min(weightList[:-2]))

			muRFcorrdNewUpHist.SetBinContent(ibin,histList[indCorrdUp].GetBinContent(ibin))
			muRFcorrdNewDnHist.SetBinContent(ibin,histList[indCorrdDn].GetBinContent(ibin))
			muRFdecorrdNewUpHist.SetBinContent(ibin,histList[indDeCorrdUp].GetBinContent(ibin))
			muRFdecorrdNewDnHist.SetBinContent(ibin,histList[indDeCorrdDn].GetBinContent(ibin))

			muRFcorrdNewUpHist.SetBinError(ibin,histList[indCorrdUp].GetBinError(ibin))
			muRFcorrdNewDnHist.SetBinError(ibin,histList[indCorrdDn].GetBinError(ibin))
			muRFdecorrdNewUpHist.SetBinError(ibin,histList[indDeCorrdUp].GetBinError(ibin))
			muRFdecorrdNewDnHist.SetBinError(ibin,histList[indDeCorrdDn].GetBinError(ibin))
		if 'sig__mu' in hist and normalizeRENORM: #normalize the renorm/fact shapes to nominal
			renormNomHist = tfile[iRfile].Get(hist[:hist.find('__mu')]).Clone()
			muRFcorrdNewUpHist.Scale(renormNomHist.Integral()/muRFcorrdNewUpHist.Integral())
			muRFcorrdNewDnHist.Scale(renormNomHist.Integral()/muRFcorrdNewDnHist.Integral())
			muRFdecorrdNewUpHist.Scale(renormNomHist.Integral()/muRFdecorrdNewUpHist.Integral())
			muRFdecorrdNewDnHist.Scale(renormNomHist.Integral()/muRFdecorrdNewDnHist.Integral())
		muRFcorrdNewUpHist.Write()
		muRFcorrdNewDnHist.Write()
		muRFdecorrdNewUpHist.Write()
		muRFdecorrdNewDnHist.Write()

	pdfUphists = [k.GetName() for k in tfile[iRfile].GetListOfKeys() if 'pdf0' in k.GetName()]
	for hist in pdfUphists:
		newPDFName = 'pdfNew'
# 		if 'ewk' in hist: newPDFName = 'pdfNewEWK'
# 		if 'top' in hist: newPDFName = 'pdfNewTOP'
# 		if 'qcd' in hist: newPDFName = 'pdfNewQCD'
# 		if 'sig' in hist: newPDFName = 'pdfNewSIG'
		pdfNewUpHist = rebinnedHists[hist].Clone(hist.replace('pdf0',newPDFName+'__plus'))
		pdfNewDnHist = rebinnedHists[hist].Clone(hist.replace('pdf0',newPDFName+'__minus'))
		for ibin in range(1,pdfNewUpHist.GetNbinsX()+1):
			weightList = [rebinnedHists[hist.replace('pdf0','pdf'+str(pdfInd))].GetBinContent(ibin) for pdfInd in range(100)]
			indPDFUp = sorted(range(len(weightList)), key=lambda k: weightList[k])[83]
			indPDFDn = sorted(range(len(weightList)), key=lambda k: weightList[k])[15]
			pdfNewUpHist.SetBinContent(ibin,rebinnedHists[hist.replace('pdf0','pdf'+str(indPDFUp))].GetBinContent(ibin))
			pdfNewDnHist.SetBinContent(ibin,rebinnedHists[hist.replace('pdf0','pdf'+str(indPDFDn))].GetBinContent(ibin))
			pdfNewUpHist.SetBinError(ibin,rebinnedHists[hist.replace('pdf0','pdf'+str(indPDFUp))].GetBinError(ibin))
			pdfNewDnHist.SetBinError(ibin,rebinnedHists[hist.replace('pdf0','pdf'+str(indPDFDn))].GetBinError(ibin))
		if 'sig__pdf' in hist and normalizePDF: #normalize the renorm/fact shapes to nominal
			renormNomHist = tfile[iRfile].Get(hist[:hist.find('__pdf')]).Clone()
			pdfNewUpHist.Scale(renormNomHist.Integral()/pdfNewUpHist.Integral())
			pdfNewDnHist.Scale(renormNomHist.Integral()/pdfNewDnHist.Integral())
		pdfNewUpHist.Write()
		pdfNewDnHist.Write()

	outputRfile[iRfile].Close()
	tfile[iRfile].Close()
 	iRfile+=1

print "Total root files modified:", iRfile




