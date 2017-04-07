"""
Author :
Date :
"""
import csv as csv
import numpy as np
import math

def read_from_file(fileName):
    """
    This method reads from a file
    inputs :
        - fileName: name of the file to be written
    outputs:
        - data: our case base
    """

    csv_file_object = csv.reader(open(fileName, 'rb')) 	    # Load in the csv file
    # header = csv_file_object.next() 						# Skip the fist line as it is a header
    data=[] 												# Create a variable to hold the data

    for row in csv_file_object: 							# Skip through each row in the csv file,
        data.append(row[0:]) 								# adding each row to the data variable
    data = np.array(data) 									# Then convert from a list to an array.

    return data

def write_to_file(fileName, test_sample):
    """
    This method writes the results of the prediction to a file
    inputs :
        - fileName: name of the file to be written
        - test_sample: test_sample to be written

    """
    predictions_file = open(fileName, "a")
    predictions_file_object = csv.writer(predictions_file)
    predictions_file_object.writerow(test_sample)
    predictions_file.close()


def pre_process(data, is_categorical):
    """
    This method standardizes the data
    inputs :
        - data: our case base
        - is_categorical: the information for a feature of whether it is categorical or not

    outputs:
        - stdData: standardized data
    """
    j = 0

    stdData = np.array([]).reshape(data.shape[0],0)
    n_features = np.shape(data)[1]

    # Processing numeric values
    for colNum in range(0, n_features):
        if is_categorical[colNum] == 0:
            column = data[:, colNum]
            # column[column == '?'] = '0'
            newColumn = np.copy(column)

            # For training data fill the null values with the inclass mean

            newColumn[(newColumn == '?')] = np.mean(newColumn[(newColumn <> '?')].astype(np.float))  # mean replacement for empty values for test data

            newColumn  = newColumn.astype(np.float)
            # Apply standardization
            mean = np.mean(newColumn, axis = 0)
            cov = np.std(newColumn, axis=0)

            norm = np.round([(float(i) - mean)/cov for i in newColumn], 2)
            if colNum == 0:
                stdData = norm
            else:
                stdData = np.vstack([stdData, norm])
        else:   # categorical data is handled
            column = data[:, colNum]
            if colNum == 0:
                stdData = column
            else:
                stdData = np.vstack([stdData, column])

    return stdData.T

def find_difference(sample1, sample2, is_categorical):

    """
    This function calculates the difference between two samples
    inputs :
        - sample1: the instance 1
        - sample2: the instance 2
        - is_categorical: the information for a feature of whether it is categorical or not

    outputs:
        - diff: the difference between two samples
    """
    diff = 0

    n_features = np.shape(sample1)[0]
    for colNum in range(0, n_features):
        if is_categorical[colNum] == 0:
            diff = diff + (float(sample1[colNum]) - float(sample2[colNum])) ** 2
        else:
            if (sample1[colNum] != sample2[colNum]):
                diff = diff + 1

    return diff


def find_weighted_difference(sample1, sample2, is_categorical, weights):

    """
    This function calculates the difference between two samples with weights for each feature
    inputs :
        - sample1: the instance 1
        - sample2: the instance 2
        - is_categorical: the information for a feature of whether it is categorical or not
        - weights: weight of each feature

    outputs:
        - diff: the difference between two samples
    """
    diff = 0

    n_features = np.shape(sample1)[0]
    for colNum in range(0, n_features):
        if is_categorical[colNum] == 0:
            diff = diff + int(weights[colNum]) * (float(sample1[colNum]) - float(sample2[colNum])) ** 2
        else:
            if (sample1[colNum] != sample2[colNum]):
                diff = diff + int(weights[colNum])

    return diff

def retrieve_similars(test_sample, train_samples, is_categorical, weights, n_similars):

    """
    This function checks n_similars number of most similar examples
    inputs :
        - test_sample: the new instance
        - train_samples: the instance in the case base that is compared
        - is_categorical: the information for a feature of whether it is categorical or not
        - weights: weight of each feature
        - n_similars: how many samples to fetch as most similars

    outputs:
        - min_distance_samples: the most similar samples
        - min_distances: the distances from the most similar samples
    """

    n_samples_train = np.shape(train_samples)[0]
    min_distance_samples = list()
    min_distances = list()
    max_distance = 0
    max_distance_sample = -1

    for i in range (0, n_samples_train):
        train_sample = train_samples[i, :]

        # distance = find_difference(test_sample, train_sample, is_categorical)
        distance = find_weighted_difference(test_sample, train_sample, is_categorical, weights)
        if len(min_distance_samples) < n_similars:

            min_distance_samples.append(i)
            min_distances.append(distance)

            if distance > max_distance:
                max_distance = distance
                max_distance_sample = i
        else:
            if distance < max_distance:
                min_distance_samples.append(i)
                min_distances.append(distance)
                index_del = min_distance_samples.index(max_distance_sample)
                del min_distance_samples[index_del]
                del min_distances[index_del]
                max_distance = max(min_distances)
                index_max = min_distances.index(max_distance)
                max_distance_sample = min_distance_samples[index_max]

    return min_distance_samples,min_distances

def retain(data,test_sample,avg_price,min_distances,alpha):
    """
    This function checks if the similarity of the new instance is less than
    the the threshold alpha, if it is, it adds the new test instances with
    the avg_price appended.
    inputs :
        - data: our case base
        - test_sample: the new instance features
        - avg_price: the predicted price by the algorithm.
        - alpha: used for similarity threshold
       
    outputs:
        - data: the case base, may or may not be updated based on the 
            predicted similarity and calculations in this function.    
    """
     

    most_similar = np.min(min_distances)
    if most_similar > alpha:
        test_sample = np.append(test_sample, avg_price)
        data = np.vstack([data, test_sample])

    return data

def find_average_error(real_prices, predicted_prices):
    """
    This function calculates the average error in the predictions we make and the real errors
    inputs :
        - real_prices: the real prices
        - predicted_prices: the predicted prices

    outputs:
        - error: the average error between real and predicted prices
    """

    return np.sum(np.fabs(real_prices - predicted_prices))/ np.shape(real_prices)[0]
