"""########################### LING 571: Homework #4 - Program 2 - Ryan Timbrook #############################################################
                                    Converting from CKY to Probabilistic CKY
Author: Ryan Timbrook
Date: 01/29/2016

High Level:
    -Implement a probabilistic version of the CKY parsing algorithm. Given a probabilistic context-free grammar and an input string,
     the algorithm should return the highest probability parse tree for that input string.

Program 1 Requirements:
    -Read in a PCFG in NLTK format as generated above
    -Read in a set of sentences to parse
    -For each sentence:
        -Parse the sentences using a PCKY algorithm that you implement
        -Print the highest scoring parse to a file, on a single line

Program Name:  hw4_parser.py
    Invoked as: hw4_parser.{py|pl|etc} <input_PCFG_file> <test_sentence_filename> <output_parse_filename>
        where:
            <input_PCFG_file> is the name of the file holding the induced PCFG grammar to be read.
            <test_sentence_filename> is the name of the file holding the test sentences to be parsed.
            <output_parse_filename> is the name of the file to which the best parse for each sentence will be written.
                Each parse should appear on only one line, and there should be one line per sentence in the output file.
    **Note: The test sentences may include words not seen in training; this happens in real life. In a baseline system, these may fail to parse.
#################################################################################################################################################"""
#!/opt/python-3.4/bin/python3.4
import sys, nltk, math, copy, pprint
from nltk.tokenize import TreebankWordTokenizer
from utils import common_utils
from utils.parsers import grammar_do
from utils.exceptions import ZeroParseException
from utils.parsers.ckyParse import PCFGRule
##############################################################################################################################
#  Main Controller Function
##############################################################################################################################
def main(argv):
    print("hw4_topcfg.main: Entered")

    if argv is None:
        argv = sys.argv

    c = 0
    for arg in argv:
        print("hw4_topcfg.main: argv%d[%s]"%(c,argv[c]))
        c+=1

    #load pcfg induced file generated from Program 1
    pcfg = common_utils.loadPCFGGrammarFromFile('./',argv[1])

    #read in sentences to be parsed
    sentences = common_utils.openSentences(argv[2])

    #parse sentence, return most probably parse and its probability
    #2.1 - Initialize grammar data object
    grammarDO = grammar_do.GrammarDO(pcfg)

    #3 - Execute custome Probabilistic CKY algorithm implementation on test sentence
    pparse = []
    for sentence in sentences:
        #words = nltk.wordpunct_tokenize(sentence)
        words = TreebankWordTokenizer().tokenize(sentence)
        #words = sentence.sp

        #validate the grammar file has the lexical words to parse the sentence
        try:
            #try:
                # ValueError is thrown by check_coverage(tokens) method if the grammar doesn't have all the words needed to parse the sentence
                #grammarDO.grammar.check_coverage(words)#TODO: it's throwing ValueError for symboles not in specific case of the grammar, should this be rechecked ignorring the case?
           # except ValueError as ve:
              #  print("***** WARNING *****:hw4_parser.main: Caught ValueError, %s"%str(ve))
               # grammarDO.setUnrecognizedTokensList(str(ve))
               # raise ZeroParseException(str(ve))

            #Run CKYRecognizer / Parser
            pparse = (ckyRecognizer(list(words),grammarDO))
            if len(pparse) > 0:
                #print the highest scoring parse to a file, on a single line
                common_utils.outputToFile(pparse,argv[3],'./')
            else:
                grammarDO.setNonParsedSentences(sentence)
                raise ZeroParseException("Parse list returned from parser is empty for sentence [%s]"%sentence)

        except ZeroParseException as zpe:
            print("***** WARNING *****:hw4_parser.main: Caught ZeroParseException; %s"%str(zpe))
            # print blank line
            pparse = [' ']
            common_utils.outputToFile(pparse,argv[3],'./')
            pparse.clear()
            continue

        except Exception as e:
            print("***** ERROR *****:hw4_parser.main: Caught Exception, %s"%str(e) ,sys.stderr)
            raise Exception

    print("hw4_parser.main: Exiting")
# End main(argv)###############################################################################################################

###############################################################################################################################
# HW3-CKY Recognizer modified with Probabilistic CKY algorithm
# *input a list of words that compose a sentence to be parsed, parsed built incrementally during analysis
# :param words: A list of words to recognize
# :param grammar: A PCFG grammar
###############################################################################################################################
def ckyRecognizer(words,grammarDO):
    numberOfWordsToEvaluate = len(words)
    print("**Start ckyParser: word count [%d], words to parse: [ %s ]"%(numberOfWordsToEvaluate,words))
    treeMatrix = [[None for i in range(numberOfWordsToEvaluate+1)] for j in range(numberOfWordsToEvaluate+1)]
    pointers = []
    wordTags = []
    startSymbol = grammarDO.grammar.start()
    j = 1
    while j <= numberOfWordsToEvaluate:#iterate over the columns
        word = words[j-1]
        print("* Column j[%d], word[%s] "%(j,word))
        treeMatrix[j-1][j] = grammarDO.findWordPartsOfSpeech(word)
        wordTag = {word:{'i':j-1,'j':j}}
        wordTags.insert(j-1,wordTag)
        i = j - 2
        while i >= 0:#iterates over the rows, from the bottom up
            print("** Row i[%d], Column j[%d], word[%s]"%(i,j,word))

            k = i + 1
            while k >= i+1 and k <= j-1 :#ranges over the places where the string can be split, fill in the cells
                print("*** Analysing word[%s]; k[%d]--> file cell[%d,%d]"%(word,k,i,j))
                print("**** Subanalysis B[%d,%d]; C[%d,%d]"%(i,k,k,j))
                setB = {} #HW4 - modify
                setC = {} #HW4 - modify
                newSet = {}#HW - modify to dict include probabilities
                if not treeMatrix[i][k] == None:
                    setB.update(treeMatrix[i][k])
                    if not treeMatrix[k][j] == None:
                        setC.update(treeMatrix[k][j])
                        for b in setB:
                            for c in setC:
                                #H4-Add check to see that both constituents probabilities are greater than zero
                                if setB[b] > 0 and setC[c] > 0:
                                   tempSet = grammarDO.findSubConstituent(b,setB[b],c,setC[c])#HW4-updated attribute list to include probabilities to be summed
                                else:
                                    tempSet = None
                                if not isinstance(tempSet,type(None)):
                                    newSet.update(tempSet)#found subconstituents
                                tempNonterminalSet = {}
                                tmatrix = treeMatrix[i][j]
                                newSetIndex = 0
                                for const in copy.copy(newSet):
                                    if not isinstance(tmatrix,type(None)):
                                        matrixA = treeMatrix[i][j].get(const)
                                        if not isinstance(matrixA,type(None)):
                                            newP = newSet[const]
                                            if math.log1p(newP) > math.log1p(matrixA):
                                                treeMatrix[i][j].pop(const)
                                                #pointers.pop(newSetIndex)
                                                treeMatrix[i][j].update({const:newP})

                                    treeMatrix[i][j] = newSet
                                    B = {b:{'i':i,'j':k,'p':setB[b]}}
                                    C = {c:{'i':k,'j':j,'p':setC[c]}}
                                    K = {const:{'i':i,'j':j,'p':newSet[const]}}
                                    backPointers = [K,B,C]
                                    pcfgRule = PCFGRule(const,[B,C])
                                    pcfgRule.setProbability(newSet[const])
                                    grammarDO.setCnfRules(pcfgRule)#constituents

                                    #H4 - TODO: READ_ME - Reconstructing the code in efforts to increase precision and recal statistics only raised them by 1% (though my backpointer objects went from 700+ to 120 ish) - Remove lower level constituents from backpointers
                                    try:
                                        if not isinstance(pointers,type(None)):
                                            constIndex = 0
                                            for pointer in copy.copy(pointers):
                                                if const in pointer:
                                                    constList = pointer[const]
                                                    constK = constList[0]
                                                    constI = constK[const].get('i')
                                                    constJ = constK[const].get('j')
                                                    if constI == i and constJ == j:#determine if const is in backpointers
                                                        constP = constK[const].get('p')
                                                        newConstP = newSet[const]
                                                        if math.log1p(constP) < math.log1p(newConstP):
                                                            pointers.pop(constIndex)
                                                            NT = {const:backPointers}
                                                            pointers.append(NT)
                                                            raise StopIteration("Breaking out of backpointer probability evaluation, constP[%f] < newConstP[%f], removed lower value pointer"%(constP,newConstP))
                                                        else:#H4-Don't update backpointer list with lower probability
                                                            raise StopIteration("Breaking out of backpointer probability evaluation, constP[%f] > newConstP[%f]"%(constP,newConstP))
                                                constIndex += 1
                                            else:
                                                NT = {const:backPointers}
                                                pointers.append(NT)
                                        else:
                                           NT = {const:backPointers}
                                           pointers.append(NT)

                                    except StopIteration as si:
                                        #print("hw4_parser.ckyRecognizer: Caught StopIteration; %s"%str(si))
                                        #NT = {const:backPointers}###TEST - Low Sentence Recognition - ADDED THIS BACK
                                        #pointers.append(NT)###TEST - Low Sentence Recognition - ADDED THIS BACK
                                        continue
                                newSetIndex += 1
                    else:
                        print("** INFO **: There are no C[%d,%d] elements to compare to:"%(k,j))
                else:
                    print("** INFO **: There are no B[%d,%d] elements to start with:"%(i,k))

                k += 1#loop condition
            #End K analysis
            i -= 1#loop condition
        #End Inner Row Loop
        j += 1#loop condition
    #End Outer Column Loop

    ##Check number of TOP Sentences in list
    topPMem = None
    for point in pointers:
        topI = 0
        for key in point.keys():
            if key == startSymbol:
                top = point[key]
                topI = top[0][key].get('i')
                topJ = top[0][key].get('j')
                if topI == 0 and topJ == numberOfWordsToEvaluate:
                    if not isinstance(topPMem,type(None)):
                        tempP = topP = top[0][key].get('p')
                        if math.log1p(topPMem) > math.log1p(tempP):
                            pointers.remove(topI)

                    else:
                        topPMem = topP = top[0][key].get('p')

        topI +=1

    print("** End ckyParser: return treeMatrix")
    #return treeMatrix
    wordTagDict = {'word_tags':wordTags}
    pointers.append(wordTagDict)
    cpointers = copy.copy(pointers)
    ckyBackPointers = CKYBackPointer(wordTagDict,cpointers,numberOfWordsToEvaluate,startSymbol)

    #pointers.clear()
    return completeParse(ckyBackPointers)

## End ckyRecognizer(words,grammar)###########################################################################################

##############################################################################################################################
# HW3 - Reconstruct a parse based on recognized constituents using back-pointer mappings
#
# :param backPointers: -An object used to store constituent mapping data and tracing attributes for reconstructing
#                       the parse through recursion.
#
#   *TODO: READ_ME: Note: modified in HW4 to accept the CKYBackPointer object for parse reconstruction
##############################################################################################################################
from nltk.tree import Tree
def completeParse(backPointers):
    parse = []
    finalRecognitions = []
    finalParses = []
    foundFinalParse = False

    #Get wordTags
    for e in backPointers.parseList:
        if 'word_tags' in e.keys():
            backPointers.wordTags = e.get('word_tags')
    #Get List of Final Parses based on start symbol 'TOP'
    for nonTerm in backPointers.parseList:
        topList = []
        if backPointers.startSymbol in nonTerm.keys():
            topList.append(nonTerm.get(backPointers.startSymbol))
            topDict = topList[0]
            topPointers = topDict[0].get(backPointers.startSymbol)
            i = topPointers.get('i')
            j = topPointers.get('j')
            #only reconstruct those parses which are final productions
            if i == 0 and j == backPointers.wordCount:
                parse.append('(') #parse: Opening bracket for start symbol
                parse.append(backPointers.startSymbol._symbol) #parse: Start symbol
                #isComplete = False
                finalRecognitions.append(nonTerm)
                foundFinalParse = True
                #get both RHS rules of the final production along with their back pointer mapping
                topPointersLft = copy.copy(topDict[1]).popitem()
                nonTerminalLft = topPointersLft[0]
                backPointerCellDictLft = topPointersLft[1]
                topPointersRht = copy.copy(topDict[2]).popitem()
                nonTerminalRht = topPointersRht[0]
                backPointerCellDictRht = topPointersRht[1]

                #Start the reconstruction going down the left side of the tree
                backPointers.slide = 'left'
                backPointers.isComplete = False
                parse.append('(') #parse: Opening bracket for top, left most, RHS rule of the final production
                parse.append(nonTerminalLft._symbol) #parse: Nonterminal symbol of the top, left most, RHS rule of the final production
                parse = reconstructParse(nonTerminalLft,backPointerCellDictLft,parse,backPointers)
                #parse.append(')') #****Removed This: It was through off the bracketing order, it's a duplicate of one being added in the calling function -parse: Closing bracket for the top, left most, RHS rule of the final prduction

                #Complete the reconstruction going down the right side of the of the top, right most, RHS rule of the final production
                backPointers.isComplete = False
                backPointers.slide = 'left' #of this rule, start off reconstructing it's LHS constituents
                parse.append('(') #parse: Opening bracket for top, right most, RHS rule of the final production
                parse.append(nonTerminalRht._symbol) #Nonterminal symbol of the top, right most, RHS rule of the final production
                parse = reconstructParse(nonTerminalRht,backPointerCellDictRht,parse,backPointers)
                #parse.append(')') #****Removed This: It was through off the bracketing order, it's a duplicate of one being added in the calling function - parse: Closing bracket for the top, right most, RHS rule of the final prduction

                #apply closing bracket to the start Nonterminal
                parse.append(')') #parse:

                #construct a parse string from the parse list object containing individual elements of the parse
                parseStr = ''
                for c in parse:
                    parseStr = parseStr+c

                #TODO: READ_ME: HW4 - Added conversion of a parse as a string object to a Tree object of the NLTK library
                try:
                    t = Tree.fromstring(parseStr)
                    backPointers.setParseTrees(t)
                except ValueError as ve:
                    print("***** ERROR *****: Caught Value Error Converting parse string [%s] to an NLTK Tree object; %s", file=sys.stderr)%(parseStr,str(ve))

                #finalParses.append(parseStr)
                finalParses.append(parseStr)

    return finalParses
## End completeParse(backPointers)############################################################################################

##############################################################################################################################
# HW3 - This function is used as a recursive function to identify all sub-constituents of the Nonterminal object passed to it
#
# :param nonTerminal: Nonterminal object to recursively find all sub-constituents
# :param map: A dictionary object containing the cell location this Nonterminal was recognized from
# :param parse: A list object containing the reconstructed parse elements found through this Nonterminal
# :param backPointers: An object used to maintain state of the recursive function iterating
#
# *TODO: READ_ME: Note: modified in HW4 to accept the CKYBackPointer object for parse reconstruction
###############################################################################################################################
def reconstructParse(nonTerminal,map,parse,backPointers):
    #search through nodes till a pre-terminal is found and tag the NonTerminal and word
    while not backPointers.isComplete:
        try:
            for dict in backPointers.parseList: #Search through back-pointers list and identify if the Nonterminal argument attribute is in the list
                if nonTerminal in dict.keys():
                   tempNT = dict.get(nonTerminal)
                   nt = tempNT[0].get(nonTerminal)#find Nonterminal from pointer
                   if nt.get('i') == map.get('i') and nt.get('j') == map.get('j'):#Found NonTerminal Mapping
                        #does constituent have child element?
                        if backPointers.slide == 'left':
                            const1 = tempNT[1]
                            c1 = copy.copy(const1)
                            nonTermConst1 = c1.popitem()
                            parse.append('(') #parse: Opening bracket for left child node identified
                            parse.append(nonTermConst1[0]._symbol) #parse: left side child node Nonterminal symbol
                            parse = reconstructParse(nonTermConst1[0],nonTermConst1[1],parse,backPointers) #recusively call function with child node
                            if backPointers.slide == 'right':
                                backPointers.isComplete = False
                                backPointers.wordFound = False
                                break
                            #else:
                                #parse.append(')') #parse: closing bracket of left child node
                        elif backPointers.slide == 'right':
                            const2 = tempNT[2]
                            c2 = copy.copy(const2)
                            nonTermConst2 = c2.popitem()
                            parse.append('(') #parse: Opening bracket for right side child node identified
                            parse.append(nonTermConst2[0]._symbol) #parse: right side child node Nonterminal symbol
                            backPointers.slide = 'left' #slide the flow back to the left side
                            parse = reconstructParse(nonTermConst2[0],nonTermConst2[1],parse,backPointers) #recusively call function with child node
                            if backPointers.wordFound == True:
                                backPointers.isComplete = True
                                parse.append(')') #parse: closing bracket of right side child node Nonterminal symbol
                                break
                            else:
                                backPointers.recursionComplete = True
                                parse.append(')') #parse: apply outter most closing bracket to this instance node
                                backPointers.isComplete = True
                                break
                        else:
                            #should never reach this step unless the slider rule changes from something other than 'left' or 'right'
                            backPointers.isComplete = True

            else:
                #Nonterminal has no child elements, is a preterminal
                parse.append(' ') #parse: apply a space before the word part of speech is attached
                parse.append(getWordTag(map,backPointers))
                parse.append(')') #parse: Closing bracket of the pre-terminal node
                if backPointers.slide == 'left': #should always be left side when finding a terminator
                    backPointers.slide = 'right'
                #break out of recursion
                backPointers.isComplete = True

        except StopIteration as si:
            print("StopIteration: %si"%str(si))

    return parse
##############################################################################################################################

##############################################################################################################################
# HW3 - This function is used to identify the pre-terminals of the lexical words recognized
#
# :param map: Is a dictionary object containing the mapping of the Nonterminal
# :param backPointers: An object used to maintain state of the recursive function iterating

# *TODO: READ_ME Note: modified in HW4 to accept the CKYBackPointer object for parse reconstruction
##############################################################################################################################
def getWordTag(map,backPointers):
    word = ''
    try:
        for wordDict in backPointers.wordTags:
            items = wordDict.items()
            for e in items:
                i = e[1].get('i')
                j = e[1].get('j')
                if i == map.get('i') and j == map.get('j'):
                    word = e[0]
                    backPointers.wordFound = True
                    raise StopIteration("getWordTag: word[%s] found --> cell[%d,%d]"%(word,i,j))
        #else:
            #backPointers.recursionComplete = True

    except StopIteration as si:
        print("StopIteration: %s"%str(si))

    return word
## End getWordTag(map,backPointers)###########################################################################################

##############################################################################################################################
# HW3 - Backpointer object used to track flow of recursive function calling to reconstruct parse from Nonterminal
#        constituent mapping
#   *Note: HW4 - Updated to include start symbol, and parseList
##############################################################################################################################
class CKYBackPointer():

    slide = ''
    __parseTrees = []
    finalRecognition = {}
    wordTags = {}
    wordCount = 0
    parseList = []
    treeMatrix = [[]]
    startSymbol = None
    isComplete = False
    wordFound = False
    recursionComplete = False

    def __init__(self,wordTags=None,parseList=None,wordCount=None,startSymbol=None,finalRecognition=None):
        self.isComplete = False
        self.slide = 'left'
        self.wordTags = wordTags
        self.parseList = parseList
        self.wordCount = wordCount
        self.startSymbol = startSymbol
        self.finalRecognition = finalRecognition

    def setParseTrees(self,tree):
        self.__parseTrees.append(tree)

    def getParseTrees(self):
        return self.__parseTrees

##End class CKYBackPointer()##################################################################################################

##############################################################################################################################
# In-line process flow to call the main controller function
##############################################################################################################################
main(sys.argv)