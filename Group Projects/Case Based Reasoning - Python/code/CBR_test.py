import CBR as cbr
import numpy as np
import os
import sys

# if a feature is categorical the value is 1
is_categorical = np.array([1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0])

# the weight of each feature to compute similarity
weights = np.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 20, 1, 1, 1, 1, 1, 1, 1, 20, 1, 1, 1])

test_data = cbr.read_from_file('test.csv')
n_samples_test = np.shape(test_data)[0]
n_columns_test = np.shape(test_data)[1]
test_features = test_data[:, 0: n_columns_test-1]
test_prices = test_data[:, n_columns_test-1].astype('float')
predicted_prices = np.zeros([n_samples_test])

alpha = 3 # to be used in retain function.


# read training samples from file.
# read the data once, and keep it in memory after we update
data = cbr.read_from_file('train.csv')
for i in range(0, n_samples_test):

    n_samples_train = np.shape(data)[0]
    n_columns_train = np.shape(data)[1]

    train_samples = data[:, 0: n_columns_train-1]
    train_prices = data[:, n_columns_train-1]

    test_sample = test_features[i]
    train_plus_test = np.vstack([train_samples, test_sample])

    # preprocess test and train together
    train_plus_test_std = cbr.pre_process(train_plus_test, is_categorical)
    train_samples_std = train_plus_test_std[0:n_samples_train, :]
    test_sample_std = train_plus_test_std[n_samples_train, :]

    # RETRIEVE PHASE
    # uses k similars to predict the price
    k = 5
    k_similars, min_distances = cbr.retrieve_similars(test_sample_std, train_samples_std, is_categorical, weights, k)

    # REUSE PHASE
    # for reuse phase in CBR, we take the average of the most similar cases.
    avg_price = round(np.sum(train_prices[k_similars].astype('float') * (1 / np.array(min_distances))) / np.sum( 1 / np.array(min_distances)), 2)
    # avg_price = np.mean(train_prices[k_similars].astype('float'))
    predicted_prices[i] = avg_price

    # RETAIN PHASE
    # the new test sample is added to the case base if the minimum distance is bigger than the value alpha
    # i.e. it seems to be a new case which is different enough than the existing ones
    data = cbr.retain(data, test_sample, avg_price, min_distances,alpha)


avg_error = cbr.find_average_error(test_prices, predicted_prices)

print "The average error for test samples is: " + str(avg_error)

"""
We can now write the updated case base to a new file
"""
n_samples_train = np.shape(data)[0]
# removing old train2.csv to write the updated one.
os.remove('train2.csv')
for i in range(0,n_samples_train):
    cbr.write_to_file('train2.csv', data[i,:])