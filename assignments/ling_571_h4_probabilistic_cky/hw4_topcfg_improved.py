"""########################### LING 571: Homework #4 - Program 1 - Ryan Timbrook ################################################
                                    Improving the parser
Author: Ryan Timbrook
Date: 02/1/2016

Program 4,5 Requirements:
    -Improve baseline parser. You can improve the parser either by:
I       ***-Improving the coverage of the parser in terms of sentences parsed.
            -You will:
                -Modify your grammar induction process:
                    -Creating hw4_topcfg_improved.{py|pl|etc}

Program Name: hw4_topcfg_improved.py
    Invoked as: hw4_topcfg.{py|pl|etc} <treebank_filename> <output_PCFG_file>
        where:
            <treebank_filename> is the name of the file holding the parsed sentences, one parse per line, in Chomsky Normal Form.
            <output_PCFG_file> (parses_improved.out) is the name of the file where the induced grammar should be written.
####################################################################################################################################"""
import sys, nltk, collections, pprint, copy
from utils import common_utils
from utils.exceptions import MainException, EstimateProductionException
#!/opt/python-3.4/bin/python3.4
####################################################################################################################################
# HW4 - main function - Inducing a Probabilistic Context-free Grammar
#   -Step 1) Read in a set of parsed sentences (a mini-treebank) from a file
#   -Step 2) Identify productions and estimate their probabilities
#        Sub-Step 2.1) **Improve PCFG Sentence recognition
#                   2.1.1) **Split Nonterminals using Parent Annotation
#   -Step 3) Print out the induced PCFG with production of the form of: A -> B C [0.38725]
#   :param argv: system input attribute
####################################################################################################################################
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

        productions = [] #TODO: READ_ME: Improve Update - Changed collection object to set - Productions went from 8092 down to 856
        #productions = set()
        try:
            #Identify productions
            for sentence in parsedSentences:
                try:
                    tree = nltk.tree.Tree.fromstring(sentence)
                    #HW4-TODO: READ_ME: Update to split Non-Terminals
                    splitProductions = splitNonterminalsParentAnnotation(tree.label(),tree)

                    joinedProductions = set(tree.productions()+splitProductions)#testing if this has a better recognition

                    #for p in splitProductions:
                    for p in joinedProductions:
                        productions.append(p)
                        #productions.add(p)
                except ValueError as ve:
                    print("***** WARNING *****: hw4_topcfg_imporved.main: Caught ValueError reading in parse.train sentence; %s"%str(ve))

            #and estimate their probabilities
            productionDictP = estimateProductions(productions)

            #print out induced PCFG
            common_utils.pPrintPCFGToFile(productionDictP,argv[2],'./')


        except EstimateProductionException as epe:
            print("hw4_topcfg.main: EstimateProductionException Raised, %s"%str(epe))

    except MainException as e:
        print("hw4_topcfg.main: Exception Raised; %s"%str(e))
## End main(argv) ###########################################################################################################

#############################################################################################################################
# HW4 - Compute probabilities of rules, count: Number of times non-terminal is expanded over the number
#       of times non-terminal is expanded by given rule
#   :param productions: A list of Rules identified by reading in a mini-tree bank parsed sentence group
#   :return pcfg: - An induced Grammar file in PCFG form
#############################################################################################################################
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
    # TODO: READ_ME: Add to readme section: Need to convert productions to probabilistic before reading in by Program 2
    for p in prodOccurancesCnt:
       prob =  float(prodOccurancesCnt[p]/nonTermLHSOccurancesCnt[p.lhs()])
       pprod = nltk.grammar.ProbabilisticProduction(p.lhs(),p.rhs(),prob=prob)
       pcfgProductions.append(pprod)
       productionsProbDict[p] = float(prodOccurancesCnt[p]/nonTermLHSOccurancesCnt[p.lhs()])

    #create a PCFG induced grammar, set the start node to 'TOP'-Based on parses.train parses
    pcfg = nltk.grammar.PCFG(nltk.grammar.Nonterminal('TOP'),pcfgProductions)

    #validate all possible expansions of a non-terminal, the sum of their probabilites is 1
    validateSumProbability(productionsProbDict)


    return pcfg
##End estimateProductions(productions) ##############################################################################################

#####################################################################################################################################
#   HW4 - Utility Function - validate all possible expansions of a non-terminal, the sum of their probabilites is 1
#   :param probabilityDict: -
#####################################################################################################################################
def validateSumProbability(probabilityDict):
    sums = {}
    keys = probabilityDict.keys()
    for key in probabilityDict:
        if key.lhs() in sums:
            sums[key.lhs()] = probabilityDict[key]+sums[key.lhs()]
        else:
            sums[key.lhs()] = probabilityDict[key]

    pprint.pprint("** The sum of all non-terminal probability expansions: [ %s ]"%str(sums))

## End validateSumProbability(probabilityDict) #######################################################################################

######################################################################################################################################
#   HW4 - Improve the Parser - Parent Annotation
#
#   :param tree: - Productions generated by reading in mini-tree bank parses.train
#   :return
######################################################################################################################################
def splitNonterminalsParentAnnotation(lable,tree):
    print("main.splitNonterminalsParentAnnotation: Starting; lable[%s] productions[%s]"%(lable,str(tree)))

    #get words of speech filter
    wordPOSs = []
    for word in tree.subtrees(lambda wordsT: wordsT.height() == 2):
        wordPOSs.append(word)

    annotatedProductions = []
    i = 0
    for subT in tree.subtrees():
        annotatedRHSs = []
        parentNode = ''
        if isinstance(subT[0],str):
            parentNode = subT._label
            annotatedRHSs.append(subT[0])
        if not isinstance(subT[0],str):
            strAnnotatedRHSNode1 = subT[0]._label+'^'+subT._label
            annotatedRHSs.append(nltk.grammar.Nonterminal(strAnnotatedRHSNode1))
            strAnnotatedRHSNode2 = subT[1]._label+'^'+subT._label
            annotatedRHSs.append(nltk.grammar.Nonterminal(strAnnotatedRHSNode2))

        strAnnotatedLHSNode = subT._label

        annotatedProductions.append(nltk.grammar.Production(nltk.grammar.Nonterminal(strAnnotatedLHSNode),annotatedRHSs))
        i += 1

    #is this a child of that?
    notComplete = True
    side = 0
    annotatedHeadCount = len(annotatedProductions)
    headAnnotatedProductions = []
    while notComplete:
        for rhsEval in copy.deepcopy(annotatedProductions):#outer loop eval right hand as parent
            if not isinstance(rhsEval.rhs()[0],str):
                rhsAsParent = rhsEval.rhs()[side]._symbol.split('^')[1]
                rhsChild = rhsEval.rhs()[side]._symbol.split('^')[0]
                for lftEval in copy.copy(annotatedProductions):
                    lhsAsChild = lftEval.lhs()._symbol
                    if lhsAsChild == lable: #TOP found, jump over
                        continue
                    if lhsAsChild == rhsChild:
                       # print("Found match, lhs[%s] == rhs[%s]"%(lhsAsChild,rhsChild))
                        annotatedProductions.append(nltk.grammar.Production(nltk.grammar.Nonterminal(rhsChild+'^'+rhsAsParent),lftEval.rhs()))
                        headAnnotatedProductions.append(nltk.grammar.Production(nltk.grammar.Nonterminal(rhsChild+'^'+rhsAsParent),lftEval.rhs()))
                        annotatedProductions.remove(lftEval)
                        break
        else:
            side = 1
            if annotatedHeadCount <= len(headAnnotatedProductions)+1:
                notComplete = False

    return list(set(annotatedProductions + headAnnotatedProductions))


main(sys.argv)



