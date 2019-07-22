import numpy as np
import nibabel as nib
import os
import re
import DataSelection as ds

t1_name = '/t1_aligned_brain.nii.gz'
t2_name = '/t2_aligned_brain.nii.gz'
lesion_name = '/lesions_aligned.nii.gz'
tissue_name = '/segmentation_aligned.nii.gz'
lesion_found_name = '/lesions_aligned_found.nii.gz'
lesion_final = "_lesions_final.nii.gz"

whiteMatterTissue = [2, 41, 77, 78, 79, 251, 252, 253, 254, 255]
whiteAndGrayMatterTissue = [2, 41, 77, 78, 79, 251, 252, 253, 254, 255, 9, 10, 11, 12, 13, 17, 18, 26, 48, 49, 50, 51, 52, 53, 54, 58, 28, 60, 1001]

# This function prepares the training samples
# data_path_train: data path
# number_of_classes: how many classes for classification - lesion - non-lesion
# margin: the margin from which to start exploring the mri
# only_white: if only white tissue will be considered
# augmented: if the data will be augmented - not used
def prepare_training_files(number_of_train_files, data_path_train, number_of_classes, margin, only_white_matter, augmented, extension):

    for num in range(1, number_of_train_files + 1):
        data_path = data_path_train + "/DataTrain" + str(num)
        save_training_samples(data_path, margin, only_white_matter, augmented, extension)

# This function prepares the validation samples
# data_path_val: data path
# number_of_classes: how many classes for classification - lesion - non-lesion
# margin: the margin from which to start exploring the mri
# only_white: if only white tissue will be considered
# augmented: if the data will be augmented - not used
def prepare_validation_files(number_of_validation_files, data_path_val, number_of_classes, margin, only_white_matter, augmented, extension):

    for num in range(1, number_of_validation_files + 1):
        data_path = data_path_val + "/DataValidation" + str(num)
        save_four_class_samples(data_path, margin, only_white_matter, augmented, extension)

# This function prepares the 4 class training samples
# data_path_train: data path
# number_of_classes: how many classes for classification - lesion - non-lesion
# margin: the margin from which to start exploring the mri
# only_white: if only white tissue will be considered
# augmented: if the data will be augmented - not used
def prepare_four_class_training_files(number_of_training_files, data_path_val, number_of_classes, margin, only_white_matter, augmented, extension):

    for num in range(1, number_of_training_files + 1):
        data_path = data_path_val + "/DataTrain" + str(num)
        save_four_class_samples(data_path, margin, only_white_matter, augmented, extension)

# This function prepares the 4 class validation samples
# data_path_val: data path
# number_of_classes: how many classes for classification - lesion - non-lesion
# margin: the margin from which to start exploring the mri
# only_white: if only white tissue will be considered
# augmented: if the data will be augmented - not used
def prepare_four_class_validation_files(number_of_validation_files, data_path_val, number_of_classes, margin, only_white_matter, augmented, extension):

    for num in range(1, number_of_validation_files + 1):
        data_path = data_path_val + "/DataTrain" + str(num)
        save_four_class_samples(data_path, margin, only_white_matter, augmented, extension)

# This function prepares the 3 class training samples
# data_path_train: data path
# number_of_classes: how many classes for classification - lesion - non-lesion
# margin: the margin from which to start exploring the mri
# only_white: if only white tissue will be considered
# augmented: if the data will be augmented - not used
def prepare_three_class_training_files(number_of_validation_files, data_path_val, number_of_classes, margin, only_white_matter, augmented, extension):

    for num in range(1, number_of_validation_files + 1):
        data_path = data_path_val + "/DataTrain" + str(num)
        save_three_class_samples(data_path, margin, only_white_matter, augmented, extension)

# This function prepares the 3 class validation samples
# data_path_val: data path
# number_of_classes: how many classes for classification - lesion - non-lesion
# margin: the margin from which to start exploring the mri
# only_white: if only white tissue will be considered
# augmented: if the data will be augmented - not used
def prepare_three_class_validation_files(number_of_validation_files, data_path_val, number_of_classes, margin, only_white_matter, augmented, extension):

    for num in range(1, number_of_validation_files + 1):
        data_path = data_path_val + "/DataValidation" + str(num)
        save_three_class_samples(data_path, margin, only_white_matter, augmented, extension)

# This function seperates validation samples to T1 T2 locations and labels
# test_samples: the patches(T1, T1, location together)
# frame_size: the length of T1 and T2
# number_of_samples: how many samples to select
# class_type: which class type to select
def take_test_samples(test_samples, frame_size, number_of_samples, class_type):

    if class_type == 0:
         testLabels = np.tile([1, 0], (number_of_samples, 1))
    else:
         testLabels = np.tile([0, 1], (number_of_samples, 1))

    testT1 = test_samples[0:number_of_samples, 0:frame_size]
    testT2 = test_samples[0:number_of_samples, frame_size:frame_size*2]
    testLocations = test_samples[0:number_of_samples, frame_size*2:(frame_size*2)+3]

    return testT1, testT2, testLocations, testLabels

# This function seperates validation samples to T1 T2 locations and labels for 4 class
# test_samples: the patches(T1, T1, location together)
# frame_size: the length of T1 and T2
# number_of_samples: how many samples to select
# class_type: which class type to select
def take_test_samples_four_class(test_samples, frame_size, number_of_samples, class_type):

    if class_type == 0:
         testLabels = np.tile([1, 0, 0, 0], (number_of_samples, 1))
    elif class_type == 1:
         testLabels = np.tile([0, 1, 0, 0], (number_of_samples, 1))
    elif class_type == 2:
         testLabels = np.tile([0, 0, 1, 0], (number_of_samples, 1))
    elif class_type == 3:
         testLabels = np.tile([0, 0, 0, 1], (number_of_samples, 1))

    testT1 = test_samples[0:number_of_samples, 0:frame_size]
    testT2 = test_samples[0:number_of_samples, frame_size:frame_size*2]
    testLocations = test_samples[0:number_of_samples, frame_size*2:(frame_size*2)+3]

    return testT1, testT2, testLocations, testLabels

# This function seperates validation samples to T1 T2 locations and labels for 3 class
# test_samples: the patches(T1, T1, location together)
# frame_size: the length of T1 and T2
# number_of_samples: how many samples to select
# class_type: which class type to select
def take_test_samples_three_class(test_samples, frame_size, number_of_samples, class_type):

    if class_type == 0:
         testLabels = np.tile([1, 0, 0], (number_of_samples, 1))
    elif class_type == 1:
         testLabels = np.tile([0, 1, 0], (number_of_samples, 1))
    elif class_type == 2:
         testLabels = np.tile([0, 0, 1], (number_of_samples, 1))

    testT1 = test_samples[0:number_of_samples, 0:frame_size]
    testT2 = test_samples[0:number_of_samples, frame_size:frame_size*2]
    testLocations = test_samples[0:number_of_samples, frame_size*2:(frame_size*2)+3]

    return testT1, testT2, testLocations, testLabels

# This function saves training samples to a file
# data_path: the path where data is to be found
# margin: the margin from which to start exploring the mri
# only_white: if only white tissue will be considered
# augmented: if the data will be augmented - not used
def save_training_samples(data_path, margin, onlyWhite, augmented, extension):

    subjects = [s for s in os.listdir(data_path) if not re.match(r'.*\.npz', s)]
    if '.DS_Store' in subjects:
        subjects.remove('.DS_Store')

    for subject in subjects:

        filenameLesion = os.path.join(data_path, subject + lesion_name)
        filenameTissue = os.path.join(data_path, subject + tissue_name)

        mri_Tissue = nib.load(filenameTissue)
        tissue = mri_Tissue.get_data()
        mri_Lesion = nib.load(filenameLesion)
        data_Lesion = mri_Lesion.get_data()

        framesPos, framesNeg = ds.obtain_indices_on_pure_border2(data_Lesion, tissue, margin, onlyWhite)

        fileFrames = os.path.join(data_path, subject + extension)
        np.savez_compressed(fileFrames, pos=framesPos, neg=framesNeg)


# This function saves training samples to a file for 4 class
# data_path: the path where data is to be found
# margin: the margin from which to start exploring the mri
# only_white: if only white tissue will be considered
# augmented: if the data will be augmented - not used
def save_four_class_samples(data_path, margin, onlyWhite, augmented, extension):

    subjects = [s for s in os.listdir(data_path) if not re.match(r'.*\.npz', s)]
    if '.DS_Store' in subjects:
        subjects.remove('.DS_Store')

    for subject in subjects:

        filenameLesion = os.path.join(data_path, subject + lesion_name)
        filenameTissue = os.path.join(data_path, subject + tissue_name)

        mri_Tissue = nib.load(filenameTissue)
        tissue = mri_Tissue.get_data()
        mri_Lesion = nib.load(filenameLesion)
        data_Lesion = mri_Lesion.get_data()

        framesPosInt, framesPosBorder, framesNegInt, framesNegBorder = ds.obtain_indices_four_class(data_Lesion, tissue, margin, onlyWhite)

        fileFrames = os.path.join(data_path, subject + extension)
        np.savez_compressed(fileFrames, posInt=framesPosInt, posBorder=framesPosBorder, negInt=framesNegInt, negBorder=framesNegBorder)


# This function saves training samples to a file for 3 class
# data_path: the path where data is to be found
# margin: the margin from which to start exploring the mri
# only_white: if only white tissue will be considered
# augmented: if the data will be augmented - not used
def save_three_class_samples(data_path, margin, onlyWhite, augmented, extension):

    subjects = [s for s in os.listdir(data_path) if not re.match(r'.*\.npz', s)]
    if '.DS_Store' in subjects:
        subjects.remove('.DS_Store')

    for subject in subjects:

        filenameLesion = os.path.join(data_path, subject + lesion_name)
        filenameTissue = os.path.join(data_path, subject + tissue_name)

        mri_Tissue = nib.load(filenameTissue)
        tissue = mri_Tissue.get_data()
        mri_Lesion = nib.load(filenameLesion)
        data_Lesion = mri_Lesion.get_data()

        framesPosInt, framesPosBorder, framesNegInt = ds.obtain_three_class_indices(data_Lesion, tissue, margin, onlyWhite)

        fileFrames = os.path.join(data_path, subject + extension)
        np.savez_compressed(fileFrames, pos=framesPosInt, border=framesPosBorder, neg=framesNegInt)


# This function retrieves training samples from a file
# data_path: the path where data is to be found
# patch_size: the size of the patch to be considered -
# number_of_classes: how many classes for classification - lesion - non-lesion
def retrieve_samples_from_file(data_path, patch_size, number_of_classes, extension):

    subjects = [s for s in os.listdir(data_path) if not re.match(r'.*\.npz', s)]
    if '.DS_Store' in subjects:
        subjects.remove('.DS_Store')

    frame_size = patch_size**3

    framesPosFinal = np.array([]).reshape(0,2 * frame_size + 3)
    framesNegFinal = np.array([]).reshape(0,2 * frame_size + 3)

    for subject in subjects:

        filenameT1 = os.path.join(data_path, subject + t1_name)
        filenameT2 = os.path.join(data_path, subject + t2_name)

        mri_T1 = nib.load(filenameT1)
        data_T1 = mri_T1.get_data()
        mri_T2 = nib.load(filenameT2)
        data_T2 = mri_T2.get_data()

        data_ST_T1 = ds.standardizeData(data_T1)
        data_ST_T2 = ds.standardizeData(data_T2)

        fileFrames = os.path.join(data_path, subject + extension)

        loaded = np.load(fileFrames)

        indicesPos = loaded['pos']
        indicesNeg = loaded['neg']

        indicesPos = np.random.permutation(indicesPos)
        indicesNeg = np.random.permutation(indicesNeg)

        indicesPos = indicesPos[0:10000, :]
        indicesNeg = indicesNeg[0:10000, :]

        framesPos = takeFramesByIndices(data_ST_T1, data_ST_T2, indicesPos, patch_size)
        framesNeg = takeFramesByIndices(data_ST_T1, data_ST_T2, indicesNeg, patch_size)

        framesPosFinal = np.append(framesPosFinal, framesPos, axis=0)
        framesNegFinal = np.append(framesNegFinal, framesNeg, axis=0)

    framesPosFinal = np.random.permutation(framesPosFinal)
    framesNegFinal = np.random.permutation(framesNegFinal)

    nPosFinal = np.shape(framesPosFinal)[0]
    nNegFinal = np.shape(framesNegFinal)[0]
    nTotal = nPosFinal + nNegFinal

    frames = np.zeros((nTotal, 2 * (patch_size**3) + 3))
    labels = np.zeros((nTotal, number_of_classes))

    indNeg = 0
    indPos = 0

    for i in range(0, nPosFinal + nNegFinal):
        if (i % 2 == 0) and indNeg < nNegFinal:
            frames[i, :] = framesNegFinal[indNeg, :]
            labels[i, :] = [1, 0]
            indNeg +=  1
        elif indPos < nPosFinal:
            frames[i, :] = framesPosFinal[indPos, :]
            labels[i, :] = [0, 1]
            indPos += 1

    labels = labels.astype(float)

    trainFramesT1, trainFramesT2, trainLocations = separate_T1_T2(frames, frame_size)

    return trainFramesT1, trainFramesT2, trainLocations, labels

# This function retrieves training samples from a file for 4 class
# data_path: the path where data is to be found
# patch_size: the size of the patch to be considered - 19
# number_of_classes: how many classes for classification - lesion - non-lesion
def retrieve_four_class_samples_from_file(data_path, patch_size, number_of_classes, extension):

    subjects = [s for s in os.listdir(data_path) if not re.match(r'.*\.npz', s)]
    if '.DS_Store' in subjects:
        subjects.remove('.DS_Store')

    frame_size = patch_size**3

    framesPosIntFinal = np.array([]).reshape(0,2 * frame_size + 3)
    framesPosBorderFinal = np.array([]).reshape(0,2 * frame_size + 3)
    framesNegIntFinal = np.array([]).reshape(0,2 * frame_size + 3)
    framesNegBorderFinal = np.array([]).reshape(0,2 * frame_size + 3)

    for subject in subjects:

        filenameT1 = os.path.join(data_path, subject + t1_name)
        filenameT2 = os.path.join(data_path, subject + t2_name)

        mri_T1 = nib.load(filenameT1)
        data_T1 = mri_T1.get_data()
        mri_T2 = nib.load(filenameT2)
        data_T2 = mri_T2.get_data()

        data_ST_T1 = ds.standardizeData(data_T1)
        data_ST_T2 = ds.standardizeData(data_T2)

        fileFrames = os.path.join(data_path, subject + extension)

        loaded = np.load(fileFrames)

        indicesPosInt = loaded['posInt']
        indicesPosBorder = loaded['posBorder']
        indicesNegInt = loaded['negInt']
        indicesNegBorder = loaded['negBorder']

        indicesPosInt = np.random.permutation(indicesPosInt)
        indicesPosBorder = np.random.permutation(indicesPosBorder)
        indicesNegInt = np.random.permutation(indicesNegInt)
        indicesNegBorder = np.random.permutation(indicesNegBorder)

        indicesPosInt = indicesPosInt[0:5000, :]
        indicesNegInt = indicesNegInt[0:5000, :]
        indicesPosBorder = indicesPosBorder[0:5000, :]
        indicesNegBorder = indicesNegBorder[0:5000, :]

        framesPosInt = takeFramesByIndices(data_ST_T1, data_ST_T2, indicesPosInt, patch_size)
        framesNegInt = takeFramesByIndices(data_ST_T1, data_ST_T2, indicesNegInt, patch_size)
        framesPosBorder = takeFramesByIndices(data_ST_T1, data_ST_T2, indicesPosBorder, patch_size)
        framesNegBorder = takeFramesByIndices(data_ST_T1, data_ST_T2, indicesNegBorder, patch_size)

        framesPosIntFinal = np.append(framesPosIntFinal, framesPosInt, axis=0)
        framesNegIntFinal = np.append(framesNegIntFinal, framesNegInt, axis=0)
        framesPosBorderFinal = np.append(framesPosBorderFinal, framesPosBorder, axis=0)
        framesNegBorderFinal = np.append(framesNegBorderFinal, framesNegBorder, axis=0)


    framesPosIntFinal = np.random.permutation(framesPosIntFinal)
    framesNegIntFinal = np.random.permutation(framesNegIntFinal)
    framesPosBorderFinal = np.random.permutation(framesPosBorderFinal)
    framesNegBorderFinal = np.random.permutation(framesNegBorderFinal)

    nPosIntFinal = np.shape(framesPosIntFinal)[0]
    nNegIntFinal = np.shape(framesNegIntFinal)[0]
    nPosBorderFinal = np.shape(framesPosBorderFinal)[0]
    nNegBorderFinal = np.shape(framesNegBorderFinal)[0]
    nTotal = nPosIntFinal + nNegIntFinal + nPosBorderFinal + nNegBorderFinal

    nMin = min(nPosIntFinal, nNegIntFinal, nPosBorderFinal, nNegBorderFinal)

    framesPosIntFinal = framesPosIntFinal[0:nMin, :]
    framesNegIntFinal = framesNegIntFinal[0:nMin, :]
    framesPosBorderFinal = framesPosBorderFinal[0:nMin, :]
    framesNegBorderFinal = framesNegBorderFinal[0:nMin, :]

    frames = np.zeros((nTotal, 2 * (patch_size**3) + 3))
    labels = np.zeros((nTotal, number_of_classes))

    print nMin
    for i in range(0, nMin * 4):
        ind = i / 4
        class_voxel = i % 4
        if (class_voxel == 0):
            frames[i, :] = framesNegIntFinal[ind, :]
            labels[i, :] = [1, 0, 0, 0]
        elif (class_voxel == 1):
            frames[i, :] = framesNegBorderFinal[ind, :]
            labels[i, :] = [0, 1, 0, 0]
        elif (class_voxel == 2):
            frames[i, :] = framesPosIntFinal[ind, :]
            labels[i, :] = [0, 0, 1, 0]
        elif (class_voxel == 3):
            frames[i, :] = framesPosBorderFinal[ind, :]
            labels[i, :] = [0, 0, 0, 1]

    labels = labels.astype(float)

    trainFramesT1, trainFramesT2, trainLocations = separate_T1_T2(frames, frame_size)

    return trainFramesT1, trainFramesT2, trainLocations, labels

# This function retrieves validation samples from a file for 3 classes
# data_path: the path where data is to be found
# patch_size: the size of the patch to be considered - 19
# number_of_classes: how many classes for classification - lesion - non-lesion
def retrieve_three_class_validation_samples_from_file(data_path, patch_size, number_of_classes, extension):

    subjects = [s for s in os.listdir(data_path) if not re.match(r'.*\.npz', s)]
    if '.DS_Store' in subjects:
        subjects.remove('.DS_Store')

    frame_size = patch_size**3

    framesPosFinal = np.array([]).reshape(0,2 * frame_size + 3)
    framesBorderFinal = np.array([]).reshape(0,2 * frame_size + 3)
    framesNegFinal = np.array([]).reshape(0,2 * frame_size + 3)

    for subject in subjects:

        filenameT1 = os.path.join(data_path, subject + t1_name)
        filenameT2 = os.path.join(data_path, subject + t2_name)

        mri_T1 = nib.load(filenameT1)
        data_T1 = mri_T1.get_data()
        mri_T2 = nib.load(filenameT2)
        data_T2 = mri_T2.get_data()

        data_ST_T1 = ds.standardizeData(data_T1)
        data_ST_T2 = ds.standardizeData(data_T2)

        fileFrames = os.path.join(data_path, subject + extension)

        loaded = np.load(fileFrames)

        indicesPos = loaded['pos']
        indicesBorder = loaded['border']
        indicesNeg = loaded['neg']

        indicesPos = np.random.permutation(indicesPos)
        indicesBorder = np.random.permutation(indicesBorder)
        indicesNeg = np.random.permutation(indicesNeg)

        indicesPos = indicesPos[0:5000, :]
        indicesNeg = indicesNeg[0:5000, :]
        indicesBorder = indicesBorder[0:5000, :]

        framesPos = takeFramesByIndices(data_ST_T1, data_ST_T2, indicesPos, patch_size)
        framesNeg = takeFramesByIndices(data_ST_T1, data_ST_T2, indicesNeg, patch_size)
        framesBorder = takeFramesByIndices(data_ST_T1, data_ST_T2, indicesBorder, patch_size)

        framesPosFinal = np.append(framesPosFinal, framesPos, axis=0)
        framesNegFinal = np.append(framesNegFinal, framesNeg, axis=0)
        framesBorderFinal = np.append(framesBorderFinal, framesBorder, axis=0)

    framesPosFinal = np.random.permutation(framesPosFinal)
    framesNegFinal = np.random.permutation(framesNegFinal)
    framesBorderFinal = np.random.permutation(framesBorderFinal)

    return framesNegFinal, framesBorderFinal, framesPosFinal


# This function retrieves training samples from a file for 3 class
# data_path: the path where data is to be found
# patch_size: the size of the patch to be considered - 19
# number_of_classes: how many classes for classification - lesion - non-lesion
def retrieve_three_class_samples_from_file(data_path, patch_size, number_of_classes, extension):

    subjects = [s for s in os.listdir(data_path) if not re.match(r'.*\.npz', s)]
    if '.DS_Store' in subjects:
        subjects.remove('.DS_Store')

    frame_size = patch_size**3

    framesPosFinal = np.array([]).reshape(0,2 * frame_size + 3)
    framesBorderFinal = np.array([]).reshape(0,2 * frame_size + 3)
    framesNegFinal = np.array([]).reshape(0,2 * frame_size + 3)

    for subject in subjects:

        filenameT1 = os.path.join(data_path, subject + t1_name)
        filenameT2 = os.path.join(data_path, subject + t2_name)

        mri_T1 = nib.load(filenameT1)
        data_T1 = mri_T1.get_data()
        mri_T2 = nib.load(filenameT2)
        data_T2 = mri_T2.get_data()

        data_ST_T1 = ds.standardizeData(data_T1)
        data_ST_T2 = ds.standardizeData(data_T2)

        fileFrames = os.path.join(data_path, subject + extension)

        loaded = np.load(fileFrames)

        indicesPos = loaded['pos']
        indicesBorder = loaded['border']
        indicesNeg = loaded['neg']

        indicesPos = np.random.permutation(indicesPos)
        indicesBorder = np.random.permutation(indicesBorder)
        indicesNeg = np.random.permutation(indicesNeg)

        indicesPos = indicesPos[0:5000, :]
        indicesNeg = indicesNeg[0:5000, :]
        indicesBorder = indicesBorder[0:5000, :]

        framesPos = takeFramesByIndices(data_ST_T1, data_ST_T2, indicesPos, patch_size)
        framesNeg = takeFramesByIndices(data_ST_T1, data_ST_T2, indicesNeg, patch_size)
        framesBorder = takeFramesByIndices(data_ST_T1, data_ST_T2, indicesBorder, patch_size)

        framesPosFinal = np.append(framesPosFinal, framesPos, axis=0)
        framesNegFinal = np.append(framesNegFinal, framesNeg, axis=0)
        framesBorderFinal = np.append(framesBorderFinal, framesBorder, axis=0)

    framesPosFinal = np.random.permutation(framesPosFinal)
    framesNegFinal = np.random.permutation(framesNegFinal)
    framesBorderFinal = np.random.permutation(framesBorderFinal)

    nPosFinal = np.shape(framesPosFinal)[0]
    nNegFinal = np.shape(framesNegFinal)[0]
    nBorderFinal = np.shape(framesBorderFinal)[0]
    nTotal = nPosFinal + nNegFinal + nBorderFinal

    nMin = min(nPosFinal, nNegFinal, nBorderFinal)

    framesPosFinal = framesPosFinal[0:nMin, :]
    framesNegFinal = framesNegFinal[0:nMin, :]
    framesBorderFinal = framesBorderFinal[0:nMin, :]

    frames = np.zeros((nTotal, 2 * (patch_size**3) + 3))
    labels = np.zeros((nTotal, number_of_classes))

    print nMin
    for i in range(0, nMin * 3):
        ind = i / 3
        class_voxel = i % 3
        if (class_voxel == 0):
            frames[i, :] = framesNegFinal[ind, :]
            labels[i, :] = [1, 0, 0]
        elif (class_voxel == 1):
            frames[i, :] = framesBorderFinal[ind, :]
            labels[i, :] = [0, 1, 0]
        elif (class_voxel == 2):
            frames[i, :] = framesPosFinal[ind, :]
            labels[i, :] = [0, 0, 1]

    labels = labels.astype(float)

    trainFramesT1, trainFramesT2, trainLocations = separate_T1_T2(frames, frame_size)

    return trainFramesT1, trainFramesT2, trainLocations, labels

# extracts T1, T2, tissue, lesion files
def extract_files(data_path, subject):

    filenameT1 = os.path.join(data_path, subject + t1_name)
    filenameT2 = os.path.join(data_path, subject + t2_name)
    filenameLesion = os.path.join(data_path, subject + lesion_name)
    filenameTissue = os.path.join(data_path, subject + tissue_name)

    mri_T1 = nib.load(filenameT1)
    data_T1 = mri_T1.get_data()
    mri_T2 = nib.load(filenameT2)
    data_T2 = mri_T2.get_data()
    mri_Tissue = nib.load(filenameTissue)
    tissue = mri_Tissue.get_data()
    mri_Lesion = nib.load(filenameLesion)
    data_Lesion = mri_Lesion.get_data()
    data_ST_T1 = ds.standardizeData(data_T1)
    data_ST_T2 = ds.standardizeData(data_T2)

    tissue[tissue > 1000] = 1001

    ix = np.in1d(tissue.ravel(), whiteAndGrayMatterTissue).reshape(tissue.shape)
    data_Lesion[ix == False] = 0

    return data_ST_T1, data_ST_T2, tissue, data_Lesion

# extracts T1, T2, tissue, lesion files for stage 2
def extract_files_stage2(data_path, subject):

    filenameT1 = os.path.join(data_path, subject + t1_name)
    filenameT2 = os.path.join(data_path, subject + t2_name)
    filenameLesionFound = os.path.join(data_path, subject + lesion_found_name)
    filenameTissue = os.path.join(data_path, subject + tissue_name)

    mri_T1 = nib.load(filenameT1)
    data_T1 = mri_T1.get_data()
    mri_T2 = nib.load(filenameT2)
    data_T2 = mri_T2.get_data()
    mri_Tissue = nib.load(filenameTissue)
    tissue = mri_Tissue.get_data()
    mri_lesion_found = nib.load(filenameLesionFound)
    data_lesion_found = mri_lesion_found.get_data()
    data_ST_T1 = ds.standardizeData(data_T1)
    data_ST_T2 = ds.standardizeData(data_T2)

    return data_ST_T1, data_ST_T2, tissue, data_lesion_found

# extracts lesion files
def extract_lesion(data_path, subject):

    filenameLesion = os.path.join(data_path, subject + lesion_name)
    filenameTissue = os.path.join(data_path, subject + tissue_name)

    mri_lesion = nib.load(filenameLesion)
    data_lesion = mri_lesion.get_data()
    mri_Tissue = nib.load(filenameTissue)
    tissue = mri_Tissue.get_data()

    tissue[tissue > 1000] = 1001

    ix = np.in1d(tissue.ravel(), whiteAndGrayMatterTissue).reshape(tissue.shape)
    data_lesion[ix == False] = 0

    return data_lesion


# This function retrieves test samples from a cross section - k
def retrieve_samples_for_dice(data_ST_T1, data_ST_T2, tissue, data_Lesion, patch_size, number_of_classes, k):

    frame_size = patch_size**3

    framesFinal = np.array([]).reshape(0, 2 * frame_size + 3)
    labelsFinal = np.array([]).reshape(0, number_of_classes)

    marginTemp = 19
    indicesPos, indicesNeg = ds.obtain_indices_for_test(data_Lesion, tissue, marginTemp, True, k)

    framesPos = takeFramesByIndices(data_ST_T1, data_ST_T2, indicesPos, patch_size)
    framesNeg = takeFramesByIndices(data_ST_T1, data_ST_T2, indicesNeg, patch_size)
    nPos = np.shape(framesPos)[0]
    nNeg = np.shape(framesNeg)[0]

    framesFinal = np.append(framesFinal, framesPos, axis=0)
    framesFinal = np.append(framesFinal, framesNeg, axis=0)

    posLabels = np.tile([0, 1], (nPos, 1))
    negLabels = np.tile([1, 0], (nNeg, 1))

    labelsFinal = np.append(labelsFinal, posLabels, axis=0)
    labelsFinal = np.append(labelsFinal, negLabels, axis=0)

    testFramesT1, testFramesT2, testLocations = separate_T1_T2(framesFinal, frame_size)

    return testFramesT1, testFramesT2, testLocations, labelsFinal

# This function retrieves negative test samples from a cross section - k
def retrieve_negative_samples_for_dice(data_ST_T1, data_ST_T2, tissue, data_Lesion, patch_size, number_of_classes, k):

    frame_size = patch_size**3

    indicesNeg = ds.obtain_negative_indices_for_test(data_Lesion, tissue, patch_size, False, k)

    framesNeg = takeFramesByIndices(data_ST_T1, data_ST_T2, indicesNeg, patch_size)
    nNeg = np.shape(framesNeg)[0]

    negLabels = np.tile([1, 0], (nNeg, 1))

    testFramesT1, testFramesT2, testLocations = separate_T1_T2(framesNeg, frame_size)

    return testFramesT1, testFramesT2, testLocations, negLabels, indicesNeg

# This function retrieves negative test samples on the border from a cross section - k to be used in the second stage
def retrieve_negative_samples_on_border(data_ST_T1, data_ST_T2, tissue, data_Lesion, patch_size, number_of_classes, k):

    frame_size = patch_size**3

    indicesNeg = ds.obtain_negative_indices_on_border(data_Lesion, tissue, patch_size, False, k)

    framesNeg = takeFramesByIndices(data_ST_T1, data_ST_T2, indicesNeg, patch_size)
    nNeg = np.shape(framesNeg)[0]

    negLabels = np.tile([1, 0], (nNeg, 1))

    testFramesT1, testFramesT2, testLocations = separate_T1_T2(framesNeg, frame_size)

    return testFramesT1, testFramesT2, testLocations, negLabels, indicesNeg


# This function retrieves positive test samples
def retrieve_positive_samples_for_dice(data_ST_T1, data_ST_T2, tissue, data_Lesion, patch_size, number_of_classes):

    frame_size = patch_size**3

    indicesPos = ds.obtain_positive_indices_for_test(data_Lesion, tissue, patch_size, False)

    framesPos = takeFramesByIndices(data_ST_T1, data_ST_T2, indicesPos, patch_size)
    nPos = np.shape(framesPos)[0]

    posLabels = np.tile([0, 1], (nPos, 1))

    testFramesT1, testFramesT2, testLocations = separate_T1_T2(framesPos, frame_size)

    return testFramesT1, testFramesT2, testLocations, posLabels, indicesPos

# This function retrieves test samples from a cross section - k to be used in the second stage
def retrieve_second_stage_samples(data_ST_T1, data_ST_T2, tissue, data_lesion_found, patch_size, number_of_classes, k):

    frame_size = patch_size**3

    indicesPos = ds.obtain_second_stage_indices(data_lesion_found, tissue, patch_size, False, k)

    framesPos = takeFramesByIndices(data_ST_T1, data_ST_T2, indicesPos, patch_size)

    testFramesT1, testFramesT2, testLocations = separate_T1_T2(framesPos, frame_size)

    return testFramesT1, testFramesT2, testLocations, indicesPos

# This function retrieves test samples from a cross section - k
def retrieve_samples(data_ST_T1, data_ST_T2, tissue, data_Lesion, patch_size, number_of_classes, k):

    frame_size = patch_size**3

    indices = ds.obtain_indices(data_Lesion, tissue, patch_size, False, k)

    frames = takeFramesByIndices(data_ST_T1, data_ST_T2, indices, patch_size)

    testFramesT1, testFramesT2, testLocations = separate_T1_T2(frames, frame_size)

    return testFramesT1, testFramesT2, testLocations, indices


# This function retrieves validation samples from a file
# data_path: the path where data is to be found
# patch_size: the size of the patch to be considered - 19
# number_of_classes: how many classes for classification - lesion - non-lesion
# the extension of the file from which to retrieve the validation samples
def retrieve_validation_samples_from_file(data_path, patch_size, number_of_classes, extension):

    subjects = [s for s in os.listdir(data_path) if not re.match(r'.*\.npz', s)]
    if '.DS_Store' in subjects:
        subjects.remove('.DS_Store')

    frame_size = patch_size**3

    framesPosIntFinal = np.array([]).reshape(0,2 * frame_size + 3)
    framesNegIntFinal = np.array([]).reshape(0,2 * frame_size + 3)
    framesPosBorderFinal = np.array([]).reshape(0,2 * frame_size + 3)
    framesNegBorderFinal = np.array([]).reshape(0,2 * frame_size + 3)

    for subject in subjects:

        filenameT1 = os.path.join(data_path, subject + t1_name)
        filenameT2 = os.path.join(data_path, subject + t2_name)

        mri_T1 = nib.load(filenameT1)
        data_T1 = mri_T1.get_data()
        mri_T2 = nib.load(filenameT2)
        data_T2 = mri_T2.get_data()

        data_ST_T1 = ds.standardizeData(data_T1)
        data_ST_T2 = ds.standardizeData(data_T2)

        fileFrames = os.path.join(data_path, subject + extension)

        loaded = np.load(fileFrames)

        indicesPosInt = loaded['posInt']
        indicesNegInt = loaded['negInt']
        indicesPosBorder = loaded['posBorder']
        indicesNegBorder = loaded['negBorder']

        indicesPosInt = np.random.permutation(indicesPosInt)
        indicesNegInt = np.random.permutation(indicesNegInt)
        indicesPosBorder = np.random.permutation(indicesPosBorder)
        indicesNegBorder = np.random.permutation(indicesNegBorder)

        indicesPosInt = indicesPosInt[0:1000, :]
        indicesNegInt = indicesNegInt[0:1000, :]
        indicesPosBorder = indicesPosBorder[0:1000, :]
        indicesNegBorder = indicesNegBorder[0:1000, :]

        framesPosInt = takeFramesByIndices(data_ST_T1, data_ST_T2, indicesPosInt, patch_size)
        framesNegInt = takeFramesByIndices(data_ST_T1, data_ST_T2, indicesNegInt, patch_size)
        framesPosBorder = takeFramesByIndices(data_ST_T1, data_ST_T2, indicesPosBorder, patch_size)
        framesNegBorder = takeFramesByIndices(data_ST_T1, data_ST_T2, indicesNegBorder, patch_size)

        framesPosIntFinal = np.append(framesPosIntFinal, framesPosInt, axis=0)
        framesNegIntFinal = np.append(framesNegIntFinal, framesNegInt, axis=0)
        framesPosBorderFinal = np.append(framesPosBorderFinal, framesPosBorder, axis=0)
        framesNegBorderFinal = np.append(framesNegBorderFinal, framesNegBorder, axis=0)

    framesPosIntFinal = np.random.permutation(framesPosIntFinal)
    framesNegIntFinal = np.random.permutation(framesNegIntFinal)
    framesPosBorderFinal = np.random.permutation(framesPosBorderFinal)
    framesNegBorderFinal = np.random.permutation(framesNegBorderFinal)

    return framesPosIntFinal, framesPosBorderFinal, framesNegIntFinal, framesNegBorderFinal

# separate T1, T2, locations
def separate_T1_T2(frames, frame_size):

    trainFramesT1 = frames[:, 0:frame_size]
    trainFramesT2 = frames[:, frame_size:frame_size*2]
    trainLocations = frames[:, frame_size*2:(frame_size*2)+3]

    return trainFramesT1, trainFramesT2, trainLocations

# obtain samples using indices
def takeFramesByIndices(data_T1, data_T2, indices, patch_size):

    sizeIndices = np.shape(indices)[0]

    frames = np.zeros((sizeIndices, 2 * (patch_size**3) + 3))

    dims = np.shape(data_T1)
    xDim = dims[0]
    yDim = dims[1]
    zDim = dims[2]

    margin = int((patch_size - 1) / 2)

    for num in range(0, sizeIndices):

        i = int(indices[num, 0])
        j = int(indices[num, 1])
        k = int(indices[num, 2])

        patch_T1 = data_T1[i-margin:i+(margin + 1), j-margin:j+(margin + 1), k-margin:k+(margin + 1)]
        newFrame = np.reshape(patch_T1, -1)
        patch_T2 = data_T2[i-margin:i+(margin + 1), j-margin:j+(margin + 1), k-margin:k+(margin + 1)]
        newFrame_T2 = np.reshape(patch_T2, -1)
        newFrame = np.append(newFrame, newFrame_T2, axis=0)
        newFrame = np.append(newFrame, [float(i) / xDim, float(j) / yDim, float(k) / zDim], axis=0)
        frames[num, :] = newFrame

    return frames

# save the lesions found in a lesion file
def save_found_lesion_file(data_path, subject, data_lesion, data_lesion_prob, org_data_lesion):

    filenameOrgLesion = os.path.join(data_path, subject + lesion_name)

    filenameLesionFound = os.path.join(data_path, subject + "_Lesions.nii.gz")
    filenameLesionOrg = os.path.join(data_path, subject + "_Org_Lesions.nii.gz")
    filenameLesionProb = os.path.join(data_path, subject + "_Lesions_prob.nii.gz")
    filenameLesionStage2 = os.path.join(data_path, subject + lesion_found_name)

    mri_Lesion = nib.load(filenameOrgLesion)

    lesionImage = nib.Nifti1Image(data_lesion, mri_Lesion.affine, mri_Lesion.header)
    nib.save(lesionImage, filenameLesionFound)

    lesionOrgImage = nib.Nifti1Image(org_data_lesion, mri_Lesion.affine, mri_Lesion.header)
    nib.save(lesionOrgImage, filenameLesionOrg)

    lesionProbImage = nib.Nifti1Image(data_lesion_prob, mri_Lesion.affine, mri_Lesion.header)
    nib.save(lesionProbImage, filenameLesionProb)
    nib.save(lesionProbImage, filenameLesionStage2)

# save the second stage lesion file
def save_cert_lesion_file(data_path, subject, data_lesion_cert, second_stage):

    filenameOrgLesion = os.path.join(data_path, subject + lesion_name)
    filenameFirstStage = os.path.join(data_path, subject + lesion_found_name)

    filenameLesionCert = os.path.join(data_path, subject + lesion_final)

    mri_Lesion = nib.load(filenameOrgLesion)

    lesionImage = nib.Nifti1Image(data_lesion_cert, mri_Lesion.affine, mri_Lesion.header)
    if second_stage:
        nib.save(lesionImage, filenameLesionCert)
    else:
        nib.save(lesionImage, filenameFirstStage)

