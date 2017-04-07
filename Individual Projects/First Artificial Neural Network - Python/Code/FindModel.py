"""
Author : Erol Kazancli
Date : 15 January 2016
This file is used to find the best model using the architecture found in the previous 5-fold analysis
"""

import CsvReader
import numpy as np
from NeuralNetwork import NeuralNetwork


# the numeric and the categorical columns are identified
numericColumns = np.array([5, 6, 7, 9])
catgColumns = np.array([2, 4, 11])

# data is read from the training file
data, survival = CsvReader.Read('train.csv')
Y = np.matrix(survival).T

# The first cut point, which separates the test portion
cutPoint = (len(data) * 4) / 5

trainAndValidation = data[:cutPoint, :]
trainAndValidationY = Y[:cutPoint, :]
survivalTrainAndVal = survival[:cutPoint]

# test portion will be used after the model parameters are found
test = data[cutPoint:, :]
testY = Y[cutPoint:, :]

# test is normalized without the knowledge of the survival values
test = CsvReader.Normalize(test, [], numericColumns, catgColumns, 'test')

# the second cut point between training and validation, validation will be used to stop training
cutPoint = (len(trainAndValidation) * 4) / 5
train = trainAndValidation[:cutPoint, :]
validation = trainAndValidation[cutPoint:, :]

trainY = trainAndValidationY[:cutPoint, :]
validationY = trainAndValidationY[cutPoint:, :]

survivalTrain = survivalTrainAndVal[:cutPoint]

# normalization and augmentation is done here
# note validation and train are normalized seperately, not to bias the validation
train = CsvReader.Normalize(train, survivalTrain, numericColumns, catgColumns, 'train')
validation = CsvReader.Normalize(validation, [], numericColumns, catgColumns, 'test')

# these are the chosen weights after several random trials, they are thought to be close to a good local minimum
chosenInitW1 = [[ -2.07600134e-01,   4.86911274e-02,  -4.98130411e-02,   2.08534138e-01,
   -7.48333116e-02,  -2.06643522e-01,  -2.30422433e-01,   2.64178942e-02],
 [ -2.19270667e-01,   2.76479621e-03,  -1.77073250e-01,   1.07089699e-01,
    1.82342438e-01,  -1.38983910e-01,  -8.45249864e-02,   7.62467929e-03],
 [  1.35915773e-01,   6.86486890e-02,  -1.03412370e-01,   1.39733072e-01,
   -1.08079980e-01,  -6.19851814e-02,  -2.46670905e-01,   2.33339000e-01],
 [  8.56512654e-02,  -1.57270906e-01,  -1.15103697e-01,   2.13217483e-01,
   -1.31197463e-01,   1.56523676e-01,  -1.73580716e-01,   1.96555701e-01],
 [ -8.61309337e-02,  -2.18711862e-01,  -1.81619855e-01,  -5.45028471e-02,
    1.13125718e-02,   2.61010297e-01,   2.08243058e-01,  -1.65763818e-01],
 [  6.59891080e-02,   1.63487747e-02,   2.28535498e-01,   2.15139316e-01,
   -1.67847480e-01,  -1.79246683e-01,   1.27981967e-01,  -1.84501641e-02],
 [ -2.05239423e-01,   1.24948286e-01,   1.39819418e-01,  -5.65143843e-03,
   -2.50364412e-01,   2.65861558e-01,   1.25415110e-01,  -1.74387142e-01],
 [  3.31846650e-02,  -1.71582431e-01,  -1.85450243e-01,   1.32495650e-01,
    5.03285817e-02,  -1.69464869e-01,  -5.53944471e-03,  -2.52294149e-01],
 [  2.05879578e-02,   7.17513287e-02,   6.03446576e-02,   2.97550852e-02,
    1.98417681e-01,   4.95208700e-02,  -2.32159834e-01,  -1.93517911e-01],
 [  1.42822476e-01,   1.94479226e-01,  -6.45093289e-02,  -7.58565081e-04,
   -1.53865041e-01,   6.14585098e-02,   1.13175483e-01,   4.92504349e-02],
 [ -2.31720218e-02,   4.62428539e-02,  -2.11758313e-01,   1.56564603e-01,
    2.36981230e-01,   2.11441243e-01,   7.00507427e-02,   1.16775360e-01],
 [ -1.92987939e-02,   1.76512329e-01,   7.15332506e-02,  -8.78423798e-02,
   -1.64903036e-02,  -2.63259204e-04,   1.15843690e-01,   1.86755629e-01],
 [  1.54664139e-01,  -6.29961640e-02,   1.10436832e-01,  -1.68149660e-01,
    5.68785231e-02,  -2.23944148e-01,   1.48604190e-01,  -1.63551574e-01],
 [ -1.54730500e-01,  -1.49501371e-01,  -4.87193765e-02,   3.83698639e-02,
    1.43009344e-01,  -6.60825879e-02,   3.22696270e-03,  -1.47053560e-01]]

chosenInitW2 = [[-0.2105125 ],
 [ 0.00820572],
 [ 0.25757586],
 [-0.3363186 ],
 [ 0.2093863 ],
 [-0.21612688],
 [-0.31108313],
 [-0.02554597],
 [ 0.00760433]]


inputLayerSize = len(train.T)
hiddenLayerSize = 8
outputLayerSize = 1
initialW1 = np.asarray(chosenInitW1)
initialW2 = np.asarray(chosenInitW2)

# this par was used to find good initial weights in several trials
# initialW1 = (2 * np.random.random((inputLayerSize, hiddenLayerSize)) - 1) / math.sqrt(inputLayerSize)
# initialW2 = (2 * np.random.random((hiddenLayerSize + 1, outputLayerSize)) - 1) / math.sqrt(hiddenLayerSize) # + 1 refers to bias term

# Neural network is initialized
net = NeuralNetwork(inputLayerSize, hiddenLayerSize, outputLayerSize, initialW1, initialW2)

numSamples = len(train)
errorVal = 0
errorTEST = 0

# 150000 is the maximum epoch number
for i in range(0, 150000):

    a2, z2, a3, yEst, signEst = net.forward(train)

    YEST = net.findY(validation)
    errorVal = net.getError(validationY, YEST)

    # In every 10000th epoch the results are printed to see the progress
    if (i <> 0) and (i % 10000 == 0):
        error = net.getError(trainY, signEst)
        print "Error Train:" + str(error)
        print "Error Validation:" + str(errorVal)

    # Here when the minimum validation error is reached, the model has been found and the test error can be calculated.
    # The reason 0.24 is being used is that it has been found that 0.237 is the min validation error for these initial weights

    if errorVal < 0.24:
        YESTTest = net.findY(test)
        errorTEST = net.getError(testY, YESTTest)
        break

    der1, der2 = net.getDerivatives(a2, z2, a3, train, trainY, yEst)

    ModelW1, ModelW2 = net.updateWeights(der1, der2, numSamples)

print "Model Weights W1:" + str(ModelW1)
print "Model Weights W2:" + str(ModelW2)

# this par was used to find good initial weights
# print "Initial Weights W1:" + str(initialW1)
# print "Initial Weights W2:" + str(initialW2)

print "Test Error:" + str(errorTEST)


