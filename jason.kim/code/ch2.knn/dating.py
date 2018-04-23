from kNN import *
import matplotlib.pyplot as plt

def file2matrix(filename):
    fr = open(filename)
    numberOfLines = len(fr.readlines())
    returnMat = zeros((numberOfLines, 3))
    classLabelVector = []
    fr = open(filename)
    index = 0
    for line in fr.readlines():
        line = line.strip()
        listFromLine = line.split('\t')
        returnMat[index,:] = listFromLine[0:3]
        classLabelVector.append(int(listFromLine[-1]))
        index += 1
    return returnMat,classLabelVector

def file2matrix2(filename):
    fr = open(filename)
    numberOfLines = len(fr.readlines())
    returnMat = zeros((numberOfLines, 3))
    classLabelVector = []
    fr = open(filename)
    index = 0
    for line in fr.readlines():
        line = line.strip()
        listFromLine = line.split('\t')
        returnMat[index,:] = listFromLine[0:3]
        classLabelVector.append(listFromLine[-1])
        index += 1
    return returnMat,classLabelVector

# datingMat, datingLabels = file2matrix2('datingTestSet.txt')
datingMat, datingLabels = file2matrix('datingTestSet2.txt')
print datingMat
print datingLabels

fig = plt.figure()
ax = fig.add_subplot(111)
# ax.scatter(datingMat[:, 1], datingMat[:, 2])
# ax.scatter(datingMat[:, 1], datingMat[:, 2], 15.0 * array(datingLabels), 15.0 * array(datingLabels))
ax.scatter(datingMat[:, 0], datingMat[:, 1], 15.0 * array(datingLabels), 15.0 * array(datingLabels))
plt.show()


def autoNorm(dataSet):
    minVals = dataSet.min(0)
    maxVals = dataSet.max(0)
    ranges = maxVals - minVals
    normDataSet = zeros(shape(dataSet))
    m = dataSet.shape[0]
    normDataSet = dataSet - tile(minVals, (m,1))
    normDataSet = normDataSet/tile(ranges, (m,1))   #element wise divide
    return normDataSet, ranges, minVals


normMat, ranges, minvals = autoNorm(datingMat)
fig = plt.figure()
ax = fig.add_subplot(111)
ax.scatter(normMat[:, 0], normMat[:, 1], 15.0 * array(datingLabels), 15.0 * array(datingLabels))
plt.show()

def datingClassTest():
    hoRatio = 0.50      #hold out 10%
    datingDataMat,datingLabels = file2matrix('datingTestSet2.txt')       #load data setfrom file
    normMat, ranges, minVals = autoNorm(datingDataMat)
    m = normMat.shape[0]
    numTestVecs = int(m*hoRatio)
    errorCount = 0.0
    for i in range(numTestVecs):
        classifierResult = classify0(normMat[i,:],normMat[numTestVecs:m,:],datingLabels[numTestVecs:m],3)
        print "the classifier came back with: %d, the real answer is: %d" % (classifierResult, datingLabels[i])
        if (classifierResult != datingLabels[i]): errorCount += 1.0
    print "the total error rate is: %f" % (errorCount/float(numTestVecs))
    print errorCount

datingClassTest()

