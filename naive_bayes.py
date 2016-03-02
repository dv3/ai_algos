#histograms, gaussians, or mixtures
import sys,math
numofclasses = 0

###################
# This is all histograms
###################
def histogramming(someExample,attributes,binnes):
    classData,totalRows = classCounts(someExample)
    #print 'attributes',attributes
    baapAtributes=[]
    for col in attributes:
        allBinsCurrentCol = binningofaColumn(someExample, col,binnes)
        #print '\nallBinsCurrentCol',allBinsCurrentCol
        anAttributesBinProbabilities={}
        anAttributesBinProbabilities = ClassProbabilityofBins(allBinsCurrentCol,classData)
        baapAtributes.append(anAttributesBinProbabilities)
        #print '\n anAttributesBinProbabilities',anAttributesBinProbabilities

    print '\n Output of Training phase'
    printTrainingPhase(baapAtributes)
    #print '\nbaapAtributes',baapAtributes
    return baapAtributes

def printTrainingPhase(trainingOutput):
    global numofclasses
    for c in range(0,numofclasses ):
        for atr in range(0,len(trainingOutput)):
            aColumn=trainingOutput[atr] #first index in list is first attribute
            for eachBin in aColumn:
                #print 'eachBin',eachBin
                actualDict={}
                actualDict=aColumn[eachBin]
                #print 'actualDict',actualDict
                temp=actualDict.values()
                probDistrib = temp[0]
                print 'Class=',c,' attribute=',atr, ' bin=',eachBin,' P(bin|class)=',probDistrib[c]                   

#calculates each class probability for a bin
def ClassProbabilityofBins(binsOfaColumn,allClassData):
    #global numofclasses
    #distributionArray=[0] * (numofclasses+1)
    # creating a bigger array. looking at unknown future 
    #binClasses = {}
    count = 0
    for aBin in binsOfaColumn:
        global numofclasses
        distributionArray=[0] * (numofclasses+1)
        actualDataDict={}
        actualDataDict=binsOfaColumn[aBin]
        keyss = actualDataDict.keys()
        tupleKey = keyss[0]
        rowsinListForm=actualDataDict.values()
        rowsofthisBin=rowsinListForm[0]
        classDataOfaBin,totalRowsInaBin = classCounts(rowsofthisBin)
        #print 'classDataOfaBin',classDataOfaBin
        for k in classDataOfaBin:
            itsCountInaBin=classDataOfaBin[k]
            classTotal = allClassData[k]
            #print 'itsCountInaBin',itsCountInaBin,' classTotal',classTotal
            divides= itsCountInaBin/float(classTotal)
            #print 'divides',divides
            #divide by all classes data rows
            distributionArray[k]=divides

        temp={tupleKey: distributionArray }
        binsOfaColumn[count] = temp
        #binClasses[count]=distributionArray
        count+=1

    #print 'binsOfaColumn',binsOfaColumn
    return binsOfaColumn 

#creates bin out of a column
#binGroups {0: {(10.0, 27.5): [[10, 90, 8], [20, 80, 2]]}, 1: {(27.5, 45.0): [[30, 70, 1], [40, 60, 4]]} }
def binningofaColumn(someExample,someColumn,bins):
    localExample=someExample
    currentCol=select_column(localExample,someColumn)
    #print 'currentCol',currentCol
    numb=max(currentCol)
    bigValue=math.ceil(numb)
    numb=min(currentCol)
    smallValue=math.floor(numb)
    jee=(bigValue+smallValue)/float(bins)

    #print 'bigValue',bigValue,'smallValue',smallValue,'jee',jee
    binGroups={}
    for bin in range(0,bins):
        eachBin={}
    	binList=[]
    	low=(smallValue+(jee*bin ))
    	high=(smallValue+(jee*(bin+1) ) )
        lisst=[low,high]
        keyss=tuple(lisst)
    	#print 'bin',bin,'low',low,'high',high
    	for row in someExample:
    		colValue=row[someColumn]
    		#print 'colValue',colValue
    		if (colValue >= low and colValue < high) :
    			#print 'colValue',colValue,'row',row
    			binList.append(row)

    	#binGroups[bin]=binList
    	eachBin[keyss]=binList
        binGroups[bin]=eachBin

    #print 'binGroups',binGroups
    return binGroups

def classificationUsingHistogram( answer1 , probOfAllClasses , testExamples , testAttributes ):
    allacuracy=[]
    rowNumber=0
    for row in testExamples:
        #print 'row',row
        #finalDistibutionOfaRow=[]
        attrDistri=[]
        for i in range(0,len(row)-1): #dont touch class
            aColumn={}
            aColumn=answer1[i] #first index in list is first attribute
            for eachBin in aColumn:
                actualDict={}
                actualDict=aColumn[eachBin]
                #print 'actualDict',actualDict
                temp=actualDict.keys()
                binRanges=temp[0]
                low=binRanges[0]
                high=binRanges[1]
                #print 'high',high,'low',low,'row[i]',row[i]
                if (row[i] >= low and row[i] < high) :
                    temp=actualDict.values()
                    probDistrib = temp[0]
                    attrDistri.append(probDistrib )
                    #attrDistri=[row[i]*h for h in probDistrib]
                    #finalDistibutionOfaRow.append(attrDistri)

        #print 'finalDistibutionOfaRow',finalDistibutionOfaRow
        global numofclasses
        decidingArrayProb=[]
        for classs in range(0,numofclasses):
            currentClass=select_column(attrDistri,classs)
            #print 'currentClass',currentClass
            xGivenClass=reduce(lambda x, y: x*y, currentClass)
            PofClass=probOfAllClasses[classs]
            #print 'PofClass',PofClass,'xGivenClass',xGivenClass
            finalProbOfaClass=xGivenClass*PofClass
            decidingArrayProb.append(finalProbOfaClass)

        #print 'decidingArrayProb',decidingArrayProb
        #maxProb=max(decidingArrayProb)
        #predictedClass=decidingArrayProb.index(maxProb)
        probabilityDistributionDict={}
        for i in range(0,len(decidingArrayProb) ):
            probabilityDistributionDict[i]=decidingArrayProb[i]

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
                predictedClass=decidingArrayProb[0]
                acuracy=0
                allacuracy.append(acuracy)

        print '\nID=',rowNumber,' predicted=',predictedClass, ' probability=',maxProbability,' true=',trueClass,' accuracy=',acuracy
        rowNumber=rowNumber+1

    allElements = len(allacuracy)
    totalAddition=0
    for k in allacuracy:
        totalAddition=totalAddition+k

    classification_accuracy= totalAddition/float(allElements)
    print 'Classification_accuracy:',classification_accuracy
    return classification_accuracy


####################
# From here its for gaussian
####################
def printGaussian(cal_gaussi):
    for key,value in cal_gaussi.iteritems():
        i=0
        for attr in value:
            mean=attr[0]
            std=attr[1]
            print 'Class=',key,' attribute=',i, ' mean=',mean,' std=',std
            i=i+1

def calculateGaussianProbability( trainingExamples , testExamples, trainingAttribute ,prob_class):
    tempClassDistribution=findingClasswiseRows(trainingExamples)
    cal_gaussian=calculateSum(tempClassDistribution, trainingAttribute )

    print 'Training Phase Output:'
    printGaussian(cal_gaussian)

    print 'Testing Phase starts'
    length_val = len(cal_gaussian[1])
    #print 'length_val',length_val
    gaussian=1  
    predicated_class=[]

    allacuracy=[]
    rowNumber=0

    for row in testExamples:
        prob_rowgivenclass=[]
        for key,value in cal_gaussian.iteritems(): 
            #print 'value',value
            gaussian=1
            for i in range(0,length_val):
                ourNumbers = value[i]
                mean = ourNumbers[0]
                std = ourNumbers[1]
                #print 'row[i]',i,'mean,std',row[i],mean,std
                gaussian = gaussian*calculateGaussian(row[i],mean,std)
                #print 'gaussian',gaussian
    
            prob_rowgivenclass.append(gaussian*prob_class[key])  

        #max_inter = max(prob_rowgivenclass)
        #predicated_class.append(prob_rowgivenclass.index(max_inter)))
        #print "predicated_class", predicated_class
        #print 'prob_rowgivenclass',prob_rowgivenclass

        probabilityDistributionDict={}
        for i in range(0,len(prob_rowgivenclass) ):
            probabilityDistributionDict[i]=prob_rowgivenclass[i]

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
                predictedClass=prob_rowgivenclass[0]
                acuracy=0
                allacuracy.append(acuracy)

        print 'ID=',rowNumber,' predicted=',predictedClass, ' probability=',maxProbability,' true=',trueClass,' accuracy=',acuracy
        rowNumber=rowNumber+1

    allElements = len(allacuracy)
    totalAddition=0
    for k in allacuracy:
        totalAddition=totalAddition+k

    classification_accuracy= totalAddition/float(allElements)
    print 'Classification_accuracy:',classification_accuracy
    return classification_accuracy

def findingClasswiseRows(someExample):
    myclasses, rows = classCounts(someExample)
    keys = myclasses.keys()
    class_distribution={}
    for key in keys:
        temp=[]
        for row in someExample:
            if(key == row[-1]):
                temp.append(row)
        
        class_distribution[key]=temp

    return class_distribution

def calculateSum(class_distribution, trainingAttributes):
    cal_gaussian = {}
    for key, value in class_distribution.iteritems():
        attribute_values=[]
        for attrib in trainingAttributes:
            column = select_column(value,attrib)
            #if key == 4:
                #print 'attrib',attrib, ' value',value
                #print '##############3'
            avg,std = calculateStandardDeviation(column)
            attribute_values.append([avg,std])
            #print 'attribute_values',attribute_values

        cal_gaussian[key] = attribute_values

    #print '\ncal_gaussian',cal_gaussian
    return cal_gaussian

def calculateAverage(colum):
    return sum(colum)/float(len(colum))

def calculateStandardDeviation(colum):
    avg=calculateAverage(colum)
    variance = sum([pow(x-avg,2) for x in colum])/float(len(colum)-1)
    standardDeviation=math.sqrt(variance)
    return avg,standardDeviation

def calculateGaussian(x, mean, stdev):
    #print 'x, mean, stdev',x, mean, stdev
    if stdev == 0 : 
        return 0

    exponent = math.exp(-(math.pow(x-mean,2)/(2*math.pow(stdev,2))))
    return (1 / (math.sqrt(2*math.pi) * stdev)) * exponent


####################
# this part is for mixture of gaussians
# ##################

def printMixGaussian(someDict):
    for key,value in someDict.iteritems():
        i=0
        for attr in value:
            mean=attr[0]
            std=attr[1]
            print 'Class=',key,' attribute=',i, ' mean=',mean,' std=',std
            i=i+1

def gaussianTesting( trainingExamples, testExamples,probOfAllClasses,number,trainingAttributes):
    allacuracy=[]
    rowNumber=0
    baapDict=mixtureOfGaussians(trainingExamples,number,trainingAttributes)
    print 'Output of training phase:'
    printMixGaussian(baapDict)

    print 'Testing phase starts'

    for row in testExamples:
        probArray=[]
        distri=[]
        for key, value in baapDict.iteritems():
            for i in range(0,len(row)-1): 
                for val in value:
                    attribGivenClass = val[3]*calculateGaussian(row[i],val[0],val[1])
                    probArray.append(finalGauss)
            xGivenClass = reduce(lambda x, y: x*y, probArray)
            probClass = xGivenClass* probOfAllClasses[key]
            distri.append(probClass)

        #print 'distri',distri
        probabilityDistributionDict={}
        for i in range(0,len(distri) ):
            probabilityDistributionDict[i]=distri[i]

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
                predictedClass=distri[0]
                acuracy=0
                allacuracy.append(acuracy)

        print 'ID=',rowNumber,' predicted=',predictedClass, ' probability=',maxProbability,' true=',trueClass,' accuracy=',acuracy
        rowNumber=rowNumber+1

    allElements = len(allacuracy)
    totalAddition=0
    for k in allacuracy:
        totalAddition=totalAddition+k

    classification_accuracy= totalAddition/float(allElements)
    print 'Classification_accuracy:',classification_accuracy
    return classification_accuracy
        

#First is same, find classwiserows
def mixtureOfGaussians(someExample,number,trainingAttributes):
    class_distribution=findingClasswiseRows(someExample)
    std_dev = 1
    w = 1/float(number)
    dick={}
    for key, value in class_distribution.iteritems():
        attriList=[]
        for attrib in trainingAttributes:
            columnVals = select_column(value,attrib)
            l = max(columnVals)
            s = min(columnVals)
            g= (l-s)/float(number)
            gaussian=[]
            for i in range(0,number):
                mi = s + (i*g) +(g/2)
                gaussianVal=[]
                #e_step(columnVals, mi, std_dev, w)
                #perform em algo here and get real values to store
                gaussianVal.append(mi)
                gaussianVal.append(std_dev)
                gaussianVal.append(w)
                gaussian.append(gaussianVal)
                
            attriList.append(gaussian)
            
        dick[key]=attriList

    baapData=em_algorithm(class_distribution,dick,trainingAttributes)
    return baapData

    
def em_algorithm(class_distribution,dick,trainingAttributes):
    #print 'em_algorithm'
    bigData={}
    for key, value in class_distribution.iteritems():
        for classes, gaussians in dick.iteritems():
            attriList=[]
            temp=[]
            for attrib in trainingAttributes:
                columnVals = select_column(value,attrib)
                bigGaussianColumn=gaussians[attrib]
                answer=emAlgo(columnVals, bigGaussianColumn)
                temp.append(answer)

            bigData[key]=temp

    return bigData

def emAlgo(columnVals, bigGaussianColumn):
    #print 'emAlgo'
    flag=1
    answer2=None
    for i in range(0,2):
        #print '###########i',i
        if flag ==1:
            answer1= e_step(columnVals, bigGaussianColumn)
        else:
            answer1= e_step(columnVals, answer2)

        answer2=m_step(columnVals, answer1)
        #print '### answer2 ###',answer2
        flag=0

    return answer2


def e_step(columnVals, values):
    #print 'e_step values'
    i=0
    estep=[]
    for colVal in columnVals:
        weightedNarray=[]
        pijArray=[]

        if i == 2:
            break

        for value in values:
            nixj = calculateGaussian(colVal,value[0],value[1])
            weightedN = nixj*value[2]
            weightedNarray.append(weightedN)
            #print 'weightedNarray',weightedNarray

        pxj = sum(weightedNarray)
        #print 'pxj',pxj

        for i in weightedNarray:
            pij = i/float(pxj)
            pijArray.append(pij)
        
        estep.append( pijArray)
        i+=1

    #print 'end of estep',estep
    return estep

def m_step(columnVals, estep):
    #print 'm_step'
    i=0
    weights=0
    for r in estep:
        for c in r:
            weights=weights+c

    bigGaussian=[]
    for value in estep:
        i=0
        for colVal in columnVals:
            i+=1
            numer=denomi=0
            gaussian=[]
            for jj in value:
                numer = jj*colVal
                denomi=denomi+jj

            newMean=numer/float(denomi)
            variance= (math.pow(colVal-newMean,2)) / float(denomi)
            std=math.sqrt(variance)
            gaussian.append(newMean)
            gaussian.append( std )
            gaussian.append( denomi/weights )
            bigGaussian.append(gaussian)
            if i ==1:
                break

    #print 'end of mstep',bigGaussian
    return bigGaussian

####################
# common functions for all
####################

def allClassProbability(someExample):
    classData,totalRows = classCounts(someExample)
    classProbabilityDistribution={}
    for k in classData:
        itsCount=classData[k]
        divides= itsCount/float(totalRows)
        classProbabilityDistribution[k]=divides

    #print 'classProbabilityDistribution',classProbabilityDistribution
    return classProbabilityDistribution,totalRows 

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

    if len(argv) > 5 or len(argv) < 4:
        print 'Atleast 4 command-line arguments are needed:'
        print('Usage: %s [training_file] [test_file] [option] [*number]' % argv[0])
        sys.exit(2)

    print 'Command line arguments:',argv
    training_file,test_file,bayesOptions = argv[1:4]

    listofOptions=['histograms','gaussians','mixtures']
    howMany=0

    if not bayesOptions in listofOptions:
        print('%s is an unrecognized options.Please select from:%s' % (bayesOptions,listofOptions) )
        sys.exit(2)

    if bayesOptions in ['histograms','mixtures']:
    	if not(len(argv) == 5):
    		print('Last argument for the number of histogram or mixture not given.Exiting..' ) 
    		sys.exit(2)
    	else:
    		howMany=int(argv[4])
    		print 'Fourth argument:',howMany

    #read training sets
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

    #lets read test file too
    testExamples=[]
    testAttributes=[]
    testClassList=set()
    testExamples,numOfAttributes,testClassList=readFileReturnDataset(test_file,testExamples,testClassList)
    for i in range(0,numOfAttributes):
        testAttributes.append(i)

    #print '\ntestAttributes:',testAttributes
    #print 'testClassList:',testClassList

    probOfAllClasses,totallyRows=allClassProbability(trainingExamples)
    #print 'probOfAllClasses',probOfAllClasses

    if bayesOptions == 'histograms':
    	answer1 = histogramming(trainingExamples,trainingAttributes,howMany)
    	print '\nLets start classification:'
        finalAccuracy=classificationUsingHistogram( answer1 , probOfAllClasses , testExamples , testAttributes )
        print 'Final Accuracy of training set over histograms of bins ', howMany, ' is:' ,finalAccuracy
    elif bayesOptions == 'gaussians':
        finalAccuracy=calculateGaussianProbability( trainingExamples, testExamples, trainingAttributes,probOfAllClasses)
        print 'Final Accuracy of training set over Gaussians is:' ,finalAccuracy
    elif bayesOptions == 'mixtures':
        finalAccuracy=gaussianTesting( trainingExamples, testExamples,probOfAllClasses,howMany,trainingAttributes)
        print 'Final Accuracy of training set over mixture of ', howMany, ' Gaussians is:',finalAccuracy
    else:
        print('%s is an unrecognized tree options.Please select from:%s' % (bayesOptions,listofOptions) )
        sys.exit(2)

    

    #finalAccuracy=classification(testExamples,totalTrees)
    #print 'final Accuracy of training set over ', treeCounts , ' trees= ',finalAccuracy
    print 'Finished'

if __name__ == '__main__':
    main(sys.argv)