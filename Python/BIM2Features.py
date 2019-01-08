from BIM import BIM
import numpy as np

# define BIM file path
BIMFileName = "../Data/features2SAM/BIM.json"
# define dimension of random projection
nDimRandomProj = 512


# get features from BIM
bimModel = BIM(BIMFileName)
features = bimModel.getFeatures()





