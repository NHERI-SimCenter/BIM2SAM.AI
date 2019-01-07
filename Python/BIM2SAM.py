import json
from pprint import pprint
from subprocess import call
import os
from BeamColumnSAM import BeamColumnBIM, BeamColumnSAM


class BIM2SAM:
    """A calss generating SAM from BIM and given parameetrs"""
             
    def __init__(self, BIMFileName,SAMFileName,SAMType,pars):
        '''
        BIMFileName (string): BIM file
        SAMFileName (string): SAM file
        SAMType (string): continuum, beamcolumn
        pars (list): parameters, [N,beta,An,Ap,Bn] (continuum), [nInt] (beamcolumn)
        '''
        if SAMType == 'continuum':
            if not os.path.isfile('../Cpp/createSAM'):
                # build the createSAM excutable
                call(["cd ../Cpp && sh run && cd ../Python"], shell=True)
            if len(pars) != 5:
                print('The number of parameters for continuum model most be 5.')
                exit()
            N,beta,An,Ap,Bn = pars
            call(["../Cpp/createSAM", BIMFileName, SAMFileName,str(N), "0", str(beta), str(An), str(Ap), str(Bn)])
            
        elif SAMType == 'beamcolumn':
            if len(pars) != 1:
                print('The number of parameters for beamcolumn model most be 1.')
                exit()
            nInt = pars[0]
            SAMModel = BeamColumnSAM()
            SAMModel.readBIM(BIMFileName)
            SAMModel.setMesh(32, 32, 2, 2, 4, 4, nInt)
            SAMModel.createSAM()
            SAMModel.writeSAM(SAMFileName)
            del(SAMModel)
        else:
            print('The model type should be "continuum" or "beamcolumn".')
            exit()
            

