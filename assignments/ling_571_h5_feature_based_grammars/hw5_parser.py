"""########################### LING 571: Homework #5 - Ryan Timbrook #############################################################
                                Building a Feature-based Grammar
Author: Ryan Timbrook
Date: 02/9/2016

High Level:
    -Performs the feature parsing grammar check
Program Requirements:


Program Name: hw5_parser.py
    Invoked as: hw5_parser.py <input_grammar_filename> <input_sentence_filename> <output_filename>
    where,
        <input_grammar_filename> is the name of the file holding the feature-based grammar that you created to implement the necessary grammatical constraints.
        <input_sentence_filename> is the name of the file holding the sentences to test for grammaticality and parse.
        <output_filename> is the name of the file to write the results of your grammaticality parsing test.

**Note: If the sentence is ambiguous, you only need to print a single parse.
#################################################################################################################################################"""
import sys, nltk

##############################################################################################################################
#  Main Controller Function
##############################################################################################################################

def main(argv):

    if argv is None:
        argv = sys.argv
    c = 0
    for arg in argv:
        print("hw5_parser.main: argv%d[%s]"%(c,argv[c]))
        c+=1

    #Load Feature-based grammar
    grammar = nltk.data.load(argv[1])

    #Load Test Sentences
    sents = open(argv[2])

    #Open output file for writing
    outputFile = open(argv[3],'a')

    for sent in sents.readlines():
        sent = sent[:-2]
        words = nltk.word_tokenize(sent)
        featureEarley = nltk.parse.FeatureEarleyChartParser(grammar)
        chart = featureEarley.chart_parse(words)
        fparses = list(chart.parses(grammar.start()))

        if len(fparses) == 0:
                outputFile.write(str(' ')+'\n')
        else:
            for tree in fparses:
                outputFile.write(tree._pformat_flat('','()',quotes=False)+'\n')
                break

    outputFile.flush()
    outputFile.close()

## End main(argv)###############################################################################################################

##############################################################################################################################
# In-line process flow to call the main controller function
##############################################################################################################################
if __name__ == '__main__': main(sys.argv)