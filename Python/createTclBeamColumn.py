# -*- coding: utf-8 -*-
"""
/*---------------------------------------------------------------*
| This script is used to create tcl files for beam-column model. |
|                                                                |
| Author: Charles Wang,  UC Berkeley c_w@berkeley.edu            |
|                                                                |
| Date:   01/09/2019                                             |
*---------------------------------------------------------------*/
"""

from collections import namedtuple
import json
from pprint import pprint
from math import floor
import os
from subprocess import call
from shutil import copyfile



TclBuilder = '../Cpp/TclBuilder/TclBuilder'
algoPath = 'CyclicSolutionAlgorithm.tcl'
dataDir = '../Data/ConcreteShearWallBeamcolumn/For AI-M/'


'''
testName = 'MassoneWP5'
nInt = 9
BIMName = os.path.join(dataDir, testName,'RCWall_'+testName+'_BIM.json')
EVTName = os.path.join(dataDir, testName,'RCWall_'+testName+'_EVT.json')
EDPName = os.path.join(dataDir, testName,'RCWall_'+testName+'_EDP.json')
tclDirName = os.path.join(dataDir, testName,"nInt"+str(nInt))
SAMName = os.path.join(dataDir, testName,'RCWall_'+testName+'nInt'+str(nInt)+'_SAM.json')
call([TclBuilder,BIMName,SAMName,EVTName,EDPName,tclDirName])
copyfile(algoPath, os.path.join(tclDirName,'CyclicSolutionAlgorithm.tcl'))
#print(os.path.join(tclDirName,'CyclicSolutionAlgorithm.tcl'))
#print([TclBuilder,BIMName,SAMName,EVTName,EDPName,tclDirName])
exit()
'''


for thisdir in os.listdir(dataDir):
    testName = thisdir

    BIMName = os.path.join(dataDir, testName,'RCWall_'+testName+'_BIM.json')
    EVTName = os.path.join(dataDir, testName,'RCWall_'+testName+'_EVT.json')
    EDPName = os.path.join(dataDir, testName,'RCWall_'+testName+'_EDP.json')
    
    for nInt in [5,7,9]:
        tclDirName = os.path.join(dataDir, testName,"nInt"+str(nInt))
        SAMName = os.path.join(dataDir, testName,'RCWall_'+testName+'nInt'+str(nInt)+'_SAM.json')
        print(tclDirName)
        #call(['rm',os.path.join(dataDir, testName,'nInt'+str(nInt))])
        #print(os.path.join(dataDir, testName,'nInt'+str(nInt)))
        #call([TclBuilder,BIMName,SAMName,EVTName,EDPName,tclDirName])
        #copyfile(algoPath, os.path.join(tclDirName,'CyclicSolutionAlgorithm.tcl'))
        
        try:
            call([TclBuilder,BIMName,SAMName,EVTName,EDPName,tclDirName])
            copyfile(algoPath, os.path.join(tclDirName,'CyclicSolutionAlgorithm.tcl'))
        except:
            print(tclDirName)
            #exit()
        
      

            