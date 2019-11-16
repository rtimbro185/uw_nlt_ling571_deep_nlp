"""#### LING 571: Homework #6 - Ryan Timbrook ##################
                                    Semantics
Author: Ryan Timbrook
Date: 02/16/2016

Program Name: hw6_semantics.py - performs the parsing and compositional semantic analysis
    -invoked as: hw6_semantics. <input_grammar_filename> <input_sentences_filename> <output_filename>
    -where,
        <input_grammar_filename> is the name of the file holding the grammar with FOL semantic attachments
            that you created to implement the rule-to-rule style compositional semantic analysis.
        <input_sentences_filename> is the name of the file holding the sentences to parse
            and perform semantic analysis on.
        <output_filename> is the name of the file to write the results of your automatic semantic analysis.

**Note: Only need to print a single representation if the sentence is ambiguous.
#########################################################################################################"""
import sys, nltk

########################################################################################################
#  Main Controller Function
#########################################################################################################

def main(argv):

    if argv is None:
        argv = sys.argv
    c = 0
    for arg in argv:
        print("hw6_semantics.main: argv%d[%s]"%(c,argv[c]))
        c+=1

    #Load Feature-based grammar
    grammar = nltk.data.load(argv[1])

    #Load Test Sentences
    sents = open(argv[2])

    #Open output file for writing
    outputFile = open(argv[3],'a')

    for sent in sents.readlines():
        sent = sent.replace('\n','')
        outputFile.write(sent+'\n')
        words = nltk.word_tokenize(sent)
        featureChart = nltk.parse.featurechart.FeatureChartParser(grammar)
        chart = featureChart.chart_parse(words)
        fparses = list(chart.parses(grammar.start()))

        if len(fparses) == 0:
                outputFile.write(str('\t')+'\n')
        else:
            for tree in fparses:
                outputFile.write(str(nltk.sem.util.root_semrep(tree))+'\n')
                break

    outputFile.flush()
    outputFile.close()

## End main(argv)###############################################################################################################

##############################################################################################################################
# In-line process flow to call the main controller function
##############################################################################################################################
if __name__ == '__main__': main(sys.argv)