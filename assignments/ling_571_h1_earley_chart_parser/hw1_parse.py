"""LING 571 - Homework #1 - Ryan Timbrook ################################################################################################
Parses test sentences based on a grammar, that was constructed as part of this homework assignment, and analyze the results
Requirements:
-Load your grammar
-Build a parser for your grammar using nltk.parse.EarleyChartParser
-Read in the example sentences
-For each example sentence, output to a file: the sentence itself; the simple bracketed structure parse(s); and the number of parses for that sentence
-Print the average number of parses per sentence obtained by your grammar
##########################################################################################################################################################"""
import nltk
import sys
import io
import re
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.tokenize import wordpunct_tokenize
from nltk.tokenize import TreebankWordTokenizer
from subprocess import *

#print("Number of arguments:",len(sys.argv),"arguments.")

#Get main argument list from command line
grammarCfgFileName = sys.argv[1]
sentencesToParseFileName = sys.argv[2]
outputFileName = sys.argv[3]

#print("Grammar Cfg File Name is [%s]" %grammarCfgFileName)
#print("Sentences to Parse File Name is [%s]" %sentencesToParseFileName)
#print("Output File Name is [%s]" %outputFileName)

#Define a couple of functions to test behavior
#Open the Example Sentences file and read in it's content
################################################################
def openSentencesToParse(fileName):
    sentencesList = []
    try:
        fsentences = open(sentencesToParseFileName,'r')
        sentences = fsentences.readlines()

        for sentence in sentences:
            sentence = sentence.replace('\n','')
            #sentence = re.sub(r"\,|\?|\.|\n","",sentence)
            print("Formatted Sentence: [%s]"%sentence)
            sentencesList.append(sentence)

        fsentences.close()
    except Exception as e:
        print("*****ERROR*****: Caught Exception; [%s]"%str(e))

    return sentencesList
#################################################################

##############################################################
#Parser that will read in a grammar file and sentence to parse
###############################################################
def parser(grammar,sentence,outputFileName):
    print("\nParser.Sentences: Sentence to parse [ %s ]" %sentence)
    #print("Output File Name [%s]" %outputFileName)
    i = 0
    try:
        #Open Output file for writing
        file = open(outputFileName,'a')

        #write out the sentence to be parsed
        #file.write(sentence+"\n")
        file.write(sentence)

        #tokenize the sentence
        #tokens = nltk.word_tokenize(sentence)
        #tokens = sent_tokenize(sentence)
        #tokens = word_tokenize(sentence)
        #tokens = wordpunct_tokenize(sentence)
        tokens = TreebankWordTokenizer().tokenize(sentence)

        print("Parser.SentenceTokens: [%s]"%tokens)

        #Create a parser from the grammar file
        hw1Parser = nltk.parse.EarleyChartParser(grammar)
        for item in hw1Parser.parse(tokens):
            i += 1
            print("Parser.EarleyChartParser: item [%s]"%item)
            #write out the simple parse chart
            file.write(str(item))
            file.write("\n")

        print("Number of parses: [%d]" %i)
        file.write("\nNumber of parses: %d\n" %i)
        file.write("\n")

        file.close()

    except Exception as e:
        print("*****ERROR*****: Caught Exception; [%s]"%str(e))

    return i
###################################################################

#Execute Functions
#Read in the sentences file to parse
sentenceList = openSentencesToParse(sentencesToParseFileName)
print("Sentence List To Parse: %s \n"%str(sentenceList))

#Load the Grammar File
print("Loading Grammar File: [%s]"%grammarCfgFileName)
grammar = nltk.data.load(grammarCfgFileName)
grammarCFG = nltk.data.show_cfg(grammarCfgFileName)
print("Grammar [%s] CFG: %s\n"%(grammarCfgFileName,str(grammarCFG)))
#print(nltk.do.show_cfg(grammarCfgFileName))

print("Is grammar in CNF form? [%s]"%grammar.is_chomsky_normal_form())
print("Is grammar binarised? [%s]"%grammar.is_binarised())


#Loop through all of the sentences in the specified file
averageParses = 0.0
parseList = []
count = 0
try:
    while count < len(sentenceList):
        print("Count Index is [%d]" %count)
        parseCount = parser(grammar,sentenceList[count],outputFileName)
        parseList.append(parseCount)
        count += 1

    averageParses = float(sum(parseList))/len(parseList)
    print("Average number of parses: %f" %averageParses)

    file = open(outputFileName,'a')
    file.write("\n")
    file.write("Average number of parses: %f" %averageParses)
    file.close()

except Exception as e:
    print("*****ERROR*****: Caught Exception; [%s]"%str(e))












