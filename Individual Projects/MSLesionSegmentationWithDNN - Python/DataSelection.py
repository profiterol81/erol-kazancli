import numpy as np
import random
import sklearn.preprocessing as pp

whiteMatterTissue = [2, 41, 77, 78, 79, 251, 252, 253, 254, 255]
whiteAndGrayMatterTissue = [2, 41, 77, 78, 79, 251, 252, 253, 254, 255, 9, 10, 11, 12, 13, 17, 18, 26, 48, 49, 50, 51, 52, 53, 54, 58, 28, 60, 1001]

t1_name = '/t1_aligned_brain.nii.gz'
t2_name = '/t2_aligned_brain.nii.gz'
lesion_name = '/lesions_aligned.nii.gz'
tissue_name = '/segmentation_aligned.nii.gz'

# This function selects all the positive samples on the exact border of lesions.
# It takes the negative samples one pixel away from the border.
# data_lesion: lesion file
# tissue: tissue file
# patch_size: the size of the 3D patch used
# class_number: the number of classes to be used
def obtain_indices_on_pure_border2(data_Lesion, tissue, marginTemp, onlyWhite):

    dims = np.shape(data_Lesion)
    xDim = dims[0]
    yDim = dims[1]
    zDim = dims[2]

    framesPos = np.zeros((80000, 3))
    framesNeg = np.zeros((80000, 3))

    nPos = 0
    nNeg = 0

    aaa = 0
    bbb = 0
    for i in range(marginTemp, xDim - (marginTemp + 1)):
        for j in range(marginTemp, yDim - (marginTemp + 1)):
            for k in range (marginTemp, zDim - (marginTemp + 1)):
                label = int(data_Lesion[i, j, k])
                tissueType = int(tissue[i, j, k])
                if (label == 1) or (onlyWhite and tissueType in whiteMatterTissue) or ((not onlyWhite) and (tissueType in whiteAndGrayMatterTissue or tissueType > 1000)):
                    patchLes1 = data_Lesion[i-1:i+(1 + 1), j-1:j+(1 + 1), k-1:k+(1 + 1)]
                    numLes1 = np.sum(patchLes1==1)
                    patchLes2 = data_Lesion[i-2:i+(2 + 1), j-2:j+(2 + 1), k-2:k+(2 + 1)]
                    numLes2 = np.sum(patchLes2==1)
                    if numLes2 > 0:
                        if label == 1 and numLes1 < 3**3: # take the positive examples on the border
                            framesPos[nPos, 0] = i
                            framesPos[nPos, 1] = j
                            framesPos[nPos, 2] = k

                            nPos += 1
                        else:
                            if label == 0 and numLes1 == 0: # take the negative examples not on the border but not far from the border
                                randNum = random.uniform(0, 1)
                                if randNum > 0.3:
                                    framesNeg[nNeg, 0] = i
                                    framesNeg[nNeg, 1] = j
                                    framesNeg[nNeg, 2] = k

                                    nNeg += 1
                                    bbb += 1

                    else: # take some negative examples
                        if label == 0:
                            randNum = random.uniform(0, 1)
                            if randNum > 0.999:
                                framesNeg[nNeg, 0] = i
                                framesNeg[nNeg, 1] = j
                                framesNeg[nNeg, 2] = k

                                nNeg += 1
                                aaa += 1
    print "interior negative : " + str(aaa)
    print "border negative : " + str(bbb)

    framesPos = framesPos[0:nPos, :]
    framesNeg = framesNeg[0:nNeg, :]

    framesPos = np.random.permutation(framesPos)
    framesNeg = np.random.permutation(framesNeg)

    if nNeg >= nPos:
        framesNeg = framesNeg[0:nPos, :]
        framesPos = framesPos[0:nPos, :]
    else:
        framesNeg = framesNeg[0:nNeg, :]
        framesPos = framesPos[0:nNeg, :]

    return framesPos, framesNeg

# This function selects validation samples from border with lesions and interior regions into 4 class
# data_lesion: lesion file
# tissue: tissue file
# patch_size: the size of the 3D patch used
# class_number: the number of classes to be used
def obtain_indices_four_class(data_Lesion, tissue, marginTemp, onlyWhite):

    dims = np.shape(data_Lesion)
    xDim = dims[0]
    yDim = dims[1]
    zDim = dims[2]

    framesPosInt = np.zeros((80000, 3))
    framesNegInt = np.zeros((80000, 3))
    framesPosBorder = np.zeros((80000, 3))
    framesNegBorder = np.zeros((80000, 3))

    nPosInt = 0
    nNegInt = 0
    nPosBorder = 0
    nNegBorder = 0

    sizeSubRegion = 3
    threshold = 0

    for i in range(marginTemp, xDim - marginTemp - sizeSubRegion, sizeSubRegion):
        for j in range(marginTemp, yDim - marginTemp - sizeSubRegion, sizeSubRegion):
            for k in range (marginTemp, zDim - marginTemp - sizeSubRegion, sizeSubRegion):
                borderX = i+sizeSubRegion
                borderY = j+sizeSubRegion
                borderZ = k+sizeSubRegion

                subRegion = data_Lesion[i:borderX, j:borderY, k:borderZ]

                number_of_lesions = np.sum(subRegion == 1)
                prop = float(number_of_lesions) / (sizeSubRegion * sizeSubRegion * sizeSubRegion)

                # Take the samples from the subregion if bigger than thresholds
                if prop > threshold:
                    for x in range(i, borderX):
                        for y in range(j, borderY):
                            for z in range(k, borderZ):
                                label = int(data_Lesion[x, y, z])
                                tissueType = int(tissue[x, y, z])

                                if (label == 1) or (onlyWhite and tissueType in whiteMatterTissue) or ((not onlyWhite) and (tissueType in whiteAndGrayMatterTissue or tissueType > 1000)):
                                    patchLes1 = data_Lesion[x-1:x+(1 + 1), y-1:y+(1 + 1), z-1:z+(1 + 1)]
                                    numLes1 = np.sum(patchLes1==1)

                                    if label == 1:
                                        if numLes1 < (3**3)-10:
                                            framesPosBorder[nPosBorder, 0] = x
                                            framesPosBorder[nPosBorder, 1] = y
                                            framesPosBorder[nPosBorder, 2] = z

                                            nPosBorder += 1
                                        else:
                                            framesPosInt[nPosInt, 0] = x
                                            framesPosInt[nPosInt, 1] = y
                                            framesPosInt[nPosInt, 2] = z
                                            nPosInt += 1
                                    else:
                                        framesNegBorder[nNegBorder, 0] = x
                                        framesNegBorder[nNegBorder, 1] = y
                                        framesNegBorder[nNegBorder, 2] = z
                                        nNegBorder += 1
                else:
                    randNum = random.uniform(0, 1)
                    if randNum > 0.7:
                        distToCenter = ((sizeSubRegion - 1) / 2 + 1)
                        x = i + distToCenter
                        y = j + distToCenter
                        z = k + distToCenter
                        label = int(data_Lesion[x, y, z])
                        tissueType = int(tissue[x, y, z])

                        if (label == 1) or (onlyWhite and tissueType in whiteMatterTissue) or ((not onlyWhite) and (tissueType in whiteAndGrayMatterTissue or tissueType > 1000)):

                            if label == 1:
                                framesPosBorder[nPosBorder, 0] = x
                                framesPosBorder[nPosBorder, 1] = y
                                framesPosBorder[nPosBorder, 2] = z
                                nPosBorder += 1
                            else:
                                framesNegInt[nNegInt, 0] = x
                                framesNegInt[nNegInt, 1] = y
                                framesNegInt[nNegInt, 2] = z
                                nNegInt += 1

    print "posint:" + str(nPosInt) + " posborder:" + str(nPosBorder) + " negint:" + str(nNegInt) + " negborder:" + str(nNegBorder)

    framesPosInt = framesPosInt[0:nPosInt, :]
    framesNegInt = framesNegInt[0:nNegInt, :]
    framesPosBorder = framesPosBorder[0:nPosBorder, :]
    framesNegBorder = framesNegBorder[0:nNegBorder, :]

    framesPosInt = np.random.permutation(framesPosInt)
    framesNegInt = np.random.permutation(framesNegInt)
    framesPosBorder = np.random.permutation(framesPosBorder)
    framesNegBorder = np.random.permutation(framesNegBorder)

    return framesPosInt, framesPosBorder, framesNegInt, framesNegBorder


# This function selects indices of negative, positive and border samples
def obtain_three_class_indices(data_Lesion, tissue, marginTemp, onlyWhite):

    dims = np.shape(data_Lesion)
    xDim = dims[0]
    yDim = dims[1]
    zDim = dims[2]

    framesPos = np.zeros((80000, 3))
    framesNeg = np.zeros((80000, 3))
    framesBorder = np.zeros((80000, 3))

    nPos = 0
    nNeg = 0
    nBorder = 0

    sizeSubRegion = 3

    for i in range(marginTemp, xDim - marginTemp - sizeSubRegion, sizeSubRegion):
        for j in range(marginTemp, yDim - marginTemp - sizeSubRegion, sizeSubRegion):
            for k in range (marginTemp, zDim - marginTemp - sizeSubRegion, sizeSubRegion):
                borderX = i+sizeSubRegion
                borderY = j+sizeSubRegion
                borderZ = k+sizeSubRegion

                for x in range(i, borderX):
                    for y in range(j, borderY):
                        for z in range(k, borderZ):
                            label = int(data_Lesion[x, y, z])
                            tissueType = int(tissue[x, y, z])

                            if (onlyWhite and tissueType in whiteMatterTissue) or ((not onlyWhite) and (tissueType in whiteAndGrayMatterTissue or tissueType > 1000)):
                                patchLes1 = data_Lesion[x-2:x+(2 + 1), y-2:y+(2 + 1), z-2:z+(2 + 1)]
                                numLes1 = np.sum(patchLes1==1)
                                if label == 1:
                                    framesPos[nPos, 0] = x
                                    framesPos[nPos, 1] = y
                                    framesPos[nPos, 2] = z
                                    nPos += 1
                                else:
                                    if numLes1 == 0:
                                        randNum = random.uniform(0, 1)
                                        if randNum > 0.97:
                                            framesNeg[nNeg, 0] = x
                                            framesNeg[nNeg, 1] = y
                                            framesNeg[nNeg, 2] = z
                                            nNeg += 1
                                    else:
                                        framesBorder[nBorder, 0] = x
                                        framesBorder[nBorder, 1] = y
                                        framesBorder[nBorder, 2] = z

                                        nBorder += 1

    print "pos:" + str(nPos) + " border:" + str(nBorder) + " neg:" + str(nNeg)

    framesPos = framesPos[0:nPos, :]
    framesNeg = framesNeg[0:nNeg, :]
    framesBorder = framesBorder[0:nBorder, :]

    framesPos = np.random.permutation(framesPos)
    framesNeg = np.random.permutation(framesNeg)
    framesBorder = np.random.permutation(framesBorder)

    return framesPos, framesBorder, framesNeg

# This function selects indices of negative and positive samples from a cross section for test
def obtain_indices_for_test(data_Lesion, tissue, marginTemp, onlyWhite, k):

    dims = np.shape(data_Lesion)
    xDim = dims[0]
    yDim = dims[1]
    zDim = dims[2]

    framesPos = np.zeros((60000, 3))
    framesNeg = np.zeros((60000, 3))

    nPos = 0
    nNeg = 0

    for i in range(marginTemp, xDim - (marginTemp + 1)):
        for j in range(marginTemp, yDim - (marginTemp + 1)):
            label = int(data_Lesion[i, j, k])
            tissueType = int(tissue[i, j, k])
            if (label == 1) or (onlyWhite and tissueType in whiteMatterTissue) or ((not onlyWhite) and (tissueType in whiteAndGrayMatterTissue or tissueType > 1000)):
                if label == 1:
                    framesPos[nPos, 0] = i
                    framesPos[nPos, 1] = j
                    framesPos[nPos, 2] = k

                    nPos += 1
                else: # take negative samples 1 pixel away from the border
                    framesNeg[nNeg, 0] = i
                    framesNeg[nNeg, 1] = j
                    framesNeg[nNeg, 2] = k

                    nNeg += 1

    framesPos = framesPos[0:nPos, :]
    framesNeg = framesNeg[0:nNeg, :]

    return framesPos, framesNeg

# This function selects indices of negative samples from a cross section for test
def obtain_negative_indices_for_test(data_Lesion, tissue, marginTemp, onlyWhite, k):

    dims = np.shape(data_Lesion)
    xDim = dims[0]
    yDim = dims[1]
    zDim = dims[2]

    framesNeg = np.zeros((60000, 3)).astype(int)

    nNeg = 0

    for i in range(marginTemp, xDim - (marginTemp + 1)):
        for j in range(marginTemp, yDim - (marginTemp + 1)):
            label = int(data_Lesion[i, j, k])
            tissueType = int(tissue[i, j, k])
            if (onlyWhite and tissueType in whiteMatterTissue) or ((not onlyWhite) and (tissueType in whiteAndGrayMatterTissue or tissueType > 1000)):
                if label == 0:
                    framesNeg[nNeg, 0] = i
                    framesNeg[nNeg, 1] = j
                    framesNeg[nNeg, 2] = k

                    nNeg += 1

    framesNeg = framesNeg[0:nNeg, :]

    return framesNeg

# This function selects indices of negative samples on the border from a cross section for test to be used for the second stage
def obtain_negative_indices_on_border(data_Lesion, tissue, marginTemp, onlyWhite, k):

    dims = np.shape(data_Lesion)
    xDim = dims[0]
    yDim = dims[1]
    zDim = dims[2]

    framesNeg = np.zeros((60000, 3)).astype(int)

    nNeg = 0

    for i in range(marginTemp, xDim - (marginTemp + 1)):
        for j in range(marginTemp, yDim - (marginTemp + 1)):
            label = int(data_Lesion[i, j, k])
            tissueType = int(tissue[i, j, k])
            patchLes1 = data_Lesion[i-1:i+(1 + 1), j-1:j+(1 + 1), k-1:k+(1 + 1)]
            patchLes2 = data_Lesion[i-2:i+(2 + 1), j-2:j+(2 + 1), k-2:k+(2 + 1)]
            numLes1 = np.sum(patchLes1==1)
            numLes2 = np.sum(patchLes2==1)
            if numLes1 == 0 and numLes2 > 0 and label == 0:
                if (onlyWhite and tissueType in whiteMatterTissue) or ((not onlyWhite) and (tissueType in whiteAndGrayMatterTissue or tissueType > 1000)):
                    framesNeg[nNeg, 0] = i
                    framesNeg[nNeg, 1] = j
                    framesNeg[nNeg, 2] = k

                    nNeg += 1

    framesNeg = framesNeg[0:nNeg, :]

    return framesNeg

# This function selects indices of samples from a cross section for test based on the lesions found in the previous stage
def obtain_second_stage_indices(data_lesion_found, tissue, marginTemp, onlyWhite, k):

    dims = np.shape(data_lesion_found)
    xDim = dims[0]
    yDim = dims[1]
    zDim = dims[2]

    framesPos = np.zeros((10000, 3)).astype(int)

    nPos = 0

    for i in range(marginTemp, xDim - (marginTemp + 1)):
        for j in range(marginTemp, yDim - (marginTemp + 1)):
            tissueType = int(tissue[i, j, k])
            label_found = int(data_lesion_found[i, j, k])
            if (onlyWhite and tissueType in whiteMatterTissue) or ((not onlyWhite) and (tissueType in whiteAndGrayMatterTissue or tissueType > 1000)):
                if label_found == 1:
                    framesPos[nPos, 0] = i
                    framesPos[nPos, 1] = j
                    framesPos[nPos, 2] = k

                    nPos += 1

    framesPos = framesPos[0:nPos, :]

    return framesPos

# This function selects indices of samples from a cross section for test
def obtain_indices(data_lesion_found, tissue, marginTemp, onlyWhite, k):

    dims = np.shape(data_lesion_found)
    xDim = dims[0]
    yDim = dims[1]
    zDim = dims[2]

    framesPos = np.zeros((30000, 3)).astype(int)

    nPos = 0

    for i in range(marginTemp, xDim - (marginTemp + 1)):
        for j in range(marginTemp, yDim - (marginTemp + 1)):
            tissueType = int(tissue[i, j, k])
            if (onlyWhite and tissueType in whiteMatterTissue) or ((not onlyWhite) and (tissueType in whiteAndGrayMatterTissue or tissueType > 1000)):
                framesPos[nPos, 0] = i
                framesPos[nPos, 1] = j
                framesPos[nPos, 2] = k

                nPos += 1

    framesPos = framesPos[0:nPos, :]

    return framesPos



# This function selects indices of positive samples for test
# data_lesion: lesion file
# tissue: tissue file
# patch_size: the size of the 3D patch used
# class_number: the number of classes to be used
def obtain_positive_indices_for_test(data_Lesion, tissue, marginTemp, onlyWhite):

    dims = np.shape(data_Lesion)
    xDim = dims[0]
    yDim = dims[1]
    zDim = dims[2]

    framesPos = np.zeros((60000, 3)).astype(int)

    nPos = 0

    for i in range(marginTemp, xDim - (marginTemp + 1)):
        for j in range(marginTemp, yDim - (marginTemp + 1)):
            for k in range(marginTemp, zDim - (marginTemp + 1)):
                label = int(data_Lesion[i, j, k])
                tissueType = int(tissue[i, j, k])
                if (onlyWhite and tissueType in whiteMatterTissue) or ((not onlyWhite) and (tissueType in whiteAndGrayMatterTissue or tissueType > 1000)):
                    if label == 1:
                        framesPos[nPos, 0] = i
                        framesPos[nPos, 1] = j
                        framesPos[nPos, 2] = k

                        nPos += 1

    framesPos = framesPos[0:nPos, :]

    return framesPos


# This function standardizes data with 0-mean unit variation standardization.
# data: data to be standardized
def standardizeData(data):

    dims = np.shape(data)
    xDim = dims[0]
    yDim = dims[1]
    zDim = dims[2]

    interim = data.astype(float)
    interim = np.reshape(interim, -1)
    interim = pp.scale(interim)
    interim = np.around(interim, decimals=3)
    stdata = np.reshape(interim, (xDim, yDim, zDim))

    return stdata