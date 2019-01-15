# -*- coding: utf-8 -*-
"""
/*------------------------------------------------------*
| This script is a demo for showing how to use the      |
| BIM class to get features.                            |
|                                                       |
| Author: Charles Wang,  UC Berkeley c_w@berkeley.edu   |
|                                                       |
| Date:   01/09/2019                                    |
*------------------------------------------------------*/
"""

from BIM import BIM
import numpy as np
import pandas as pd

# define BIM file path
BIMFileName = "../Data/features2SAM/BIM.json"
# define dimension of random projection
nDimRandomProj = 512


# get features from BIM
bimModel = BIM(BIMFileName)
# detailed features
features = bimModel.getFeatures()
# or simple version features [h w t E fpc]
featuresSimple = bimModel.getSimpleFeatures()



'''
# get features of 51 walls
basedir = "../Data/ConcreteShearWallBeamcolumn/For AI-M/"
label_path = '../Data/NeuralNets/Labels_ContinuumWall.txt'
raw_labelset = pd.read_csv(label_path, na_values = "?", comment='\t',
                      sep=",", skipinitialspace=True)
names = raw_labelset[['Name']].copy()
features = []
featuresSimple = []
for name in names['Name']:
    print(name)
    BIMFile = basedir + name + "/RCWall_" + name + "_BIM.json"
    # get features from BIM
    bimModel = BIM(BIMFile)
    # detailed features
    features.append(bimModel.getFeatures())
    # or simple version features [h w t E fpc]
    featuresSimple.append(bimModel.getSimpleFeatures())

features = np.asarray(features)
featuresSimple = np.asarray(featuresSimple)

featuresSimple = pd.DataFrame(featuresSimple)
featuresSimple.to_csv('../Data/NeuralNets/DatasetV1_ContinuumWall.txt',header=False,index=False)
print(featuresSimple.tail(5))
print(featuresSimple.shape)

features = pd.DataFrame(features)
features.to_csv('../Data/NeuralNets/DatasetV2_ContinuumWall.txt',header=False,index=False)
print(features.tail(5))
print(features.shape)
'''






