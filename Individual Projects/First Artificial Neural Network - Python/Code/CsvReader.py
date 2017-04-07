"""
Author : Erol Kazancli
Date : 12 December 2015
This file is an adapted version of the csvReader file provided by the kaggle website
New methods like normalize and write are added, the other methods have been adapted
"""
import csv as csv
import numpy as np

# This method reads from a training file and returns the attribute data and the survival information
def Read(fileName):

    csv_file_object = csv.reader(open(fileName, 'rb')) 	    # Load in the csv file
    header = csv_file_object.next() 						# Skip the fist line as it is a header
    data=[] 												# Create a variable to hold the data

    for row in csv_file_object: 							# Skip through each row in the csv file,
        data.append(row[0:]) 								# adding each row to the data variable
    data = np.array(data) 									# Then convert from a list to an array.

    survival = data[0::,1].astype(np.float)                 # Get survival column

    return data, survival

# This method reads from a test file and returns the attribute data and the passengerId
def ReadTest(fileName):

    csv_file_object = csv.reader(open(fileName, 'rb')) 	    # Load in the csv file
    header = csv_file_object.next() 						# Skip the fist line as it is a header
    data=[] 												# Create a variable to hold the data

    for row in csv_file_object: 							# Skip through each row in the csv file,
        data.append(row[0:]) 								# adding each row to the data variable
    data = np.array(data) 									# Then convert from a list to an array.

    passengerId = data[0::,0].astype(np.float)                 # Get survival column

    return data, passengerId

# This method writes the results of the classification to a file
def WriteTest(fileName, passengerId, YESTTest):
    predictions_file = open(fileName, "wb")
    predictions_file_object = csv.writer(predictions_file)
    predictions_file_object.writerow(["PassengerId", "Survived"])	# write the column headers
    for i in range(0, len(passengerId)):									# For each row in test file,
        predictions_file_object.writerow([str(int(passengerId[i])), str(int(YESTTest[i][0]))])			# write the PassengerId, and predict 1
    predictions_file.close()

# This method normalizes the data, the method slightly changes for test and training data, since
# the survival information is missing in the test file and cannot be used to fill null values
def Normalize(data, survival, numericColumns, catgColumns, trainOrTest):

    normData = np.empty((4, data.shape[0]), float)          # Initialize normalized data
    j = 0
    tData = data.T

    # Processing numeric values
    for colNum in numericColumns:
        column = tData[colNum]
        column[column == ''] = '0'
        newColumn = column.astype(np.float)

        # For training data fill the null values with the inclass mean
        if trainOrTest == 'train':
            newColumn[np.logical_and((newColumn == 0), (survival.T == 1))] = np.mean(newColumn[np.logical_and((newColumn <> 0), (survival.T == 1))])  # mean replacement for empty values
            newColumn[np.logical_and((newColumn == 0), (survival.T == 0))] = np.mean(newColumn[np.logical_and((newColumn <> 0), (survival.T == 0))])  # mean replacement for empty values
        # For test data fill the null values with the mean, because we do not have the survival info
        else:
            newColumn[(newColumn == 0)] = np.mean(newColumn[(newColumn <> 0)])  # mean replacement for empty values for test data

        # Apply normalization
        mean = np.mean(newColumn, axis = 0)
        cov = np.std(newColumn, axis=0)

        norm = [(float(i) - mean)/cov for i in newColumn]
        normData[j] = norm

        j = j + 1

    # Processing categorical data
    for colNum in catgColumns:      # categorical data is handled
        column = tData[colNum]
        u = np.unique(column)

        # This part was necessary because in the train file there was a null value which was represented by a dummy variable
        # This null was missing in the test file and the portion of test in the training, so to equalize the number of
        # attributes a null is added, but this dummy part has all zeros for the test normalized data
        if (colNum == 10 or colNum == 11) and '' not in u:
            u = np.insert(u, 0, '', axis=None)
        # Here a dummy variable is added for each unique value or for null values
        if u.shape[0] <= 10:  # if the number of unique values greater than 10 discard
            k = 0
            for t in u:
                newColumn = np.copy(column)
                newColumn[column <> t] = 0;
                newColumn[column == t] = 1;
                normData = np.vstack([normData, newColumn])
                k = k + 1

    # Augmentation is done here
    normData = np.concatenate([np.ones((1,len(normData.T))),normData]).T

    x = np.array(normData, dtype='|S4')
    normData = x.astype(np.float)

    return normData


