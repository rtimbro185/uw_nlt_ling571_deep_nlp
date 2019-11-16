"""LING 571 - Homework #2 - Ryan Timbrook ################################################################################################

##########################################################################################################################################################"""
import sys

import nltk

from ling_utils import common_utils
from ling_utils import hw2_cnfFormatter


print("Number of system arguments:",len(sys.argv),"arguments.")
outputFileName = sys.argv[2]
########################################################################################################################
#   Step 1) Read in the Grammar File to be converted from CFG to CNF
#       <input_grammar_file> is the name of the file holding the grammar to convert to Chomsky Normal Form.
#       -atis.cfg: CFG grammar to test your CNF conversion program

#Get main argument list from command line, first argument is the filename holding the grammar to convert to CNF
grammarCfgFileName = sys.argv[1]
print("Grammar Cfg File Name is [%s]" %grammarCfgFileName)

grammar = common_utils.openGrammarFile(grammarCfgFileName)
print("Grammar CFG file content to be converted :\n%s" %str(grammar))
########################################################################################################################

########################################################################################################################
#   Step 2) Convert this grammar to Chomsky Normal Form
#
print("Before Formatting: Is grammar in CNF format? [%s]" %grammar.is_chomsky_normal_form())
print("Before Formatting: Is grammar binarised? [%s]" %grammar.is_binarised())
print("Grammar is not in CNF Format, Converting grammar to CNF")
if not grammar.is_chomsky_normal_form():
    start = grammar.start()
    print("Grammar Start Symbol [%s]" %start)
    convertedProductionsList = hw2_cnfFormatter.convertGCFToCNF(grammar.productions(),start,grammar)
    print("***INFO***: Final productions list count[%d]"%len(convertedProductionsList))

    #Configur new production list as a grammar and validate it's in CNF format
    cnfGrammar = nltk.grammar.CFG(start,convertedProductionsList)
    print("After Formatting: Is grammar in CNF format? [%s]" %cnfGrammar.is_chomsky_normal_form())
    print("After Formatting: Is grammar binarised? [%s]" %cnfGrammar.is_binarised())
    print("After Formatting: Grammar CFG \n %s"%str(cnfGrammar))


else:
    print("*****ALERT*****: Grammar is already in CNF form")
########################################################################################################################

########################################################################################################################
#   Step 3) Print out the rules of the converted grammar to a file
#           <output_grammar_file> is the name of the output file for the CNF conversion.
#               *The file should be in the NLTK grammar format, but now in Chomsky Normal Form.
#           -hw2_grammar_cnf.cfg: Results of running your CNF conversion program on the atis.cfg grammar file
#

#Second system argument is the name of the output file for the CNF conversion
outputFileName = sys.argv[2]
print("Output File Name is [%s]" %outputFileName)
#hw2_utils.outputListToFile(convertedProductionsList, outputFileName, './')
common_utils.outputGrammarToFile(cnfGrammar, outputFileName, './')
#nltk.data.load(cnfGrammar)
#nltk.data.retrieve(cnfGrammar,outputFileName)

########################################################################################################################

########################################################################################################################
#   Validation:
#     Using your system from HW#1, you will parse a set of sentences with
#           -a general NLTK context-free grammar, and
#           -a weakly equivalent Chomsky Normal Form context-free grammar, created by your CNF conversion program.
#     Output:
#       File 1: hw2_orig_output.txt: Results of parsing the test sentences <sentences.txt> using the original atis.cfg grammar file.
#       File 2: hw2_cnf_output.txt: Results of parsing the test sentences <sentences.txt> using your CNF-converted grammar file
#
















