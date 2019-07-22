import numpy as np
import tensorflow as tf
import DataCollectionWithIndex as dc
import os
import re

whiteMatterTissue = [2, 41, 77, 78, 79, 251, 252, 253, 254, 255]
grayMatterTissue = [9, 10, 11, 12, 13, 17, 18, 26, 48, 49, 50, 51, 52, 53, 54, 58, 28, 60]

number_of_train_files = 19
cubeSize = 11 # patch size
classNumber = 2 # number of classes

data_path_train = os.path.join(os.path.dirname(__file__), 'DataMRITrain')
data_path_test = os.path.join(os.path.dirname(__file__), 'DataMRITestNew')
log_path_model = os.path.join(os.path.dirname(__file__), 'model_with_loc_11')

extension = "_stage2"

outputFile = open('output.txt', 'a')

total_true_pos = 0
total_false_pos = 0
total_true_neg = 0
total_false_neg = 0

with tf.Session() as sess:
    saver = tf.train.import_meta_graph(log_path_model + '/my-model.meta')
    saver.restore(sess, log_path_model + '/my-model')
    g = tf.get_default_graph()
    accuracy = g.get_tensor_by_name("accuracy:0")
    x_T1 = g.get_tensor_by_name("x_T1:0")
    x_T2 = g.get_tensor_by_name("x_T2:0")
    y_ = g.get_tensor_by_name("y_:0")
    x_locations = g.get_tensor_by_name("x_locations:0")
    keep_prob = g.get_tensor_by_name("keep_prob:0")
    phase_train = g.get_tensor_by_name("phase_train:0")
    y_conv = g.get_collection("y_conv:0")
    cross_entropy = g.get_tensor_by_name("cross_entropy:0")
    prediction = g.get_tensor_by_name("prediction:0")
    probs = g.get_tensor_by_name("probs:0")

    for num in range(1, number_of_train_files + 1):
        data_path = data_path_train + "/DataTrain" + str(num)
        # data_path = data_path_validation + "/DataValidation" + str(num)

        subjects = [s for s in os.listdir(data_path) if not re.match(r'.*\.npz', s)]
        if '.DS_Store' in subjects:
            subjects.remove('.DS_Store')

        for subject in subjects:

            wrong_prediction = np.array([]).reshape(0,3)

            a = "\nSubject: " + subject
            print a
            outputFile.write(a)

            data_ST_T1, data_ST_T2, tissue, data_Lesion = dc.extract_files(data_path, subject)

            zDim = np.shape(data_ST_T1)[2]

            batchSize = 600

            testFramesT1, testFramesT2, testLocations, testLabels, indicesPos = dc.retrieve_positive_samples_for_dice(data_ST_T1, data_ST_T2, tissue, data_Lesion, cubeSize, classNumber)

            numSamples = np.shape(testFramesT1)[0]

            numBatches = numSamples / batchSize

            totalAccuracy = 0
            totalSample = 0
            totalAccuracyCert = 0
            for batch in range(0, numBatches + 1):
                start_batch = batch * batchSize
                end_batch = (batch + 1) * batchSize
                if end_batch > numSamples:
                    end_batch = numSamples
                if start_batch == end_batch:
                    break

                indices = indicesPos[start_batch:end_batch, :]

                [test_accuracy, pred_y, y_prob, y_prob2] = sess.run([accuracy, prediction, probs, cross_entropy], feed_dict={
                    x_T1:testFramesT1[start_batch:end_batch, :], x_T2:testFramesT2[start_batch:end_batch, :], y_:testLabels[start_batch:end_batch, :], x_locations:testLocations[start_batch:end_batch, :], keep_prob: 1.0, phase_train: False})

                y_prob = y_prob[:, 1]
                temp = np.logical_and(pred_y == 1, y_prob >= 0.5)
                temp = temp.astype(int)

                totalAccuracy = totalAccuracy + test_accuracy * (end_batch - start_batch)
                totalSample = totalSample +  (end_batch - start_batch)

            true_pos = totalAccuracy
            false_neg = totalSample - totalAccuracy

            a = "\nTotal Test Pos Acc.:" + repr(totalAccuracy / totalSample)
            print a
            outputFile.write(a)

            totalAccuracy = 0
            totalSample = 0
            totalAccuracyCert = 0
            false_neg_cert = 0
            for sliceNum in range(cubeSize + 1, zDim - cubeSize - 1):
                testFramesT1, testFramesT2, testLocations, testLabels, indicesNeg = dc.retrieve_negative_samples_on_border(data_ST_T1, data_ST_T2, tissue, data_Lesion, cubeSize, classNumber, sliceNum)

                numSamples = np.shape(testFramesT1)[0]

                numBatches = numSamples / batchSize

                if numSamples != 0:
                    for batch in range(0, numBatches + 1):
                        start_batch = batch * batchSize
                        end_batch = (batch + 1) * batchSize
                        if end_batch > numSamples:
                            end_batch = numSamples
                        if start_batch == end_batch:
                            break
                        indices = indicesNeg[start_batch:end_batch, :]

                        [test_accuracy, pred_y, y_prob, y_prob2] = sess.run([accuracy, prediction, probs, cross_entropy], feed_dict={
                            x_T1:testFramesT1[start_batch:end_batch, :], x_T2:testFramesT2[start_batch:end_batch, :], y_:testLabels[start_batch:end_batch, :], x_locations:testLocations[start_batch:end_batch, :], keep_prob: 1.0, phase_train: False})
                        y_prob = y_prob[:, 1]
                        temp = np.logical_and(pred_y == 1, y_prob >= 0.5)
                        temp = temp.astype(int)

                        wrong_prediction = np.append(wrong_prediction, indices[temp == 1], axis=0)

                        temp = np.logical_and(pred_y == 0, y_prob >= 0)
                        temp = temp.astype(int)
                        size_w_p = wrong_prediction.shape[0]
                        indices = np.random.permutation(indices)

                        wrong_prediction = np.append(wrong_prediction, indices[temp == 1][0:size_w_p, :], axis=0)

                        totalAccuracy = totalAccuracy + test_accuracy * (end_batch - start_batch)
                        totalSample = totalSample +  (end_batch - start_batch)

            a = "\nTotal Test Neg Acc.:" + repr(totalAccuracy / totalSample)
            print a
            outputFile.write(a)

            outputFile.flush()

            fileFrames = os.path.join(data_path, subject + extension)
            np.savez_compressed(fileFrames, pos=indicesPos, neg=wrong_prediction)
