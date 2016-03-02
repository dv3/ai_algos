import sys,math
from binary_tree import *
from random import randint
isRandom = False
numofclasses = 0
#global items if any


def DecisionTreeLearner(example,attribute,default):
    examples_left=[]
    examples_right=[]
    #print 'example',example

    if len(example) == 0:
        print 'Length of example: 0'
        newTree=BinaryTree(-1,-1,-1,default)
        return newTree
    elif all_same_class(example):
        probabilityDistributionsArray=[]
        probabilityDistributionsArray=distributions(example)
        newTree=BinaryTree(-1,-1,-1,probabilityDistributionsArray)
        return newTree
    else:
        best_attribute=best_threshold=max_gain=0
        if isRandom:
            best_attribute,best_threshold,max_gain=choose_attribute_randomzied(example,attribute)
            #print 'best_attribute:',best_attribute,'best_threshold:',best_threshold,'max_gain',max_gain
        else:
            best_attribute,best_threshold,max_gain=choose_attribute(example,attribute)
            #print 'best_attribute:',best_attribute,'best_threshold:',best_threshold,'max_gain',max_gain

        examples_left,examples_right = splitIntoChildren(example,best_attribute,best_threshold)
        #print 'examples_left,examples_right',examples_left,examples_right

        probabilityDistributionsArray=[]
        probabilityDistributionsArray=distributions(example)
        #pruning
        if len(examples_left) < 50 :
            newTree=BinaryTree(-1,-1,-1,probabilityDistributionsArray)
            print 'left < 50'
            #printTree(newTree)
            return newTree

        if len(examples_right) < 50 :
            newTree=BinaryTree(-1,-1,-1,probabilityDistributionsArray)
            print 'right< 50'
            #printTree(newTree)
            return newTree

        if (len(examples_left) >= 0 and  len(examples_right) >= 0 ):
            newTree=BinaryTree(best_attribute,best_threshold,max_gain,probabilityDistributionsArray)

            leftSubtree = DecisionTreeLearner(examples_left,attribute,probabilityDistributionsArray)
            #printTree(leftSubtree)

            rightSubtree= DecisionTreeLearner(examples_right,attribute,probabilityDistributionsArray)
            #printTree(rightSubtree)

            newTree.left=leftSubtree
            newTree.right=rightSubtree
            return newTree

def choose_attribute(examples,attributes):
    max_gain = best_attribute = best_threshold = -1

    for currentAttribute in attributes:
        #print '\nin choose_attribute: currentAttribute:',currentAttribute
        attribute_values = select_column(examples, currentAttribute)

        minAttriValues=min(attribute_values)
        #print 'minAttriValues',minAttriValues
        maxAttriValues=max(attribute_values)
        #print 'maxAttriValues',maxAttriValues

        # 1,51
        for k in range(1,51):
            threshold=minAttriValues + float((k * (maxAttriValues - minAttriValues))/float(51))
            #print 'threshold',threshold
            #threshold=88
            gain=information_gain(examples,currentAttribute,threshold)
            if gain > max_gain:
                max_gain=gain
                best_attribute=currentAttribute
                best_threshold=threshold

    #print best_attribute,best_threshold,max_gain
    return best_attribute,best_threshold,max_gain

def choose_attribute_randomzied(examples,attributes):
    max_gain = best_attribute = best_threshold = -1

    currentAttribute = randint(0,attributes[-1])
    #print '\nin choose_attribute_randomzied: currentAttribute:',currentAttribute
    attribute_values = select_column(examples, currentAttribute)

    minAttriValues=min(attribute_values)
    #print 'minAttriValues',minAttriValues
    maxAttriValues=max(attribute_values)
    #print 'maxAttriValues',maxAttriValues

    # 1,51
    for k in range(1,51):
        threshold=minAttriValues + float((k * (maxAttriValues - minAttriValues))/float(51))
        #print 'threshold',threshold
        #threshold=88
        gain=information_gain(examples,currentAttribute,threshold)
        if gain > max_gain:
            max_gain=gain
            best_attribute=currentAttribute
            best_threshold=threshold

    #print best_attribute,best_threshold,max_gain
    return best_attribute,best_threshold,max_gain

def information_gain(example,attri,thresho):
    #entropy from whole example
    papaEntropy,papaClasses=calculateEntropy(example)
    #print 'papaEntropy,papaClasses',papaEntropy,papaClasses

    #entropy from reduced examples
    leftChildExample,rightChildExample = splitIntoChildren(example,attri,thresho)
    #print 'leftChildExample,rightChildExample',leftChildExample,rightChildExample

    leftChildEntropy,leftClasses = calculateEntropy(leftChildExample)
    #print 'leftChildEntropy,leftClasses',leftChildEntropy,leftClasses

    rightChildEntropy,rightClasses = calculateEntropy(rightChildExample)
    #print 'rightChildEntropy,rightClasses',rightChildEntropy,rightClasses

    informationGain = (papaEntropy - ((leftClasses/float(papaClasses)) * float(leftChildEntropy) ) - ( (rightClasses/float(papaClasses)) * float(rightChildEntropy) ))
    #print 'informationGain',informationGain
    return informationGain

def splitIntoChildren(parentExamples,attribute,thresho):
    example=parentExamples
    leftChildExample=[]
    rightChildExample=[]

    for row in example:
        if row[attribute] < thresho :
            leftChildExample.append(row)
        else:
            rightChildExample.append(row)

    #print 'parent divorced'
    return leftChildExample,rightChildExample

def distributions(someExample):
    classData,totalRows = classCounts(someExample)
    #print 'classData,totalRows',classData,totalRows
    global numofclasses
    distributionArray=[0] * (numofclasses+1)
    # creating a bigger array. looking at unknown future 

    for k in classData:
        itsCount=classData[k]
        probability=itsCount / float(totalRows)
        distributionArray[k] = probability

    #print 'distributionArray',distributionArray
    return distributionArray

def calculateEntropy(someExample):
    classData,totalRows = classCounts(someExample)
    entrops=0
    for k in classData:
        itsCount=classData[k]
        divides= itsCount/float(totalRows)
        entrops= entrops + float((- divides) * (math.log(divides,2)))

    #print 'entrops',entrops
    #differentClasses = len(classData)
    return entrops,totalRows

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
def select_column(example, anAttribute):
    myColumn=[]
    for row in example:
        myColumn.append(row[anAttribute])

    #print 'myColumn',myColumn
    return myColumn

def all_same_class(examples):
    firstClass=examples[0][-1]
    flags=False
    for row in examples:
        if row[-1] == firstClass:
            flags=firstClass
        else:
            flags=False

    return flags

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

def fetch_distribution(obj, tree):
    if tree.featureID == -1 :
        return tree.distributions
    if obj[tree.featureID] < tree.threshold :
        return fetch_distribution(obj, tree.left)
    else:
        return fetch_distribution(obj, tree.right)

def classification(testExamples,treeList):
    rowNumber=0
    allacuracy=[]
    
    for row in testExamples:
        listOfTreePredictions=[]
        for eachTree in treeList:
            probabilityDistributions=[]
            probabilityDistributions=fetch_distribution(row[0:-1],eachTree)
            listOfTreePredictions.append(probabilityDistributions )

        #print 'listOfTreePredictions:',listOfTreePredictions
        eachColAdded=[sum(i) for i in zip(*listOfTreePredictions)]
        rowsOflistOfTreePredictions= len(listOfTreePredictions)
        #print 'rowsOflistOfTreePredictions',rowsOflistOfTreePredictions
        #average of all columns
        averageDistributionArray=[]
        averageDistributionArray=[x/float(rowsOflistOfTreePredictions) for x in eachColAdded]
        #print 'averageDistributionArray',averageDistributionArray

        probabilityDistributionDict={}
        for i in range(0,len(averageDistributionArray) ):
            probabilityDistributionDict[i]=averageDistributionArray[i]

        #print 'answer',answer
        #maxClass = max([ (answer[i],i) for i in answer])[1]
        newd={}
        for k,v in probabilityDistributionDict.iteritems():
            newd.setdefault(v,[]).append(k)

        maxProbability=max(newd)
        maxClasses=newd[maxProbability]
        trueClass= row[-1]
        acuracy=0
        #lets match last column element with maxClasses
        if len(maxClasses) == 1:
            predictedClass=maxClasses[0]
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
                allacuracy.append(acuracy)
            else: # no classes match from tied ones
                predictedClass=averageDistributionArray[0]
                acuracy=0
                allacuracy.append(acuracy)

        print 'ID=',rowNumber,' predicted=',predictedClass,' true=',trueClass,' accuracy=',acuracy
        rowNumber=rowNumber+1

    allElements = len(allacuracy)
    totalAddition=0
    for k in allacuracy:
        totalAddition=totalAddition+k

    classification_accuracy= totalAddition/float(allElements)
    print 'Classification_accuracy:',classification_accuracy
    return classification_accuracy

def main(argv):
    # Make sure we have enough command-line arguments

    if len(argv) != 4:
        print '3 command-line arguments are needed:'
        print('Usage: %s [training_file] [test_file] [option]' % argv[0])
        sys.exit(2)

    print 'Command line arguments:',argv
    training_file,test_file,treeOptions = argv[1:4]
    listofOptions=['optimized','randomized','forest3','forest15']

    if not treeOptions in listofOptions:
        print('%s is an unrecognized tree options.Please select from:%s' % (treeOptions,listofOptions) )
        sys.exit(2)

    #read training sets
    treeCounts=1
    global isRandom
    if treeOptions == 'optimized':
        treeCounts=1
        isRandom = False
    elif treeOptions == 'randomized':
        treeCounts=1
        isRandom = True
    elif treeOptions == 'forest3':
        treeCounts=3
        isRandom = True
    elif treeOptions == 'forest15':
        treeCounts=15
        isRandom = True
    else:
        print('%s is an unrecognized tree options.Please select from:%s' % (treeOptions,listofOptions) )
        sys.exit(2)

    #print read training set data
    trainingExamples=[]
    trainingAttributes=[]
    trainingClassList=set()
    trainingExamples,numOfAttributes,trainingClassList=readFileReturnDataset(training_file,trainingExamples,trainingClassList)
    for i in range(0,numOfAttributes):
            trainingAttributes.append(i)

    print 'trainingClassList',trainingClassList
    global numofclasses
    numofclasses = max(trainingClassList)
    defaultdistributionArray=[0] * (numofclasses+1)

    individualTreeAccuracy=0
    treeAccuracyArray=[]
    totalTrees=[]

    for eachTree in range(0,treeCounts) :
        print '\nCalling DecisionTreeLearner to create training tree:',eachTree+1
        tree=DecisionTreeLearner(trainingExamples,trainingAttributes,defaultdistributionArray)
        totalTrees.append(tree)
        print '\nTraining Phase Output in BFS:'
        tree.BFS(eachTree+1)

    print '\nList of tree are ready:'
    #starting with test file
    testExamples=[]
    testAttributes=[]
    testClassList=set()
    testExamples,numOfAttributes,testClassList=readFileReturnDataset(test_file,testExamples,testClassList)
    for i in range(0,numOfAttributes):
        testAttributes.append(i)

    #print '\ntestAttributes:',testAttributes
    #print 'testClassList:',testClassList

    finalAccuracy=classification(testExamples,totalTrees)
    print 'final Accuracy of training set over ', treeCounts , ' trees= ',finalAccuracy
    print 'Finished'

if __name__ == '__main__':
    main(sys.argv)