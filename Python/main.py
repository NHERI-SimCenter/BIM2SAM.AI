from BIM2SAM import BIM2SAM
from BIM import BIM
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import model_from_json


# ------------------------------
# BIM2SAM demo
# ------------------------------

# define BIM and SAM file path
BIMFileName = "../Data/features2SAM/BIM.json"
SAMFileName = "../Data/features2SAM/SAM_Continuum.json"
# define dimension of random projection
nDimRandomProj = 512


# get features from BIM
bimModel = BIM(BIMFileName)
# detailed features
features = bimModel.getFeatures()
# or simple version features [h w t E fpc]
featuresSimple = []
featuresSimple.append(np.asarray(bimModel.getSimpleFeatures()))
featuresSimple = np.asarray(featuresSimple)
featuresSimple = pd.DataFrame(featuresSimple, columns=['height', 'length', 'thickness', 'E', 'fc'] )
# normalize the inputs
store = pd.HDFStore('../Data/NeuralNets/DataStats_ContinuumWall_V1.h5')
dataStats = store['stats']
def norm(x):
  return (x - dataStats['mean']) / dataStats['std']
featuresSimple = norm(featuresSimple)


# load json and create model
json_file = open('../Data/NeuralNets/NNModel_ContinuumWall_V1.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
# load weights into new model
loaded_model.load_weights('../Data/NeuralNets/NNModel_ContinuumWall_V1.h5')
print("Loaded model from disk")


# evaluate loaded model on test data
optimizer = tf.train.AdamOptimizer(1e-4)
loaded_model.compile(loss='mse', optimizer=optimizer, metrics=['mae', 'mse'])
Ap, An, Bn, beta, N = loaded_model.predict(featuresSimple)[0]
N = int(round(N))
pars = [N, beta, An, Ap, Bn]
print(pars)


# perform BIM2SAM
BIM2SAM(BIMFileName, SAMFileName, 'continuum', pars)


