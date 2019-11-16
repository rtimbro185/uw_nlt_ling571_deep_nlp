"""#### LING 571: Homework #7 - Ryan Timbrook ##################
    Creating and Evaluating Models of Semantic Similarity
Author: Ryan Timbrook
Date: 03/1/2016

Program Name: hw7_dist_similarity.py - implements the creation and evaluation of the distributional
                                       similarity model as described above and invoked as:
    hw7_dist_similarity.{py|pl|etc} <window> <weighting> <judgment_filename> <output_filename>, where:
        <window>: An integer specifying the size of the context window for your model. For a window value of 2,
                  the window should span the two words before and the two words after the current word.
        <weighting>: A string specifying the weighting scheme to apply: "FREQ" or "PMI", where:
                    FREQ: Refers to "term frequency", the number of times the word appeared in the context of the target
                    PMI: (Positive) Point-wise Mutual Information: A variant of PMI where negative association
                    scores are removed and some simple smoothing is applied.
        <judgment_filename>: The name of the input file holding human judgments of the pairs of words
                    and their similarity to evaluate against, mc_similarity.txt. Each line is of the form:
                    wd1,wd2,similarity_score
        <output_filename>: The name of the output file with the results of computing similarities and correlations
                    over the word pairs. .
#########################################################################################################"""
import sys, nltk, re, string, math
import numpy as np
import scipy.stats.stats as stats
from collections import defaultdict, OrderedDict, Counter


########################################################################################################
#  Main Controller Function
#########################################################################################################
def main(argv):
    if argv is None:
        argv = sys.argv
    c = 0
    for arg in argv:
        print("hw7_dist_similarity.main: argv%d[%s]"%(c,argv[c]))
        c+=1

    #program input parameters
    window = argv[1]
    weighting = argv[2].upper()
    judgementFileName = argv[3]
    outputFile = 'hw7_sim_'+window+'_'+weighting+'_output.txt'

    #Read in corpus that forms the basis of the distributional model
    brownWords = preprocess()

    #Create corpus feature vector representations
    corpusMatrix = vectorRepresentation(window,weighting,brownWords)

    #Open output file for writing
    outputFile = open(argv[4],'a')

    #Read in file of human judgments
    humanJudgments = open(judgementFileName,'r')
    humanSimilarityScores = []
    computedSimilarityScores = []
    computedSimilarity = ''

    for line in humanJudgments.readlines():
        humanSimilarityScores.append(line.split(',')[2])
        if weighting == 'FREQ':
             computedSimilarityScores.append(frequency(corpusMatrix,brownWords,line,outputFile,10))
        elif weighting == 'PMI':
            computedSimilarityScores.append(pmi(corpusMatrix,brownWords,line,outputFile,10))
        else:
            print("no weighting")

    outputFile.write('\n\n')
    outputFile.write(computeCorrelation(humanSimilarityScores,computedSimilarityScores))

    outputFile.flush()
    outputFile.close()

## End main(argv)######################################################################################################

#######################################################################################################################
#   Read in corpus that forms the basis of the distributional model; remove punctuation and set words to lowercase
#######################################################################################################################
def preprocess():
    brown_clean_words = []
    brown_words = list(nltk.corpus.brown.words())[0:10000]#drop size down for dev

    for word in brown_words:
        clean = re.compile('[%s]' % re.escape(string.punctuation))
        cleanWord = clean.sub('',word)
        if cleanWord != str(''):
            brown_clean_words.append(cleanWord.casefold())

    return brown_clean_words
## End preprocess()####################################################################################################

#######################################################################################################################
#   Define feature vector representations for words in corpus based on window input size constraint
#
#######################################################################################################################
def vectorRepresentation(window,weighting,words):
    corpusDict = OrderedDict(((term,index) for index, term in list(enumerate(words))))
    matrix = defaultdict(list)
    nwords = len(words)
    featureVectors = [[0]*nwords for _ in words]

    try:
        for i, w, in enumerate(words):
            wCount = words.count(w)
            featureVector = featureVectors[i]
            featureDict = {}
            # Right of target word window list
            for r in rhsBoarder(i+1, int(window), nwords):
                featureVector[corpusDict[words[r]]] += 1
            # Left of target word window list
            for q in lhsBoarder(i-1, int(window), 0):
                featureVector[corpusDict[words[q]]] += 1

            matrix[w].append(featureVector)

    except Exception as e:
        print("caught exception %s" %str(e))

    return matrix

#######################################################################################################################
#   Utility functions for controlling word context neighborhood boards
#######################################################################################################################
def lhsBoarder(start, window, border):
    count = 0
    index = start
    while count < window and start-count >= border:
        yield index
        index -= 1
        count += 1

def rhsBoarder(start, window, border):
    count = 0
    index = start
    while count < window and start+count < border:
        yield index
        index += 1
        count += 1
#######################################################################################################################

#######################################################################################################################
#   Calculate Straight Frequency - the number of times the word appeared in the context of the target; divided by the
#                                   total times the target word appeared in the sample space
#######################################################################################################################
def frequency(matrix, corpus, line, outputFile, outputRange):
    topWords = []
    words = ['an','all'] #for test only
    #words.append(line.split(',')[0])
    #words.append(line.split(',')[1])

    wordTargetVectors = defaultdict(list)

    try:
        for targetWord in words:
            wDict = {key:value for key, value in matrix.items() if key == targetWord}
            termDict = defaultdict()

            #sum the total co-occurrences; the feature term appearing in context with the target word
            wordCount = len(wDict[targetWord])
            for rowIndex, row in enumerate(wDict[targetWord]):
                for colIndex, colValue in enumerate(row):
                    term = corpus[colIndex]
                    if term in termDict and colValue > 0:
                        value = termDict.get(term)
                        termDict[term] = int(value)+int(colValue)
                    elif colValue > 0:
                        termDict[term] = int(colValue)

            #determine frequency of a given feature word found in context with the target word; divide sum coocurrences by
            #total times the feature word appeard in sample space
            termFrequencyDict = {key:value/wordCount for key, value in termDict.items()}
            wordTargetVectors[targetWord].append({key:value for key, value in termFrequencyDict.items()})

            #sort highest occurrence order in reverse for output respose display
            frequencySorted = sorted(zip(termFrequencyDict.values(), termFrequencyDict.keys()), reverse=True)

            #construct output response in the format 'feature1:weight1'
            count = 0
            try:
                for t in frequencySorted:
                    if count < outputRange:
                        topWords.append(t[1]+":"+str(t[0]))
                    else:
                        break
                    count += 1
            except Exception as e:
                print("caught exception %s" %str(e))

            outputFile.write(targetWord+' ')
            for word in topWords:
                outputFile.write(word+' ')
            outputFile.write('\n')
            outputFile.flush()

        return computeSimilarity(wordTargetVectors, outputFile)

    except KeyError as ke:
        print("caught KeyError; target word[%s] not found"%targetWord)
        return None


#######################################################################################################################

#######################################################################################################################
#   Calculate PMI, Positive Pointwise Mutual Information
#######################################################################################################################
def pmi(matrix, corpus, line, outputFile, outputRange):
    topWords = []
    words = ['an','all'] #for test only
    #words.append(line.split(',')[0])
    #words.append(line.split(',')[1])
    wordTargetVectors = defaultdict(list)

    try:
        for targetWord in words:
            wDict = {key:value for key, value in matrix.items() if key == targetWord}
            termDict = defaultdict()
            featureWeightedDict = defaultdict()
            targetWordCount = len(wDict[targetWord])
            corpusCount = len(corpus)

            #sum the total co-occurrences; the feature term appearing in context with the target word
            for rowIndex, row in enumerate(wDict[targetWord]):
                for colIndex, colValue in enumerate(row):
                    term = corpus[colIndex]
                    if term in termDict and colValue > 0:
                        value = termDict.get(term)
                        termDict[term] = int(value)+int(colValue)
                    elif colValue > 0:
                        termDict[term] = int(colValue)

            #compute PMI
            pTargetWord = float(targetWordCount/corpusCount)
            termFrequencyDict = {key:float(value/targetWordCount) for key, value in termDict.items()}
            for featureWord in termFrequencyDict:
                featureWordCount = corpus.count(featureWord)
                pFeature = float(featureWordCount/corpusCount)
                pmiWeight = max(math.log2(float((pTargetWord+termFrequencyDict[featureWord])/(pTargetWord*pFeature))),0)
                featureWeightedDict[featureWord] = pmiWeight

            wordTargetVectors[targetWord].append({key:value for key, value in featureWeightedDict.items()})
            #sort highest occurrence order in reverse for output respose display
            frequencySorted = sorted(zip(featureWeightedDict.values(), featureWeightedDict.keys()), reverse=True)

            #construct output response in the format 'feature1:weight1'
            count = 0
            try:
                for t in frequencySorted:
                    if count < outputRange:
                        topWords.append(t[1]+":"+str(t[0]))
                    else:
                        break
                    count += 1
            except Exception as e:
                print("caught exception %s" %str(e))

            #write output to file
            outputFile.write(targetWord+' ')
            for word in topWords:
                outputFile.write(word+' ')
            outputFile.write('\n')
            outputFile.flush()

        return computeSimilarity(wordTargetVectors, outputFile)

    except KeyError as ke:
        print("caught KeyError; target word[%s] not found"%targetWord)
        return None
## End pmi()###########################################################################################################

#######################################################################################################################
#   Compute the similarity between two words, based on cosine similarity
#######################################################################################################################
def computeSimilarity(targetWordVectors, outputFile):
    similarity = float()
    targetWord1_w = targetWordVectors.popitem()
    targetWord1 = targetWord1_w[0]
    targetWord1_w = targetWord1_w[1]
    targetWord1_w = targetWord1_w[0]
    targetWord2_w = targetWordVectors.popitem()
    targetWord2 = targetWord2_w[0]
    targetWord2_w = targetWord2_w[1]
    targetWord2_w = targetWord2_w[0]

    targetWord1Count = len(targetWord1_w)
    targetWord1_c = defaultdict()
    targetWord2Count = len(targetWord2_w)
    targetWord2_c = defaultdict()

    #find the common set of features between the two word similarity
    commonFeatures = targetWord1_w.keys() & targetWord2_w.keys()
    for f_c in commonFeatures:
        targetWord1_c.update({key:value for key, value in targetWord1_w.items() if key==f_c})
        targetWord2_c.update({key:value for key, value in targetWord2_w.items() if key==f_c})

    sumTargetWord1_c = float(sum(targetWord1_c.values()))
    sumTargetWord2_c = float(sum(targetWord2_c.values()))

    #compute similarity
    similarity = (sumTargetWord1_c * sumTargetWord2_c) / (targetWord1Count + targetWord2Count)

    #print similarity score
    outputFile.write(targetWord1+','+targetWord2+':'+str(similarity)+'\n')
    outputFile.flush()
    return similarity
## End sim()###########################################################################################################

#######################################################################################################################
#   Compute the Pearson correlation between the similarity scores of the human-generated and computed
#######################################################################################################################
def computeCorrelation(simScores1,simScores2):
    correlation = float()
    correlation = stats.pearsonr(simScores1, simScores2)



    return 'Correlation:'+str(correlation)
## End sim()###########################################################################################################


#######################################################################################################################
# In-line process flow to call the main controller function
#######################################################################################################################
if __name__ == '__main__': main(sys.argv)