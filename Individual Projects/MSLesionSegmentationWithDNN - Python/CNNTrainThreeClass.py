import numpy as np
import tensorflow as tf
import DeepLearning as dl
import DataCollectionWithIndex as dc
import os

# the general parameters of the CNN
cubeSize = 11 # 19
dataSize1d = cubeSize**3
kernelSizeLevelOne = 4
kernelSizeLevelTwo = 3
numberOfInputChannelLevelOne = 1
numberOfOutputChannelLevelOne = 60
numberOfOutputChannelLevelTwo = 60
resultCubeSizeOfConvolutions = 1 # (((cubeSize - kernelSizeLevelOne + 1) / 2) - kernelSizeLevelTwo + 1) / 2
classNumber = 2
multiLayerPerceptronSize = 200
frame_size = cubeSize**3

data_path_train = os.path.join(os.path.dirname(__file__), 'DataMRITrain')
data_path_validation = os.path.join(os.path.dirname(__file__), 'DataMRIValidation')
log_path_train = os.path.join(os.path.dirname(__file__), 'train')
log_path_test = os.path.join(os.path.dirname(__file__), 'test')
log_path_model = os.path.join(os.path.dirname(__file__), 'model')
log_path_model2 = os.path.join(os.path.dirname(__file__), 'model2')

number_of_train_files = 15
number_of_validation_files = 1
margin = 18
only_white_matter = False
augmented = False
extension = "three_class2.npz"
extensionVal = "three_class2.npz"

testNeg, testBorder, testPos = dc.retrieve_three_class_validation_samples_from_file(data_path_validation + "/DataValidation1", cubeSize, classNumber, extensionVal)

number_of_samples = 800

# choose test as many as number_of_samples test samples
testPosT1, testPosT2, testPosLocations, testPosLabels  = dc.take_test_samples_three_class(testPos, frame_size, number_of_samples, 2)
testBorderT1, testBorderT2, testBorderLocations, testBorderLabels  = dc.take_test_samples_three_class(testBorder, frame_size, number_of_samples, 1)
testNegT1, testNegT2, testNegLocations, testNegLabels  = dc.take_test_samples_three_class(testNeg, frame_size, number_of_samples, 0)

sess = tf.InteractiveSession()

x_T1 = tf.placeholder(tf.float32, shape=[None, dataSize1d], name="x_T1")
x_T2 = tf.placeholder(tf.float32, shape=[None, dataSize1d], name="x_T2")
y_ = tf.placeholder(tf.float32, shape=[None, classNumber], name="y_")
x_locations = tf.placeholder(tf.float32, shape=[None, 3], name="x_locations")
keep_prob = tf.placeholder(tf.float32, name="keep_prob")
phase_train = tf.placeholder(tf.bool, name="phase_train")

# first convolutional layer: kernelSizeLevelOne**3 input, numberOfOutputChannelLevelOne output channels
x_T1_3D = tf.reshape(x_T1, [-1,cubeSize,cubeSize,cubeSize,1])
h_pool1_T1_drop = dl.convolutional_layer_with_pooling_3D(x_T1_3D, kernelSizeLevelOne, numberOfInputChannelLevelOne, numberOfOutputChannelLevelOne, phase_train, keep_prob)
h_pool2_T1_drop = dl.convolutional_layer_with_pooling_3D(h_pool1_T1_drop, kernelSizeLevelTwo, numberOfOutputChannelLevelOne, numberOfOutputChannelLevelTwo, phase_train, keep_prob)

# second convolutional layer
x_T2_3D = tf.reshape(x_T2, [-1,cubeSize,cubeSize,cubeSize,1])
h_pool1_T2_drop = dl.convolutional_layer_with_pooling_3D(x_T2_3D, kernelSizeLevelOne, numberOfInputChannelLevelOne, numberOfOutputChannelLevelOne, phase_train, keep_prob)
h_pool2_T2_drop = dl.convolutional_layer_with_pooling_3D(h_pool1_T2_drop, kernelSizeLevelTwo, numberOfOutputChannelLevelOne, numberOfOutputChannelLevelTwo, phase_train, keep_prob)

# fully-connected layer
h_pool2_flat_T1 = tf.reshape(h_pool2_T1_drop, [-1, resultCubeSizeOfConvolutions**3 * numberOfOutputChannelLevelTwo])
h_pool2_flat_T2 = tf.reshape(h_pool2_T2_drop, [-1, resultCubeSizeOfConvolutions**3 * numberOfOutputChannelLevelTwo])
h_pool2_flat = tf.concat(1, [h_pool2_flat_T1, h_pool2_flat_T2])
h_pool2_flat_wl = tf.concat(1, [h_pool2_flat, x_locations])
h_pool2_flat_wl_drop = tf.nn.dropout(h_pool2_flat_wl, keep_prob)

input_size = resultCubeSizeOfConvolutions**3 * numberOfOutputChannelLevelTwo * 2 + 3
h_fc1_drop = dl.fully_connected_layer(h_pool2_flat_wl_drop, input_size, multiLayerPerceptronSize, phase_train, keep_prob)

# multi layer perceptron
y_conv = dl.multi_layer_perceptron(h_fc1_drop, multiLayerPerceptronSize, classNumber, phase_train, keep_prob)

probs = tf.nn.softmax(y_conv, "probs")
tf.add_to_collection("y_conv", y_conv)
cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(y_conv, y_), name="cross_entropy")
train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)
correct_prediction = tf.equal(tf.argmax(y_conv,1), tf.argmax(y_,1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32), name="accuracy")

tf.scalar_summary('accuracy', accuracy)
merged = tf.merge_all_summaries()

train_writer = tf.train.SummaryWriter(log_path_train, sess.graph)
prediction = tf.argmax(y_conv, 1, name="prediction")
sess.run(tf.initialize_all_variables())

batchSize = 128
outputFile = open('output.txt', 'a')
numEpochs = 200
saver = tf.train.Saver()

best_accuracy = 0
for m in range(0, number_of_train_files * numEpochs):

    epoch = m / number_of_train_files
    print "epoch: " + str(epoch)
    file_number = (m % number_of_train_files) + 1

    trainFramesT1 = []
    trainFramesT2 = []
    trainLocations = []
    trainLabels = []
    trainFramesT1, trainFramesT2, trainLocations, trainLabels = dc.retrieve_three_class_samples_from_file(data_path_train + "/DataTrain" + str(file_number), cubeSize, classNumber, extension)

    trainFramesT1 = trainFramesT1[0:20000, :]
    trainFramesT2 = trainFramesT2[0:20000, :]
    trainLocations = trainLocations[0:20000, :]
    trainLabels = trainLabels[0:20000, :]

    sizeTrain = np.shape(trainFramesT1)[0] / batchSize

    a = "\nepoch:" + str(epoch) + "-" + str(file_number)
    outputFile.write(a)

    for i in range(0, sizeTrain):

        trainBatchT1 = trainFramesT1[i*batchSize:i*batchSize+batchSize, :]
        trainBatchT2 = trainFramesT2[i*batchSize:i*batchSize+batchSize, :]
        labelBatch = trainLabels[i*batchSize:i*batchSize+batchSize, :]
        trainLocationsBatch = trainLocations[i*batchSize:i*batchSize+batchSize, :]

        _, summary, accuracy_tr = sess.run([train_step, merged, accuracy], feed_dict={x_T1: trainBatchT1, x_T2: trainBatchT2, y_: labelBatch, x_locations:trainLocationsBatch, keep_prob: 0.5, phase_train: True})
        train_writer.add_summary(summary, i)

        if i % 200 == 0:
            a = "\nBatch Acc.:" + repr(accuracy_tr)
            outputFile.write(a)

            step = i / 200
            print "step: " + str(step)

            test_pos_accuracy = accuracy.eval(feed_dict={
              x_T1:testPosT1, x_T2:testPosT2, y_:testPosLabels, x_locations:testPosLocations, keep_prob: 1.0, phase_train: False})

            test_neg_accuracy = accuracy.eval(feed_dict={
              x_T1:testNegT1, x_T2:testNegT2, y_:testNegLabels, x_locations:testNegLocations, keep_prob: 1.0, phase_train: False})

            test_border_accuracy = accuracy.eval(feed_dict={
              x_T1:testBorderT1, x_T2:testBorderT2, y_:testBorderLabels, x_locations:testBorderLocations, keep_prob: 1.0, phase_train: False})

            test_accuracy = (test_pos_accuracy + test_neg_accuracy + test_border_accuracy) / 3

            if test_accuracy > best_accuracy:
                a = "epoch:" + str(epoch) + "-" + str(file_number) + " best_accuracy:" + str(test_accuracy)
                outputFile.write(a)
                print a
                best_accuracy = test_accuracy
                saver.save(sess, log_path_model + '/my-model')

                a = "\nTest Pos:" + repr(test_pos_accuracy)
                outputFile.write(a)
                a = "\nTest Border:" + repr(test_border_accuracy)
                outputFile.write(a)
                a = "\nTest Neg:" + repr(test_neg_accuracy)
                outputFile.write(a)
                a = "\nTest Acc.:" + repr(test_accuracy)
                outputFile.write(a)
                a = "\nBatch Acc.:" + repr(accuracy_tr)
                outputFile.write(a)

    outputFile.flush()

saver.save(sess, log_path_model2 + '/my-model')