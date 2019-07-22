import DataCollectionWithIndex as dc
import os

number_of_train_files = 15
number_of_validation_files = 1
margin = 18
only_white_matter = False
augmented = False
extension = "_stage2.npz"
extensionVal = "int.npz"
number_of_classes = 2

data_path_train = os.path.join(os.path.dirname(__file__), 'DataMRITrain')
data_path_validation = os.path.join(os.path.dirname(__file__), 'DataMRIValidation')

# the files for training and validation are prepared here to later be used in the training phase
dc.prepare_validation_files(number_of_validation_files, data_path_validation, number_of_classes, margin, only_white_matter, augmented, extension)
dc.prepare_training_files(number_of_train_files, data_path_train, number_of_classes, margin, only_white_matter, augmented, extension)
