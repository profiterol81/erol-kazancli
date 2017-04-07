"""
Author : Erol Kazancli
Date : 15 January 2016
This python file is used to apply 5-fold cross validation to find the optimum hidden layer size
"""
import CsvReader
import ModelTester
import numpy as np

data, survival = CsvReader.Read('train.csv')

Y = np.matrix(survival).T

minErrorVal = 1
bestHiddenCount = 0

cutPoint = (len(data) * 4) / 5

trainAndValidation = data[:cutPoint, :]
trainAndValidationY = Y[:cutPoint, :]
survival = survival[:cutPoint]

chosenW1 = 0
chosenW2 = 0

avgErrors = [0] * 8

i = 0

# Hidden Layer size from 3 to 10 are analyzed
for hiddenNeurons in range(3, 11):

    # Finds the average error for a given hiddenLayer size using 5-fold cross validation
    avgError, bestInitialW1, bestInitialW2 = ModelTester.TestModel(trainAndValidation, trainAndValidationY, survival, hiddenNeurons)

    # the minimum average error is stored and along with it the hiddenlayerSize
    if avgError < minErrorVal:
        minErrorVal = avgError
        bestHiddenCount = hiddenNeurons
        chosenW1 = bestInitialW1
        chosenW2 = bestInitialW2

    avgErrors[i] = avgError
    i = i + 1

print "Best Avg Error Value: " + str(minErrorVal) + "Hidden Neuron Count:" + str(bestHiddenCount)
print "Initial Weights W1:" + str(chosenW1)
print "Initial Weights W2:" + str(chosenW2)