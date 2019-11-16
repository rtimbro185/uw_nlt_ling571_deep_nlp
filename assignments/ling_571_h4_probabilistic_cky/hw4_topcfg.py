"""########################### LING 571: Homework #4 - Program 1 - Ryan Timbrook ############################
                                    Inducing a Probabilistic Context-free Grammar
Author: Ryan Timbrook
Date: 01/28/2016

Program 1 Requirements:
    -Read in a set of parsed sentences (a mini-treebank) from a file
    -Identify productions and estimate their probabilities
    -Print out the induced PCFG with production of the form of: A -> B C [0.38725].

Program Name:  hw4_topcfg.py
    Invoked as: hw4_topcfg.{py|pl|etc} <treebank_filename> <output_PCFG_file>
        where:
            <treebank_filename> is the name of the file holding the parsed sentences, one parse per line, in Chomsky Normal Form.
            <output_PCFG_file> is the name of the file where the induced grammar should be written.
################################################################################################################"""
import sys, nltk, collections, pprint, math
from utils import common_utils, exceptions
#!/opt/python-3.4/bin/python3.4


def main(argv):
    if argv is None:
        argv = sys.argv

    c = 0
    for arg in argv:
        print("hw4_topcfg.main: argv%d[%s]"%(c,argv[c]))
        c+=1

    try:
        #Open parsed sentences (mini-treebank)
        parsedSentences = common_utils.openSentences(argv[1])

        productions = []
        try:
            #Identify productions
            for sentence in parsedSentences:
                tree = nltk.tree.Tree.fromstring(sentence)
                for p in tree.productions():
                    productions.append(p)

            #and estimate their probabilities
            productionDictP = estimateProductions(productions)

            #convert productions to probabilistic productions

            #print out induced PCFG
            common_utils.pPrintPCFGToFile(productionDictP,argv[2],'./')


        except exceptions.EstimateProductionException as epe:
            print("hw4_topcfg.main: EstimateProductionException Raised, %s"%str(epe))

    except exceptions.MainException as e:
        print("hw4_topcfg.main: Exception Raised; %s"%str(e))

#Compute probabilities of rules, count: Number of times non-terminal is expanded over the number
#of times non-terminal is expanded by given rule
def estimateProductions(productions):
    productionsProbDict = {}
    prodOccurancesCnt = collections.Counter()
    nonTermLHSOccurancesCnt = collections.Counter()
    pcfgProductions = []

    #cycle through all the productions
    for p in productions:
        #assign p as key of dict object, where p is the key incrementally add up the number of times p is found in the list
        prodOccurancesCnt[p] += 1
        nonTermLHSOccurancesCnt[p.lhs()] += 1

    #Count(production)/Count(production.lhs())
    # TODO: Add to readme section: Need to convert productions to probabilistic before reading in by Program 2
    for p in prodOccurancesCnt:
       prob =  float(prodOccurancesCnt[p]/nonTermLHSOccurancesCnt[p.lhs()])
       pprod = nltk.grammar.ProbabilisticProduction(p.lhs(),p.rhs(),prob=prob)
       pcfgProductions.append(pprod)
       productionsProbDict[p] = float(prodOccurancesCnt[p]/nonTermLHSOccurancesCnt[p.lhs()])

    #create a PCFG induced grammar, set the start node to 'TOP'-Based on parses.train parses
    pcfg = nltk.grammar.PCFG(nltk.grammar.Nonterminal('TOP'),pcfgProductions)

    #validate all possible expansions of a non-terminal, the sum of their probabilites is 1
    sums = {}
    keys = productionsProbDict.keys()
    for key in productionsProbDict:
        if key.lhs() in sums:
            sums[key.lhs()] = productionsProbDict[key]+sums[key.lhs()]
        else:
            sums[key.lhs()] = productionsProbDict[key]
    pprint.pprint("** The sum of all non-terminal probability expansions: [ %s ]"%str(sums))


    return pcfg



main(sys.argv)



