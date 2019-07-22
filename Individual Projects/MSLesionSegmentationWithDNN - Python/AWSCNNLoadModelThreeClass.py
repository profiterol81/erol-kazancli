import numpy as np
import tensorflow as tf
import DataCollectionWithIndex as dc
import os
from scipy import ndimage

# tissue codes
whiteMatterTissue = [2, 41, 77, 78, 79, 251, 252, 253, 254, 255]
grayMatterTissue = [9, 10, 11, 12, 13, 17, 18, 26, 48, 49, 50, 51, 52, 53, 54, 58, 28, 60]

cubeSize = 11 # patch size
classNumber = 3 # number of classes

data_path_test = os.path.join(os.path.dirname(__file__), 'DataMRITestNew') # path of the MRI images to be tested
path_model = os.path.join(os.path.dirname(__file__), 'model') # path of the saved model

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

    total_true_pos = 0
    total_false_pos = 0
    total_false_neg = 0

    for subject in subjects:

        a = "\nSubject: " + subject
        print a
        outputFile.write(a)

        data_ST_T1, data_ST_T2, tissue, data_Lesion = dc.extract_files(data_path_test, subject)

        data_lesion_cert = np.zeros(data_Lesion.shape)

        zDim = np.shape(data_ST_T1)[2]

        batchSize = 600

        for sliceNum in range(cubeSize + 1, zDim - cubeSize - 1):
            testFramesT1, testFramesT2, testLocations, indicesPos = dc.retrieve_samples(data_ST_T1, data_ST_T2, tissue, data_Lesion, cubeSize, classNumber, sliceNum)

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
                    indices = indicesPos[start_batch:end_batch, :]

                    [pred_y, y_prob] = sess.run([prediction, probs], feed_dict={
                        x_T1:testFramesT1[start_batch:end_batch, :], x_T2:testFramesT2[start_batch:end_batch, :], x_locations:testLocations[start_batch:end_batch, :], keep_prob: 1.0, phase_train: False})

                    y_prob = y_prob[:, 1]
                    temp = np.logical_or(pred_y == 2, pred_y == 2)
                    temp = temp.astype(int)
                    for index in indices[temp == 1]: data_lesion_cert[index[0], index[1], index[2]] = 1

        num_false_pos = np.sum(np.logical_and(data_Lesion == 0, data_lesion_cert == 1))
        num_false_neg = np.sum(np.logical_and(data_Lesion == 1, data_lesion_cert == 0))
        num_true_pos = np.sum(np.logical_and(data_Lesion == 1, data_lesion_cert == 1))
        pos_acc = num_true_pos / np.sum(data_Lesion)


        a = "\ntrue pos:" + str(num_true_pos)
        print a

        a = "\nfalse pos:" + str(num_false_pos)
        print a

        a = "\nfalse neg:" + str(num_false_neg)
        print a

        a = "\npos acc:" + str(pos_acc)
        print a

        total_lesion_found = num_true_pos + num_false_pos
        total_lesion = num_true_pos + num_false_neg
        vd = float(total_lesion_found - total_lesion) / total_lesion
        fpr = float(num_false_pos) / total_lesion_found
        ppv = float(num_true_pos) / total_lesion_found
        tpr = float(num_true_pos) / total_lesion

        a = "\nVD:" + str(vd)
        print a
        outputFile.write(a)

        a = "\nTotal TPR:" + str(tpr)
        print a
        outputFile.write(a)

        a = "\nFPR:" + str(fpr)
        print a
        outputFile.write(a)

        a = "\nPPV:" + str(ppv)
        print a
        outputFile.write(a)

        labeled_lesions, num_lesions = ndimage.label(data_Lesion, structure=s)
        labeled_lesions_found, num_lesions_found = ndimage.label(data_lesion_cert, structure=s)

        lesions_coincided = np.unique(labeled_lesions[data_lesion_cert == 1])

        a = "\nNum of lesions:" + str(num_lesions)
        print a
        outputFile.write(a)

        a = "\nNum of lesions found:" + str(num_lesions_found)
        print a
        outputFile.write(a)

        a = "\nNum of lesions coincided:" + str(len(lesions_coincided))
        print a
        outputFile.write(a)

        total_true_pos += num_true_pos
        total_false_pos += num_false_pos
        total_false_neg += num_false_neg

        dc.save_cert_lesion_file(data_path_test, subject, data_lesion_cert, False)

        dice_score = float(2 * num_true_pos) / (num_false_pos + num_false_neg + 2 * num_true_pos)
        jaccard = float(num_true_pos) / (num_true_pos + num_false_neg + num_false_pos)

        a = "\nDice score:" + str(dice_score)
        print a
        outputFile.write(a)
        a = "\nJaccard score:" + str(jaccard)
        print a
        outputFile.write(a)

    dice_score = float(2 * total_true_pos) / (total_false_pos + total_false_neg + 2 * total_true_pos)
    jaccard = float(total_true_pos) / (total_true_pos + total_false_neg + total_false_pos)

    a = "\nTotal Dice score:" + str(dice_score)
    print a
    outputFile.write(a)
    a = "\nTotal Jaccard score:" + str(jaccard)
    print a
    outputFile.write(a)

    total_lesion_found = total_true_pos + total_false_pos
    total_lesion = total_true_pos + total_false_neg
    vd = float(total_lesion_found - total_lesion) / total_lesion
    tpr = float(total_true_pos) / total_lesion
    fpr = float(total_false_pos) / total_lesion_found
    ppv = float(total_true_pos) / total_lesion_found

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

    outputFile.flush()
