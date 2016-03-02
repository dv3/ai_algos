#k-nearest neighbor classifiers
import sys,math
numofclasses = 0


def normalizeDatasets(someExamples,someAttributes):
    normalizedAnyExample=[]
    mathsArrays=[]
    for i in range(0,len(someExamples[0])-1):
        aColumn=select_column(someExamples, i)
        values=calculateStandardDeviation(aColumn)
        mathsArrays.append(values)

    if not (len(mathsArrays) == (len(someExamples[1])-1) ):
        print 'big problem, mean,std of n attributes not equal to number of attributes itself'
        sys.exit(2)

    for row in someExamples:
        claz=row[-1]
        theRow=row[:len(row)-1]
        oneNormalizedRow=functionfv(theRow,mathsArrays)
        oneNormalizedRow.append(claz)
        #print 'oneNormalizedRow',oneNormalizedRow
        normalizedAnyExample.append(oneNormalizedRow)

    return normalizedAnyExample

def classificationByDistance( normalizedTrainingExample, trainingAttributes, normalizedTestExample, testAttributes,numOfNeighbours ):
    testRowNumber=0
    allacuracy=[]
    for test_row in normalizedTestExample:        
        distMap={}
        i=0
        for train_row in normalizedTrainingExample:
            distance = calculateEuclideanDistance(test_row, train_row)
            distMap[i]=distance
            i=i+1

        #Sort the values based on the lowest distances
        sorted_keys = sorted(distMap, key=distMap.__getitem__)
        predictedClasses = []
        distribu1=[]
        for i in range(0, numOfNeighbours):
            distances=distMap.get(sorted_keys[i])
            trainRowNumber=sorted_keys[i]
            #print 'blah',blah
            myClass = classOfRow(normalizedTrainingExample, trainRowNumber )
            distribu1.append( [trainRowNumber,distances,myClass] )
            predictedClasses.append(myClass)
            #print 'predictedClasses',predictedClasses

        closestClasses=countClass(predictedClasses)
        #print 'closestClasses',closestClasses

        distribu,waster=findingClasswiseRows(distribu1)
        #print 'distribu1',distribu1

        eachClassWithMinRow={}
        for eachClass in distribu:
            pointsOfClass=distribu[eachClass]
            distanceClass=select_column(pointsOfClass, 0)
            leastDist=min(distanceClass)
            for rows in pointsOfClass:
                if rows[0] == leastDist:
                    eachClassWithMinRow[eachClass]=rows

        #print '\neachClassWithMinRow',eachClassWithMinRow

        newd={}
        for k,v in closestClasses.iteritems():
            newd.setdefault(v,[]).append(k)

        maxProbability=max(newd)
        maxClasses=newd[maxProbability]
        trueClass= test_row[-1]
        acuracy=None
        nn_index=None
        distan=None

        if len(maxClasses) == 1:
            predictedClass=maxClasses[0]
            values=eachClassWithMinRow[predictedClass]
            nn_index=values[0]
            distan=values[1]
            if trueClass == predictedClass: #exact 1 class match
                acuracy=1    
                allacuracy.append(acuracy)
            else: #no single match
                acuracy=0
                allacuracy.append(acuracy)
        else:
            if trueClass in maxClasses: #match in tied classes
                predictedClass=trueClass
                numClassTied= len(maxClasses)
                acuracy=1/float(numClassTied)
                values=eachClassWithMinRow[predictedClass]
                nn_index=values[0]
                distan=values[1]
                allacuracy.append(acuracy)
            else: # no classes match from tied ones
                predictedClass=maxClasses[0]
                acuracy=0
                values=eachClassWithMinRow[predictedClass]
                nn_index=values[0]
                distan=values[1]
                allacuracy.append(acuracy)

        print '\nID=',testRowNumber,'predicted=',predictedClass, ' true=',trueClass,' nn=',nn_index,' distance=',distan,' accuracy=',acuracy
        testRowNumber=testRowNumber+1

    allElements = len(allacuracy)
    totalAddition=0
    for k in allacuracy:
        totalAddition=totalAddition+k

    classification_accuracy= totalAddition/float(allElements)
    print 'Classification_accuracy:',classification_accuracy


####################
# common functions for all
####################
def findingClasswiseRows(someExample):
    myclasses, rows = classCounts(someExample)
    #print '\nmyclasses',myclasses
    newd={}
    for k,v in myclasses.iteritems():
            newd.setdefault(v,[]).append(k)

    keys = myclasses.keys()
    class_distribution={}
    for key in keys:
        temp=[]
        for row in someExample:
            if(key == row[-1]):
                temp.append(row)
        
        class_distribution[key]=temp

    return class_distribution,newd

def calculateEuclideanDistance(test_row, train_row):
    dis = 0
    for i in range(0, len(test_row)-1):
        dis = dis + ( test_row[i]-train_row[i] )**2

    ans = math.sqrt(dis)
    return ans

def classOfRow(trainingData, rowNumber):
    i=0
    for row in trainingData:
        if(i==rowNumber):
            return row[-1]

        i=i+1

def countClass(listOfClasses):
    counted={}
    for myclass in listOfClasses:
        if myclass in counted:
            counted[myclass] = counted.get(myclass)+1
        else:
            counted[myclass] = 1

    return counted

def calculateAverage(colum):
    return sum(colum)/float(len(colum))

def calculateStandardDeviation(colum):
    avg=calculateAverage(colum)
    variance = sum([pow(x-avg,2) for x in colum])/float(len(colum)-1)
    standardDeviation=math.sqrt(variance)
    return avg,standardDeviation

#returns the new Normalized attribute
def functionfv(myArray,mathArray):
    returnArray=[]
    for i in range(0,len(myArray) ):
        couple=mathArray[i]
        mean=couple[0]
        std=couple[1]
        #print 'mean', mean,' std',std,' myArray',myArray[i]
        values = 0
        if std == 0:
            values = 0
        else:
            values=(myArray[i]-mean)/float(std)
        returnArray.append(values)

    return returnArray

#returns classData
def classCounts(someExample):
    classData={}
    totalRows=0
    for row in someExample:
        totalRows=totalRows+1
        currentClass=row[-1]
        n=classData.get(currentClass,False)
        if n: #class example came up again
            n=n+1
            classData[currentClass]=n
        else: #class appeared first time
            classData[currentClass]=1

    #number of examples of each class
    #print 'classData',classData
    #print 'totalRows',totalRows
    return classData,totalRows

#return array containing one column
def select_column(someExample, anAttribute):
    myColumn=[]
    for row in someExample:
        myColumn.append(row[anAttribute])

    #print 'myColumn',myColumn
    return myColumn

def readFileReturnDataset(some_file,whole_dataset,classList):
    fout = open(some_file, 'r')
    try:
        for line in fout:
            stringlist = line.split()
            manyColumns = [int(x) for x in stringlist]
            numberOfAttributes=len(manyColumns) - 1
            classList.add(manyColumns[-1])
            whole_dataset.append( manyColumns )
    finally:
        fout.close()
    return whole_dataset,numberOfAttributes,classList

def main(argv):
    # Make sure we have enough command-line arguments
    #print 'Command line arguments:',argv

    if not(len(argv) == 4):
        print '4 command-line arguments are needed:'
        print('Usage: %s [training_file] [test_file] [k]' % argv[0])
        sys.exit(2)

    print 'Command line arguments:',argv
    training_file,test_file = argv[1:3]
    kkkiran=0
    if not(len(argv) == 4):
		print('Last argument for the k is not given.Exiting..' ) 
		sys.exit(2)
    else:
        kkkiran=int(argv[3])
        print 'K is :',kkkiran


    trainingExamples=[]
    trainingAttributes=[]
    trainingClassList=set()
    trainingExamples,numOfAttributes,trainingClassList=readFileReturnDataset(training_file,trainingExamples,trainingClassList)
    for i in range(0,numOfAttributes):
            trainingAttributes.append(i)

    print '\ntrainingClassList',trainingClassList
    global numofclasses
    numofclasses = max(trainingClassList)
    defaultdistributionArray=[0] * (numofclasses+1)

    #lets read test file too
    testExamples=[]
    testAttributes=[]
    testClassList=set()
    testExamples,numOfAttributes,testClassList=readFileReturnDataset(test_file,testExamples,testClassList)
    for i in range(0,numOfAttributes):
        testAttributes.append(i)

    #print '\ntestAttributes:',testAttributes
    #print 'testClassList:',testClassList

    normalizedTrainingExample = normalizeDatasets(trainingExamples,trainingAttributes)
    #print '\nnormalizedTrainingExample',normalizedTrainingExample
    normalizedTestExample = normalizeDatasets(testExamples,testAttributes)
    #print '\nnormalizedTestExample',normalizedTestExample

    print '\nLets start classification:'
    finalAccuracy=classificationByDistance( normalizedTrainingExample, trainingAttributes, normalizedTestExample, testAttributes,kkkiran )

    print 'Final Accuracy of training set over k:',kkkiran,' nearest neighbor classifier is:' ,finalAccuracy
    print 'Finished'

if __name__ == '__main__':
    main(sys.argv)