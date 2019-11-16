###############################################################################################################
#Ling 571 - Deep Processing Techniques for NLP
#Winter 2016
#Homework #4: Due February 2nd, 2016
#http://courses.washington.edu/ling571/ling571_WIN2016/hw/hw4/hw4.html
#Author: Ryan Timbrook
#Date: 02/2/2016
#
#Goals:
#   -Explore issues in probabilistic parser design for natural language processing.
#   -Learn how to extract rule probabilites and explore parser evaluation.
#   -Improve your understanding of the probabilistic CKY algorithm through implementation.
#   -Investigate the tradeoffs in probabilistic parser design in terms of speed and accuracy
#           -Learn about PCFGs
#            -Implement PCKY
#            -Analyze parsing evaluation
#            -Assess improvements to PCFG parsing
#
#   Tasks:
#        -Train a PCFG
#            -Estimate rule probrabilities from treebank
#        -Build PCKY parser
#        -Evaluate the parser using standard metric
#           -Parseval implemented as 'evalb'
#        -Improvement:
#           -Improve the parser in some way, coverage, accuracy, speed
#           -Evaluate the new parser
#
#   Requirements:
#
#
#   Programming
#       
#   Verification & Parse Comparison
#
#
##########################################################################################################################################################################

#############################################################################################################
#               Describe Work:
#
#   Problems Encountered?
        -hw4_parser:
            -Using the nltk.wordpunct_tokenize(sentence) proved to be a poor chose in the original parser. It throw exceptions on otherwise recognizable words
            -I switched to the TreebankWordTokenizer().tokenize(sentence) in the hw4_parser_improved program. That recognized a greater word base.
            -I also found an issue in my logic where in prior version of my parser i was using a string casefold() method to ignor case of words.
                this proved error prone with this larger grammar base that differentiated parts of speech the case of the words.
            -I had challenges with my existing parsers object model for this size of a test bed. The way I was capturing backpointers in multidimensional
                collection objects proved challenging to work through and I don't believe it's completely correct yet.
                I made many attempts at changing the way number of back pointers stored in memory and compared them to various test runs. It only seemed to make
                the recognition rates go down.
        -hw4_topcfg_improved:
            -I implemented a parent annotated model in this application and tested multiple scenarios with the pcfg results against both the original
                parser and improved parser. The results only got worse... I had a much lower recognition rate with the updated parent annotations.
                I believe I have issues in how I storing the backpointers in the parser and matching them up to the best parses. Lest run of the improved
                parser I had 10000+ pack pointers for one test sentences. The time to parse was at least 10 min.
                -The logic needs tweaking and downsizing the way I'm storing the reconstruction data.

            - I was able to get a narrow margin of increase in the number of sentences recognized:
                Base:
                    -- len<=150 --
                    Number of sentence        =     55
                    Number of Error sentence  =      0
                    Number of Skip  sentence  =     13
                    Number of Valid sentence  =     42

                Improved:
                    :-- len<=150 --
                    Number of sentence        =     55
                    Number of Error sentence  =      0
                    Number of Skip  sentence  =     10
                    Number of Valid sentence  =     45
                        -Initial parse

########################################################################################################################################
