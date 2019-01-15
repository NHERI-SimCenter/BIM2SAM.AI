# -*- coding: utf-8 -*-
"""
Created on Jan 9, 2019

@author: Charles Wang
"""

from __future__ import absolute_import, division, print_function
import pathlib
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
print(tf.__version__)

# fix random seed for reproducibility
tf.set_random_seed(1234)


# define paths
dataset_path = '../../Data/NeuralNets/DatasetV1_ContinuumWall.txt'
label_path = '../../Data/NeuralNets/Labels_ContinuumWall.txt'



# load data
column_names = ['height', 'length', 'thickness', 'E', 'fc'] 
raw_dataset = pd.read_csv(dataset_path, names=column_names,
                      na_values = "?", comment='\t',
                      sep=",", skipinitialspace=True)
dataset = raw_dataset.copy()
print(dataset.tail())

# load labels:   column_names= ['Name', Ap', 'An', 'Bn', 'beta', 'N']
raw_labelset = pd.read_csv(label_path, 
                      na_values = "?", comment='\t',
                      sep=",", skipinitialspace=True)
labelset = raw_labelset[['Ap', 'An', 'Bn', 'beta','N']].copy()
print(labelset.tail())


# merge label into dataset
dataset = pd.concat([dataset, labelset], axis=1, join='inner')
print(dataset.tail())


# Split data into train and test
train_dataset = dataset.sample(frac=0.8,random_state=0)
test_dataset = dataset.drop(train_dataset.index)

# Inspect data
# joint distributions
sns.pairplot(train_dataset[['height', 'length', 'thickness', 'E', 'fc']], diag_kind="kde")

# statistics
train_stats = train_dataset.describe()
train_stats.pop("Ap")
train_stats.pop("An")
train_stats.pop("Bn")
train_stats.pop("beta")
train_stats.pop("N")
train_stats = train_stats.transpose()
print(train_stats)
store = pd.HDFStore('../../Data/NeuralNets/DataStats_ContinuumWall_V1.h5')
store['stats'] =  train_stats



# Split features from labels
train_labels = train_dataset[['Ap','An', 'Bn', 'beta','N']].copy()
train_dataset = train_dataset.drop(['Ap','An', 'Bn', 'beta','N'], axis=1)
test_labels = test_dataset[['Ap','An', 'Bn', 'beta','N']].copy()
test_dataset = test_dataset.drop(['Ap','An', 'Bn', 'beta','N'], axis=1)



# Normalize data
def norm(x):
  return (x - train_stats['mean']) / train_stats['std']
normed_train_data = norm(train_dataset)
normed_test_data = norm(test_dataset)

print(train_stats)
exit()


# Build the model
def build_model():
  model = keras.Sequential([
    layers.Dense(256, activation=tf.nn.relu, input_shape=[len(train_dataset.keys())]),
    layers.Dense(64, activation=tf.nn.relu),
    layers.Dense(64, activation=tf.nn.relu),
    layers.Dense(64, activation=tf.nn.relu),
    layers.Dense(5)
  ])
  #optimizer = tf.train.RMSPropOptimizer(0.001)
  optimizer = tf.train.AdamOptimizer(1e-4)
  model.compile(loss='mse', optimizer=optimizer, metrics=['mae', 'mse'])
  return model



# Training
# Display training progress by printing a single dot for each completed epoch
class PrintDot(keras.callbacks.Callback):
  def on_epoch_end(self, epoch, logs):
    if epoch % 100 == 0: 
      print(epoch)
    print('.', end='')

def plot_history(history):
  hist = pd.DataFrame(history.history)
  hist['epoch'] = history.epoch
  
  plt.figure()
  plt.xlabel('Epoch')
  plt.ylabel('Mean Abs Error [Ap+An+Bn+beta+N]')
  plt.plot(hist['epoch'], hist['mean_absolute_error'],
           label='Train Error')
  plt.plot(hist['epoch'], hist['val_mean_absolute_error'],
           label = 'Val Error')
  plt.legend()
  #plt.ylim([0,1])
  '''
  plt.figure()
  plt.xlabel('Epoch')
  plt.ylabel('Mean Square Error [$Ap^2$]')
  plt.plot(hist['epoch'], hist['mean_squared_error'],
           label='Train Error')

  plt.plot(hist['epoch'], hist['val_mean_squared_error'],
           label = 'Val Error')
  plt.legend()
  #plt.ylim([0,1])
  '''
  #plt.show()

EPOCHS = 5000

'''
# no early stop
model = build_model()
model.summary()
history = model.fit(
  normed_train_data, train_labels,
  epochs=EPOCHS, validation_split = 0.2, verbose=0,
  callbacks=[PrintDot()])
hist = pd.DataFrame(history.history)
hist['epoch'] = history.epoch
print('\n')
print(hist.tail())
plot_history(history)
'''


model = build_model()
model.summary()
# The patience parameter is the amount of epochs to check for improvement
early_stop = keras.callbacks.EarlyStopping(monitor='val_loss', patience=10)
history = model.fit(normed_train_data, train_labels, epochs=EPOCHS,
                    validation_split = 0.2, verbose=0, callbacks=[early_stop, PrintDot()])
hist = pd.DataFrame(history.history)
hist['epoch'] = history.epoch
print('\n')
print(hist.tail())
plot_history(history)


loss, mae, mse = model.evaluate(normed_test_data, test_labels, verbose=0)
print("Testing set Mean Abs Error: {:5.2f} Ap+An+Bn+beta+N".format(mae))



# serialize model to JSON
model_json = model.to_json()
with open("../../Data/NeuralNets/NNModel_ContinuumWall_V1.json", "w") as json_file:
    json_file.write(model_json)
# serialize weights to HDF5
model.save_weights("../../Data/NeuralNets/NNModel_ContinuumWall_V1.h5")
print("Saved model to disk")



# Predict
test_predictions = model.predict(normed_test_data).flatten()

plt.figure(figsize=(800,40))
plt.subplot(2,5,1)
trueValues = test_labels['Ap']
predictValues = test_predictions[0::5]
plt.scatter(trueValues, predictValues)
plt.xlabel('True Values [Ap]')
plt.ylabel('Predictions [Ap]')
plt.axis('equal')
plt.axis('square')
plt.xlim([0,plt.xlim()[1]])
plt.ylim([0,plt.ylim()[1]])
_ = plt.plot([-100, 100], [-100, 100])

plt.subplot(2,5,6)
error = predictValues - trueValues
plt.hist(error, bins = 25)
plt.xlabel("Prediction Error [Ap]")
_ = plt.ylabel("Count")

plt.subplot(2,5,2)
trueValues = test_labels['An']
predictValues = test_predictions[1::5]
plt.scatter(trueValues, predictValues)
plt.xlabel('True Values [An]')
plt.ylabel('Predictions [An]')
plt.axis('equal')
plt.axis('square')
plt.xlim([0,plt.xlim()[1]])
plt.ylim([0,plt.ylim()[1]])
_ = plt.plot([-100, 100], [-100, 100])

plt.subplot(2,5,7)
error = predictValues - trueValues
plt.hist(error, bins = 25)
plt.xlabel("Prediction Error [Ap]")
_ = plt.ylabel("Count")

plt.subplot(2,5,3)
trueValues = test_labels['Bn']
predictValues = test_predictions[2::5]
plt.scatter(trueValues, predictValues)
plt.xlabel('True Values [Bn]')
plt.ylabel('Predictions [Bn]')
plt.axis('equal')
plt.axis('square')
plt.xlim([0,plt.xlim()[1]])
plt.ylim([0,plt.ylim()[1]])
_ = plt.plot([-100, 100], [-100, 100])

plt.subplot(2,5,8)
error = predictValues - trueValues
plt.hist(error, bins = 25)
plt.xlabel("Prediction Error [Bn]")
_ = plt.ylabel("Count")


plt.subplot(2,5,4)
trueValues = test_labels['beta']
predictValues = test_predictions[3::5]
plt.scatter(trueValues, predictValues)
plt.xlabel('True Values [beta]')
plt.ylabel('Predictions [beta]')
plt.axis('equal')
plt.axis('square')
plt.xlim([0,plt.xlim()[1]])
plt.ylim([0,plt.ylim()[1]])
_ = plt.plot([-100, 100], [-100, 100])

plt.subplot(2,5,9)
error = predictValues - trueValues
plt.hist(error, bins = 25)
plt.xlabel("Prediction Error [beta]")
_ = plt.ylabel("Count")


plt.subplot(2,5,5)
trueValues = test_labels['N']
predictValues = test_predictions[4::5]
plt.scatter(trueValues, predictValues)
plt.xlabel('True Values [N]')
plt.ylabel('Predictions [N]')
plt.axis('equal')
plt.axis('square')
plt.xlim([0,plt.xlim()[1]])
plt.ylim([0,plt.ylim()[1]])
_ = plt.plot([-100, 100], [-100, 100])

plt.subplot(2,5,10)
error = predictValues - trueValues
plt.hist(error, bins = 25)
plt.xlabel("Prediction Error [N]")
_ = plt.ylabel("Count")


plt.show()