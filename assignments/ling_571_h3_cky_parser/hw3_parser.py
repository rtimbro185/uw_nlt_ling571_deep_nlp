"""LING 571 - Homework #3 - Ryan Timbrook ################################################################################################
Implementing a CKY Parser

Based on the material in the lectures and text, develop an implementation of the CKY algorithm that will parse input sentences using a CNF grammar.
You may use existing implementations of the data structures to represent the grammar in NLTK or other NLP toolkits (e.g. the Stanford parser),
but you must implement the parsing algorithm yourself.
Your algorithm must return all parses derived for the input sentences given the grammar.
Note: You do not need to convert output trees back out of CNF.

Parsing with your CKY parser

The program you submit should do the following:
    Load the CNF grammar.
    Read in the example sentences.
    For each example sentence, output to a file:
        the sentence itself
        the simple bracketed structure parse(s) based on your implementation of the CKY algorithm, and
        the number of parses for that sentence.
#########################################################################################################################################################"""
import nltk, sys, copy, pprint
from utils import common_utils
from parsers.cky import CKYParser as cky
from parsers.do import grammar_do
from array import array

##Get invokation parameter values
grammarFileName = sys.argv[1]
testSentencesName = sys.argv[2]
outputFileName = sys.argv[3]
print("Grammar file name [%s], test sentence name [%s], output file name [%s]"%(grammarFileName,testSentencesName,outputFileName))

#1 - Read in and load CNF grammar file
grammar = common_utils.openGrammarFile(grammarFileName)
print("**Grammar [%s] loaded, start symbol is [%s], is CNF form? [%s], is in Binary Form? [%s]"%(sys.argv[1], grammar.start(), grammar.is_chomsky_normal_form(), grammar.is_binarised()))
#2 - Read in the example sentences
testSentences = common_utils.openSentencesClean(testSentencesName)

#2.1 - Initialize grammar data object
grammarDO = grammar_do.GrammarDO(grammar)


#3 - Execute custome CKY algorithm implementation on test sentence
for sentence in testSentences:
    words = nltk.wordpunct_tokenize(sentence)
    treeMatrix = cky.ckyRecognizer(list(words),grammarDO)
    parse = cky.completeParse(treeMatrix,grammar.start(),len(words))
    tempParse = ''
    parseCount = 0
    for i in parse:
        if i == grammar.start()._symbol:
            parseCount +=1
        tempParse = tempParse+i

    tempOut = ['\n',sentence,tempParse,"Number of parses: %d"%parseCount]

    common_utils.outputListToFile(tempOut,outputFileName,'./')
    #Parser the recognizer
    #parse = grammar_do.BaseParse(sentence,grammar.start())
    #parse.findParses(grammarDO.getFinalBackPointers(),grammarDO.getBackPointers())
    #parse.printToFile(outputFileName,'./')
    #grammarDO.clearBackPointers()
    #grammarDO.clearFinalBackPointers()

    #parse = None


#pprint.pprint(treeMatrix)
#4 - Print output to file for each sentence:
#       -the sentence itself, the simple bracketed structure parse(s), the number of parses for that sentence



