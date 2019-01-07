from collections import namedtuple
import json
from pprint import pprint
from math import floor
import os
from subprocess import call
from shutil import copyfile

opensees = '/Users/simcenter/Codes/OpenSees/bin/opensees'
dataDir = '../Data/ConcreteShearWallBeamcolumn/For AI-M/'
currentPath = os.path.dirname(os.path.realpath(__file__))


'''
testName = 'DazioWSH6'
nInt = 5

tclDirName = os.path.join(dataDir, testName,"nInt"+str(nInt))
driver = os.path.join(dataDir, testName,"nInt"+str(nInt),'wallDriver.tcl')
os.chdir(tclDirName)
call([opensees,driver])
os.chdir(currentPath)
print(os.path.dirname(os.path.realpath(__file__)))
exit()
'''



for thisdir in os.listdir(dataDir):
    testName = thisdir

    BIMName = os.path.join(dataDir, testName,'RCWall_'+testName+'_BIM.json')
    EVTName = os.path.join(dataDir, testName,'RCWall_'+testName+'_EVT.json')
    EDPName = os.path.join(dataDir, testName,'RCWall_'+testName+'_EDP.json')
    
    for nInt in [5,7,9]:
        try:
            tclDirName = os.path.join(dataDir, testName,"nInt"+str(nInt))
            driver = os.path.join(dataDir, testName,"nInt"+str(nInt),'wallDriver.tcl')
            os.chdir(tclDirName)
            call([opensees,driver])
            os.chdir(currentPath)
        except:
            print("Do nothing.")
      

            