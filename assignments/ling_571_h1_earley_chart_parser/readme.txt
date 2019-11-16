###############################################################################################################
#Ling 571 - Deep Processing Techniques for NLP
#Winter 2016
#Homework #1: Due January 12, 2016
#URL: http://courses.washington.edu/ling571/ling571_WIN2016/hw/hw1/hw1.html
#Author: Ryan Timbrook
#Date: 01/12/2016
#
#Goals:
#   Explore the basics of context-free grammar design.
#   Identify some of the challenges in building grammars for natural languages.
#   Begin to gain some familiarity with the Natural Language Toolkit (NLTK).
#   Gain some experience with the cluster and condor.
#
#Requirements:
#   Build a Grammar:
#       -Create a set of context-free grammar rules that are adequate to analyze a small set of English natural language sentences.
#           -The grammar should be able to produce parses for all sentences in the files.
#           -The grammar should capture the major clause type (S, etc.), the major phrase types (NP, VP, PP, etc.), the parts of speech (POS) (NN, VBZ), and any punctuation or special symbols
#           -*Hard-coding capitalization is accepted
#
#   Parsing:
#       -Create a program to parse the test sentences based on your grammar and analyze the results
#           -Specifics:
#               Load your grammar.
#                   -Build a parser for your grammar using nltk.parse.EarleyChartParser.
#                   -Read in the example sentences.
#                   -For each example sentence, output to a file
#                       -the sentence itself
#                       -the simple bracketed structure parse(s), and
#                       -the number of parses for that sentence.
#                       -Finally, print the average number of parses per sentence obtained by your grammar.
#
#   Programming
#       Create a program named hw1_parse.py to perform the parsing as described above invoked as:
#            hw1_parse.py <grammar_file> <test_sentence_file> <output_file>
#        where
#            <grammar_file> is the name of the file holding your grammar rules in the NLTK .cfg format.
#            <test_sentence_file> is the name of the file holding the set of sentences to parse, one sentence per line
#            <output_file> is the name of output file for your system
#
#
##########################################################################################################################################################################


#############################################################################################################
#               Describe Work:
#
#   Problems Encountered?
#           -I encountered problems with the condor hw1_cmd file when first trying to execute my program with the condor system.
#               -The program couldn't find the python interpreter to use for execution.
#               -Reading over the class goposts I found postings describing how the interpreter should be configured in the hw1_cmd file to target the python3.4.exe
#               -Making the necessary updates, Executable = /opt/python-3.4.1/bin/python3.4", to the hw1_cmd file the program executed successfully.
#
#           -I encountered challenges with creating a CFG grammar file that would produce parses using the sentences provided.
#               -These challenges were rooted in not understanding how the CFG grammar file functioned given it's syntax.
#                   -Through trial and error I learned how the CFG file's syntax operated with the nltk.grammar package classes enabling me to fix my CFG Grammar file.
#
#           -Time was my most limiting factor experienced with this assignment.
#               -Being this was my first assignment in the Linguistics program and overall my first assignment at the Univerity of Washingont,
#                my experience with all of the processes and standards took time to practice and familiarize myself with.
#
#   Were there parts of the project not able to be completed?
#
#       Why?
#
#       What was tried and/or what didn't work?
#
#   Discussion:
#
#
########################################################################################################################################

