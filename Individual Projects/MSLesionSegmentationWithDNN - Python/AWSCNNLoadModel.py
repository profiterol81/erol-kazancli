import numpy as np
import tensorflow as tf
import DataCollectionWithIndex as dc
import os
from scipy import ndimage

# tissue codes
whiteMatterTissue = [2, 41, 77, 78, 79, 251, 252, 253, 254, 255]
grayMatterTissue = [9, 10, 11, 12, 13, 17, 18, 26, 48, 49, 50, 51, 52, 53, 54, 58, 28, 60]

cubeSize = 11 # patch size
classNumber = 2  # number of classes

data_path_test = os.path.join(os.path.dirname(__file__), 'DataMRITestNew') # path of the MRI images to be tested
path_model = os.path.join(os.path.dirname(__file__), 'model_with_loc_11') # path of the saved model

# for connected components
s = np.ones([3,3,3])

# filename for results
outputFile = open('output.txt', 'a')

# subject names(folder name) to be tested
subjects = ['013MSVIS', '050MSVIS', '082MSVIS', '083MSVIS', '084MSVIS', '088MSVIS', '090MSVIS', '091MSVIS', '092MSVIS']

total_true_pos = 0
total_false_pos = 0
total_true_neg = 0
total_false_neg = 0

with tf.Session() as sess:

    # loading the model
    saver = tf.train.import_meta_graph(path_model + '/my-model.meta')
    saver.restore(sess, path_model + '/my-model')
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

    batchSize = 600
    for subject in subjects:

        a = "\nSubject: " + subject
        print a
        outputFile.write(a)

        data_ST_T1, data_ST_T2, tissue, data_Lesion = dc.extract_files(data_path_test, subject)

        data_lesion_found = np.zeros(data_Lesion.shape)
        data_lesion_prob = np.zeros(data_Lesion.shape)
        data_lesion_cert = np.zeros(data_Lesion.shape)

        zDim = np.shape(data_ST_T1)[2]

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

            indices = indicesPos[start_batch:end_batch, :]

            [test_accuracy, pred_y, y_prob, y_prob2] = sess.run([accuracy, prediction, probs, cross_entropy], feed_dict={
                x_T1:testFramesT1[start_batch:end_batch, :], x_T2:testFramesT2[start_batch:end_batch, :], y_:testLabels[start_batch:end_batch, :], x_locations:testLocations[start_batch:end_batch, :], keep_prob: 1.0, phase_train: False})

            y_prob = y_prob[:, 1]
            temp = np.logical_and(pred_y == 1, y_prob >= 0.5)
            temp = temp.astype(int)
            for index in indices[temp == 1]: data_lesion_found[index[0], index[1], index[2]] = 1
            test_accuracy_cert = float(np.sum(temp)) / (end_batch - start_batch)

            temp = np.logical_and(pred_y == 1, y_prob <= 1)
            temp = temp.astype(int)
            for index in indices[temp == 1]: data_lesion_prob[index[0], index[1], index[2]] = 1

            totalAccuracyCert = totalAccuracyCert + test_accuracy_cert * (end_batch - start_batch)
            totalAccuracy = totalAccuracy + test_accuracy * (end_batch - start_batch)
            totalSample = totalSample +  (end_batch - start_batch)

        true_pos = totalAccuracy
        false_neg = totalSample - totalAccuracy
        a = "\nTotal pos:" + str(totalSample)
        print a
        outputFile.write(a)
        a = "\nTrue pos:" + str(true_pos)
        print a
        outputFile.write(a)
        a = "\nFalse neg:" + str(false_neg)
        print a
        outputFile.write(a)

        a = "\nTotal Test Pos Acc.:" + repr(totalAccuracy / totalSample)
        print a
        outputFile.write(a)

        total_true_pos += true_pos
        total_false_neg += false_neg

        totalAccuracy = 0
        totalSample = 0
        totalAccuracyCert = 0
        false_neg_cert = 0
        for sliceNum in range(cubeSize + 1, zDim - cubeSize - 1):
            testFramesT1, testFramesT2, testLocations, testLabels, indicesNeg = dc.retrieve_negative_samples_for_dice(data_ST_T1, data_ST_T2, tissue, data_Lesion, cubeSize, classNumber, sliceNum)

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
                    for index in indices[temp == 1]: data_lesion_found[index[0], index[1], index[2]] = 1

                    temp = np.logical_and(pred_y == 1, y_prob <= 1)
                    temp = temp.astype(int)
                    for index in indices[temp == 1]: data_lesion_prob[index[0], index[1], index[2]] = 1

                    totalAccuracyCert = totalAccuracyCert + test_accuracy_cert * (end_batch - start_batch)
                    totalAccuracy = totalAccuracy + test_accuracy * (end_batch - start_batch)
                    totalSample = totalSample +  (end_batch - start_batch)

        true_neg = totalAccuracy
        false_pos = totalSample - totalAccuracy

        labeled_lesions, num_lesions = ndimage.label(data_Lesion, structure=s)
        labeled_lesions_found, num_lesions_found = ndimage.label(data_lesion_found, structure=s)

        lesions_coincided = np.unique(labeled_lesions[data_lesion_found == 1])

        dc.save_found_lesion_file(data_path_test, subject, data_lesion_found, data_lesion_prob, data_Lesion)

        a = "\nNum of lesions:" + str(num_lesions)
        print a
        outputFile.write(a)

        a = "\nNum of lesions found:" + str(num_lesions_found)
        print a
        outputFile.write(a)

        a = "\nNum of lesions coincided:" + str(len(lesions_coincided))
        print a
        outputFile.write(a)

        a = "\nTotal neg:" + str(totalSample)
        print a
        outputFile.write(a)
        a = "\nTrue neg:" + str(true_neg)
        print a
        outputFile.write(a)
        a = "\nFalse pos:" + str(false_pos)
        print a
        outputFile.write(a)

        a = "\nTotal Test Neg Acc.:" + repr(totalAccuracy / totalSample)
        print a
        outputFile.write(a)

        total_false_pos += false_pos
        total_true_neg += true_neg

        dice_score = (2 * true_pos) / (false_neg + false_pos + 2 * true_pos)
        jaccard = true_pos / (true_pos + false_neg + false_pos)

        a = "\nDice score:" + str(dice_score)
        print a
        outputFile.write(a)
        a = "\nJaccard score:" + str(jaccard)
        print a
        outputFile.write(a)

        total_lesion_found = true_pos + false_pos
        total_lesion = true_pos + false_neg
        vd = (total_lesion_found - total_lesion) / total_lesion
        fpr = false_pos / total_lesion_found
        ppv = true_pos / total_lesion_found

        a = "\nVD:" + str(vd)
        print a
        outputFile.write(a)

        a = "\nFPR:" + str(fpr)
        print a
        outputFile.write(a)

        a = "\nPPV:" + str(ppv)
        print a
        outputFile.write(a)

        outputFile.flush()

    a = "\nTotal True Pos:" + str(total_true_pos)
    print a
    outputFile.write(a)
    a = "\nTotal True Neg:" + str(total_true_neg)
    print a
    outputFile.write(a)
    a = "\nTotal False Pos:" + str(total_false_pos)
    print a
    outputFile.write(a)
    a = "\nTotal False Neg:" + str(total_false_neg)
    print a
    outputFile.write(a)

    total_dice_score = (2 * total_true_pos) / (total_false_neg + total_false_pos + 2 * total_true_pos)
    total_jaccard = total_true_pos / (total_true_pos + total_false_neg + total_false_pos)

    a = "\nTotal Dice score:" + str(total_dice_score)
    print a
    outputFile.write(a)
    a = "\nTotal Jaccard score:" + str(total_jaccard)
    print a
    outputFile.write(a)

    total_lesion_found = total_true_pos + total_false_pos
    total_lesion = total_true_pos + total_false_neg
    vd = (total_lesion_found - total_lesion) / total_lesion
    tpr = total_true_pos / total_lesion
    fpr = total_false_pos / total_lesion_found
    ppv = total_true_pos / total_lesion_found

    a = "\nTotal VD:" + str(vd)
    print a
    outputFile.write(a)

    a = "\nTotal TPR:" + str(tpr)
    print a
    outputFile.write(a)

    a = "\nTotal FPR:" + str(fpr)
    print a
    outputFile.write(a)

    a = "\nTotal PPV:" + str(ppv)
    print a
    outputFile.write(a)