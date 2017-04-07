"""
Author : Erol Kazancli
Date : 15 January 2016
Finds the average error for a given hiddenLayer size using 5-fold cross validation
"""

import numpy as np
import math
from NeuralNetwork import NeuralNetwork
import CsvReader

# Finds the average error for a given hiddenLayer size using 5-fold cross validation
def TestModel(normData, Y, survival, hiddenNeuronCount):

    inputs = normData

    sumError = 0

    bestInitialW1 = 0
    bestInitialW2 = 0

    numericColumns = np.array([5, 6, 7, 9])
    catgColumns = np.array([2, 4, 11])

    for cross_val in range(1, 6):

        # The cut point between training and validation data, the test data is seperated beforehand n the Analysis.py
        # and is not included in the 5-fold analysis
        cutPoint = (len(inputs) * 4) / 5
        train = inputs[:cutPoint, :]
        validation = inputs[cutPoint:, :]

        survivalTrain = survival[:cutPoint]
        survivalVal = survival[cutPoint:]
        trainY = Y[:cutPoint, :]
        validationY = Y[cutPoint:, :]

        trainNorm = CsvReader.Normalize(train, survivalTrain, numericColumns, catgColumns, 'train')
        validationNorm = CsvReader.Normalize(validation, survivalVal, numericColumns, catgColumns, 'test')

        # Here I put the validation data on top of the train son that in the next iteration a different set is chosen for train
        # an validation
        inputs = np.concatenate([validation, train])
        Y = np.concatenate([validationY, trainY])
        survival = np.concatenate([survivalVal, survivalTrain])

        inputLayerSize = len(trainNorm.T)
        hiddenLayerSize = hiddenNeuronCount
        outputLayerSize = 1

        # The weights are randomly initialized
        initialW1 = (2 * np.random.random((inputLayerSize, hiddenLayerSize)) - 1) / math.sqrt(inputLayerSize)
        initialW2 = (2 * np.random.random((hiddenLayerSize + 1, outputLayerSize)) - 1) / math.sqrt(hiddenLayerSize) # + 1 refers to bias term

        net = NeuralNetwork(inputLayerSize, hiddenNeuronCount, outputLayerSize, initialW1, initialW2)

        numSamples = len(trainNorm)
        minErrorVal = 1000
        for i in range(0, 150000):

            a2, z2, a3, yEst, signEst = net.forward(trainNorm)

            YEST = net.findY(validationNorm)
            errorVal = net.getError(validationY, YEST)
            if errorVal < minErrorVal:
                minErrorVal = errorVal
                bestInitialW1 = initialW1
                bestInitialW2 = initialW2
#            This par is used to see the progress and can be uncommented if desired
#            if (i <> 0) and (i % 10000 == 0):
#                error = net.getError(trainY, signEst)
#                print "Error Train:" + str(error)
#                print "Error Validation:" + str(errorVal)

            # the derivatives are found
            der1, der2 = net.getDerivatives(a2, z2, a3, trainNorm, trainY, yEst)

            # Weights are updated
            net.updateWeights(der1, der2, numSamples)

        print "Cross Validation Number:" + str(cross_val)
        print "Min Validation Error Value:" + str(minErrorVal)
        sumError = sumError + minErrorVal

    avgError = sumError/5
    print "Avg Error Value for " + str(hiddenNeuronCount) + " Hidden Neurons :" + str(avgError)

    return avgError, bestInitialW1, bestInitialW2


