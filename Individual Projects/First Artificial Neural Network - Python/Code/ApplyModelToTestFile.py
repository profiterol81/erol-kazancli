"""
Author : Erol Kazancli
Date : 15 January 2016
# This python file is used to apply the found found model to the test file provided by the Kaggle website
"""

import CsvReader
import numpy as np
from NeuralNetwork import NeuralNetwork

# the positions of the relevant columns are different for this test file than the training file, because the
# survival data is missing in this file

numericColumns = np.array([4, 5, 6, 8])
catgColumns = np.array([1, 3, 10])

data, passengerId = CsvReader.ReadTest('test.csv')

# normalization and augmentation is done here
normData = CsvReader.Normalize(data, [], numericColumns, catgColumns, 'test')

test = normData

# These are the model parameters found in the previous analyses
ModelW1 = [[ -7.90312017e-02,  -8.95565346e-01,   2.56510735e-02,   5.68696002e-01,
    2.85748020e-01,  -8.19381794e-01,   1.84040103e-01,  -1.67757164e-01],
 [  4.70377383e-01,   4.60085493e-02,   7.18045464e-01,  -9.54051724e-02,
    1.17614505e+00,   1.54165806e-01,   1.17567018e-01,   1.10612275e-01],
 [ -7.50645357e-01,  -3.52766680e-02,  -9.49039039e-01,   1.67508218e+00,
   -8.34351277e-01,  -1.96771399e+00,  -5.24032627e+00,   5.83126988e+00],
 [ -1.45333164e-01,   3.78798201e-01,  -1.89696748e-01,   4.75974471e-02,
   -3.70584605e-01,   1.12345557e-01,  -1.51321334e+00,   6.67613204e-02],
 [ -1.80012177e-03,   4.10745746e-01,  -2.31367246e-02,  -3.26691482e-01,
   -6.96735457e-02,   5.96241853e-01,   2.29394369e-01,   3.98713611e-02],
 [ -3.41671020e-01,   6.49306147e-01,  -2.30505163e-01,   7.61946723e-01,
   -4.25729149e-01,  -8.40998296e-01,  -1.26154041e-01,   1.32513813e-01],
 [  3.85878105e-02,   5.57104999e-01,   1.69293299e-01,  -8.35194023e-02,
   -1.30184921e-01,   3.51023631e-01,   2.61018639e-01,  -4.40401974e-01],
 [  3.25586491e-01,  -2.18095299e+00,   3.19580652e-01,   2.37180710e-02,
    5.48612091e-01,  -2.05613601e-01,   5.27455571e-01,  -3.31418352e-01],
 [ -1.39800787e-01,   1.68263901e+00,  -2.44425349e-01,   2.33337191e-01,
    6.55858892e-02,  -7.54131582e-01,  -1.48549100e-01,   1.06192454e-01],
 [  4.31780153e-01,  -2.36066493e+00,   3.15724793e-01,   1.55821193e-01,
    3.39548082e-01,   2.52372690e-01,   4.44027285e-01,  -4.44634988e-01],
 [ -3.36795953e-02,   6.87017148e-02,  -2.23655559e-01,   1.66364499e-01,
    2.27357457e-01,   1.94678939e-01,   8.39772456e-02,   9.84844525e-02],
 [ -1.68324664e-02,  -8.57590950e-01,   1.31285549e-01,   1.00748634e-01,
    9.45109186e-02,  -3.25042009e-01,   3.24816323e-01,  -1.35624877e-01],
 [  1.33552378e-01,   1.01647469e+00,   6.44903365e-02,  -1.43185009e-01,
   -4.70824633e-02,   1.02138448e-01,   6.09807787e-01,  -2.98223818e-01],
 [  2.99143914e-03,  -1.16158428e+00,   2.48361811e-02,   1.75176167e-01,
    5.06174213e-01,  -6.63362402e-01,  -2.66413234e-01,   1.34115039e-01]]

ModelW2 = [[ 0.08329099],
 [-1.15726993],
 [ 4.34172651],
 [-1.52589129],
 [ 2.13551256],
 [-1.74475049],
 [-2.56949073],
 [ 3.74974147],
 [-4.04887917]]

inputLayerSize = len(test.T)
hiddenLayerSize = 8 # This is the optimum hidden layer size found in the 5-fold analysis
outputLayerSize = 1
initialW1 = np.asarray(ModelW1)
initialW2 = np.asarray(ModelW2)

net = NeuralNetwork(inputLayerSize, hiddenLayerSize, outputLayerSize, initialW1, initialW2)

errorTEST = 0
YESTTest = net.findY(test)

CsvReader.WriteTest('testResults.csv', passengerId, YESTTest)




