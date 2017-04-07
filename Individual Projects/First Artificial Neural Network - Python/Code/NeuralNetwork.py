"""
Author : Erol Kazancli
Date : 30 December 2015
This is the neural network class
"""

import numpy as np

class NeuralNetwork():

    #  initialization of the neural network
    def __init__(self, inputLayerSize, hiddenSize, outputSize, initialW1, initialW2):
        self.inputLayerSize = inputLayerSize # the bias is included beforehand
        self.outputLayerSize = outputSize
        self.hiddenLayerSize = hiddenSize
        self.p = 1
        self.Rate = 0.15

        self.W1 = initialW1
        self.W2 = initialW2

    #  the outputs of all neurons are found using the current weights and the inputs
    def forward(self, x):
        a2 = np.dot(x, self.W1)
        z2 = self.sigmoid(a2, self.p)
        z2 = np.concatenate([np.ones((1,len(z2))),z2.T]).T  # bias term is added in the hidden layer
        a3 = np.dot(z2, self.W2)
        yEst = self.sigmoid(a3, self.p)
        signEst = np.sign(yEst - 0.5)
        signEst[signEst == -1] = 0
        return a2, z2, a3, yEst, signEst


    #  the estimates are found using the current weights and the inputs
    def findY(self, X):
        a2 = np.dot(X, self.W1)
        z2 = self.sigmoid(a2, self.p)
        z2 = np.concatenate([np.ones((1,len(z2))),z2.T]).T
        a3 = np.dot(z2, self.W2)
        yEst = self.sigmoid(a3, self.p)
        signEst = np.sign(yEst - 0.5)
        signEst[signEst == -1] = 0;
        return signEst

    #  sigmoid function
    def sigmoid(self, a, p):
        return 1 / (1 + np.exp(-a / p))

    #  the derivatives are calculated
    def getDerivatives(self, a2, z2, a3, x, y, yEst):

        delta2 = -np.multiply(np.multiply((y - yEst), yEst), (1 - yEst))
        derivative2 = np.dot(z2.T, delta2)

        delta1 = np.multiply(np.multiply(np.dot(delta2, self.W2.T), z2), 1-z2)

        delta1 = np.delete(delta1, 0, 1)  # remove bias term in the hidden layer to backpropagate
        derivative1 = np.dot(x.T, delta1)

        return derivative1, derivative2

    #  the weights are updated with batch learning
    def updateWeights(self, derivative1, derivative2, numSamples):
        self.W1 = self.W1 - (self.Rate * derivative1) / numSamples
        self.W2 = self.W2 - self.Rate * derivative2 / numSamples
        return self.W1, self.W2

    #  the error value is calculated
    def getError(self, Y, YEst):

        error = np.dot((Y - YEst).T, (Y - YEst))
        return error/len(Y)

