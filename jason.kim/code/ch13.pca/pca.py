'''
Created on Jun 1, 2011

@author: Peter Harrington
'''
from numpy import *

def loadDataSet(fileName, delim='\t'):
    fr = open(fileName)
    strs_list = [line.strip().split(delim) for line in fr.readlines()]
    float_list_list = [map(float, strs) for strs in strs_list]
    return mat(float_list_list)

def pca(dataMat, topNfeat=9999999):
    meanVals = mean(dataMat, axis=0)
    meanRemoved = dataMat - meanVals    # remove mean
    covMat = cov(meanRemoved, rowvar=0)
    eigVals, eigVects = linalg.eig(mat(covMat))
    eigValInd = argsort(eigVals)              # sort, sort goes smallest to largest
    eigValInd = eigValInd[:-(topNfeat+1):-1]  # cut off unwanted dimensions
    redEigVects = eigVects[:, eigValInd]      # reorganize eig vects largest to smallest
    lowDDataMat = meanRemoved * redEigVects   # transform data into new dimensions
    reconMat = (lowDDataMat * redEigVects.T) + meanVals
    return lowDDataMat, reconMat

# dataMat = loadDataSet('testSet.txt')
# lowDMat, reconMat = pca(dataMat, 2)
# print shape(lowDMat)
# print shape(reconMat)
#
# import matplotlib
# matplotlib.use('TkAgg')
# import matplotlib.pyplot as plt
# fig = plt.figure()
# ax = fig.add_subplot(111)
# ax.scatter(dataMat[:,0].flatten().A[0], dataMat[:,1].flatten().A[0], marker='^', s=90)
# ax.scatter(reconMat[:,0].flatten().A[0], reconMat[:,1].flatten().A[0], marker='o', s=50, c='red')
# plt.show()


def replaceNanWithMean(): 
    datMat = loadDataSet('secom.data', ' ')
    numFeat = shape(datMat)[1]
    # replaced = []
    for i in range(numFeat):
        meanVal = mean(datMat[nonzero(~isnan(datMat[:, i].A))[0], i]) #values that are not NaN (a number)
        # replaced.append(str(shape(nonzero(isnan(datMat[:, i].A))[0])[0]))
        datMat[nonzero(isnan(datMat[:, i].A))[0], i] = meanVal  #set NaN values to mean
    # print ','.join(replaced)
    return datMat

dataMat = replaceNanWithMean()
meanVals = mean(dataMat, axis=0)
meanRemoved = dataMat - meanVals
covMat = cov(meanRemoved, rowvar=0)
eigVals, eigVects = linalg.eig(mat(covMat))

print eigVals[0] / (meanVals.tolist()[0][0] * shape(dataMat)[0])
print eigVals[1] / (meanVals.tolist()[0][1] * shape(dataMat)[0])
print eigVals[2] / (meanVals.tolist()[0][2] * shape(dataMat)[0])
print eigVals[3] / (meanVals.tolist()[0][3] * shape(dataMat)[0])
print eigVals[4] / (meanVals.tolist()[0][4] * shape(dataMat)[0])


n = shape(dataMat)[0]
