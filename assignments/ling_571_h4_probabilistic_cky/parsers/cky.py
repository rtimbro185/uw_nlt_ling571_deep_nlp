import collections, copy

#import parsers.do

#from parsers.do.grammar_do import BaseParse
import nltk

tree = nltk.tree.Tree
#input a list of words that compose a sentence to be parsed, parsed built incrementally during analysis
def ckyRecognizer(words,grammar):
    numberOfWordsToEvaluate = len(words)
    print("**Start ckyParser: word count [%d], words to parse: [ %s ]"%(numberOfWordsToEvaluate,words))
    treeMatrix = [[None for i in range(numberOfWordsToEvaluate+1)] for j in range(numberOfWordsToEvaluate+1)]

    pointers = []
    wordTags = []
    j = 1
    while j <= numberOfWordsToEvaluate:#iterate over the columns
        word = words[j-1]
        print("* Column j[%d], word[%s] "%(j,word))
        treeMatrix[j-1][j] = grammar.findWordPartsOfSpeech(word)
        wordTag = {word:{'i':j-1,'j':j}}
        wordTags.insert(j-1,wordTag)
        i = j - 2
        while i >= 0:#iterates over the rows, from the bottom up
            print("** Row i[%d], Column j[%d], word[%s]"%(i,j,word))
            #i -= 1#decrement row loop index

            k = i + 1
            while k >= i+1 and k <= j-1 :#ranges over the places where the string can be split, fill in the cells
                print("*** Analysing word[%s]; k[%d]--> file cell[%d,%d]"%(word,k,i,j))
                print("**** Subanalysis B[%d,%d]; C[%d,%d]"%(i,k,k,j))

                #get the sets of non-terminals to evaluate
                setB = set()
                setC = set()
                newSet = set()
                backPointerList = []
                if not treeMatrix[i][k] == None:
                    setB.update(treeMatrix[i][k])
                    if not treeMatrix[k][j] == None:
                        setC.update(treeMatrix[k][j])
                        for b in setB:
                            for c in setC:
                                tempSet = grammar.findSubConstituent(b,c)
                                if not isinstance(tempSet,type(None)):
                                    newSet.update(tempSet)#found subconstituents
                                    #add back-pointers to cell location
                                    for e in newSet:
                                        B = {b:{'i':i,'j':k}}#part of speech B
                                        C = {c:{'i':k,'j':j}}#part of speech C
                                        K = {e:{'i':i,'j':j}}
                                        backPointers = [K,B,C]
                                        NT = {e:backPointers}#Nonterminal result - mapped to cell location it filled
                                        pointers.append(NT)
                                        if i == 0 and j == numberOfWordsToEvaluate:
                                            print("")#BaseParse.storeFinalBackPointers(NT)
                    else:
                        print("** INFO **: There are no C[%d,%d] elements to compare to:"%(k,j))
                else:
                    print("** INFO **: There are no B[%d,%d] elements to start with:"%(i,k))
                #Update table matrix with new set
                if len(newSet) > 0:
                    tempNonterminalSet = set()
                    if not treeMatrix[i][j] == None:
                        tempNonterminalSet.update(treeMatrix[i][j])
                        tempNonterminalSet.update(newSet)
                        treeMatrix[i][j] = tempNonterminalSet
                    else:
                        treeMatrix[i][j] = newSet

                k += 1#loop condition
            #End K analysis
            i -= 1#loop condition
        #End Inner Row Loop
        j += 1#loop condition
    #End Outer Column Loop

    print("** End ckyParser: return treeMatrix")
    #return treeMatrix
    wordTagDict = {'word_tags':wordTags}
    pointers.append(wordTagDict)
    return pointers

########################################################################################################################################
from parsers.ckyParse import CKYBackPointer

ckyParse = CKYBackPointer()
def completeParse(parseList,startSymbol,wordCount):
    parse = []
    finalRecognitions = []
    foundFinalParse = False
    wordTags = {}
    #Get wordTags
    for e in parseList:
        if 'word_tags' in e.keys():
            wordTags = e.get('word_tags')
            ckyParse.wordTags = e.get('word_tags')
    #Get List of Final Parses based on start symbol 'TOP'
    for nonTerm in parseList:
        topList = []
        if startSymbol in nonTerm.keys():
            topList.append(nonTerm.get(startSymbol))
            topDict = topList[0]
            topPointers = topDict[0].get(startSymbol)
            i = topPointers.get('i')
            j = topPointers.get('j')
            if i == 0 and j == wordCount:
                parse.append('\n')
                parse.append('(')
                parse.append(startSymbol._symbol)

                isComplete = False
                finalRecognitions.append(nonTerm)
                foundFinalParse = True
                topPointersLft = copy.copy(topDict[1]).popitem()
                nonTerminalLft = topPointersLft[0]
                backPointerCellDictLft = topPointersLft[1]
                topPointersRht = copy.copy(topDict[2]).popitem()
                nonTerminalRht = topPointersRht[0]
                backPointerCellDictRht = topPointersRht[1]
                ckyParse.slide = 'left'
                ckyParse.isComplete = False
                parse.append('(')
                parse.append(nonTerminalLft._symbol)
                parse = reconstructParse(nonTerminalLft,backPointerCellDictLft,parse,wordTags,parseList)
                ckyParse.isComplete = False
                ckyParse.slide = 'left'
                parse.append('(')
                parse.append(nonTerminalRht._symbol)
                parse = reconstructParse(nonTerminalRht,backPointerCellDictRht,parse,wordTags,parseList)

                #closing bracket
                parse.append(' )')
                parse.append('\n')


    return parse
############################################################################


def reconstructParse(nonTerminal,map,parse,wordTags,parseList):
    #search through nodes till a pre-terminal is found and tag the NonTerminal and word
    while not ckyParse.isComplete:
        try:
            for dict in parseList:
                if nonTerminal in dict.keys():
                   tempNT = dict.get(nonTerminal)
                   nt = tempNT[0].get(nonTerminal)#find nonterminal from pointer
                   if nt.get('i') == map.get('i') and nt.get('j') == map.get('j'):#Found NonTerminal Mapping
                        #does constituent have child element?
                        if ckyParse.slide == 'left':
                            const1 = tempNT[1]
                            c1 = copy.copy(const1)
                            nonTermConst1 = c1.popitem()
                            parse.append(' (')
                            parse.append(nonTermConst1[0]._symbol)
                            parse = reconstructParse(nonTermConst1[0],nonTermConst1[1],parse,wordTags,parseList)
                            if ckyParse.slide == 'right':
                                parse.append(')')
                                ckyParse.isComplete = False
                                break
                        elif ckyParse.slide == 'right':
                            const2 = tempNT[2]
                            c2 = copy.copy(const2)
                            nonTermConst2 = c2.popitem()
                            parse.append(' (')
                            parse.append(nonTermConst2[0]._symbol)
                            ckyParse.slide = 'left'
                            parse = reconstructParse(nonTermConst2[0],nonTermConst2[1],parse,wordTags,parseList)
                            if ckyParse.recursionComplete == True:
                                ckyParse.isComplete = True
                                parse.append(')')
                                break
                            else:
                                ckyParse.slide = 'left'
                            break
                        else:

                            ckyParse.isComplete = True

            else:
                #Nonterminal has no child elements, is a preterminal

                parse.append(getWordTag(map,wordTags,nonTerminal,parse))
                parse.append(')')
                if ckyParse.slide == 'left':
                    ckyParse.slide = 'right'
                ckyParse.isComplete = True

        except StopIteration as si:
            print("StopIteration: %si"%str(si))

    return parse

def getWordTag(map,wordTags,nonTerminal,parse):
    parse.append(' ')
    #parse.append(nonTerminal._symbol)
    word = ''
    try:
        for wordDict in wordTags:
            items = wordDict.items()
            for e in items:
                i = e[1].get('i')
                j = e[1].get('j')
                if i == map.get('i') and j == map.get('j'):
                    word = e[0]
                    ckyParse.wordFound = True
                    raise StopIteration("getWordTag: word[%s] found --> cell[%d,%d]"%(word,i,j))
            else:
                ckyParse.recursionComplete = True

    except StopIteration as si:
        print("StopIteration: %s"%str(si))

    return word



