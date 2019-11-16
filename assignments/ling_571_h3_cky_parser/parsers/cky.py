from collections import defaultdict
import copy


class CKYParser():

    __grammar = set()
    __preTerminalWordTags = {}


    def __init__(self):
        self.__name = "CKYParser"
        self.__nonTerminalBackPointersDict = defaultdict(list)
        self.__preTerminalWordTagsDict = defaultdict(list)
        self.__parseCount = 0



    #input a list of words that compose a sentence to be parsed, parsed built incrementally during analysis
    def ckyRecognizer(self, words,grammar):
        numberOfWordsToEvaluate = len(words)
        print("**Start ckyParser: word count [%d], words to parse: [ %s ]"%(numberOfWordsToEvaluate,words))
        treeMatrix = [[None for i in range(numberOfWordsToEvaluate+1)] for j in range(numberOfWordsToEvaluate+1)]
        #backPointerList = []
        pointers = []
        wordTags = []

        j = 1
        while j <= numberOfWordsToEvaluate:#iterate over the columns
            word = words[j-1]
            print("* Column j[%d], word[%s] "%(j,word))
            treeMatrix[j-1][j] = grammar.findWordPartsOfSpeech(word)
            self.__preTerminalWordTags[word].append({'i':j-1,'j':j})
            #wordTag = {word:{'i':j-1,'j':j}}
            #wordTags.insert(j-1,wordTag)
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
                                        #TODO: figure out how to add the word to the cell mapping
                                        for e in newSet:
                                            B = {b:{'i':i,'j':k}}#part of speech B
                                            C = {c:{'i':k,'j':j}}#part of speech C
                                            K = {e:{'i':i,'j':j}}
                                            backPointers = [K,B,C]
                                            NT = {e:backPointers}#Nonterminal result - mapped to cell location it filled
                                            #backPointerList.append(NT)
                                            #BaseParse.storeBackPointers(NT)
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

                        #treeMatrix[i][j] = newSet #needs to update the existing treeMatrix set with subsiquent finds

                    #TODO: Update treeMatrix set to include backpointers for each Nonterminal to cell it was derived from
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

    ######################################################################################
    def completeParse(self, parseList,startSymbol,wordCount):
        parse = []
        finalRecognitions = []
        foundFinalParse = False
        wordTags = {}
        #Get wordTags
        for e in parseList:
            if 'word_tags' in e.keys():
                wordTags = e.get('word_tags')

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
                    count = 0
                    while count < 2:
                        finalRecognitions.append(nonTerm)
                        foundFinalParse = True
                        topPointers = topDict[count+1].popitem()
                        nonTerminal = topPointers[0]
                        backPointerCellDict = topPointers[1]
                        parse = self.reconstructParse(nonTerminal,backPointerCellDict,parse,wordTags,parseList,False)
                        count += 1
                #assign split symbol to break up parses
                parse.append('\n')

        return parse
    ############################################################################

    def reconstructParse(self, nonTerminal,map,parse,wordTags,parseList,isComplete):

        while not isComplete:
            parse.append(' (')
            parse.append(nonTerminal._symbol)
            parse.append(' ')

            i = map.get('i')
            j = map.get('j')
            if i == 0 and j == 1:#signifies the start of the parse
                parse.append(self.getWordTag(map,wordTags))
                isComplete = True
            else:
                #Does nonterminal have child elements
                for dict in parseList:
                    if nonTerminal in dict.keys():
                        tempNT = dict.get(nonTerminal)
                        nt = tempNT[0].get(nonTerminal)#find nonterminal from pointer
                        if nt.get('i') == i and nt.get('j') == j:
                            #first get the const to evaluate against
                            #get both constituents
                            const1 = tempNT[1]
                            c1 = copy.copy(const1)
                            nonTermConst1 = c1.popitem()
                            #does constituent one have children?
                            for child in parseList:
                                if nonTermConst1[0] in child.keys():
                                    tempNTC1 = child.get(nonTermConst1[0])
                                    ntC1 = tempNTC1[0].get(nonTermConst1[0])
                                    if ntC1.get('i') == tempNT[1].get(nonTermConst1[0]).get('i') and ntC1.get('j') == tempNT[1].get(nonTermConst1[0]).get('j'):
                                        #child found
                                        self.reconstructParse(nonTermConst1[0],nonTermConst1[1],parse,wordTags,parseList,isComplete)
                            else:
                                #no child elements, get word association
                                parse.append(self.getWordTag(nonTermConst1[1],wordTags))
                                parse.append(')')
                            #does constituent two have children?
                            const2= tempNT[2]
                            c2 = copy.copy(const2)
                            nonTermConst2 = c2.popitem()
                            for child in parseList:
                                if nonTermConst2[0] in child.keys():
                                    tempNTC2 = child.get(nonTermConst2[0])
                                    ntC2 = tempNTC2[0].get(nonTermConst2[0])
                                    if ntC2.get('i') == tempNT[2].get(nonTermConst2[0]).get('i') and ntC2.get('j') == tempNT[2].get(nonTermConst2[0]).get('j'):
                                        #child found
                                        self.reconstructParse(nonTermConst2[0],nonTermConst2[1],parse,wordTags,parseList,isComplete)
                            else:
                                #has no children, get word
                                parse.append(self.getWordTag(nonTermConst2[1],wordTags))
                                parse.append(')')
                                isComplete = True


        return parse


    def getWordTag(self, map,wordTags):
        word = ''
        try:
            for wordDict in wordTags:
                items = wordDict.items()
                for e in items:
                    i = e[1].get('i')
                    j = e[1].get('j')
                    if i == map.get('i') and j == map.get('j'):
                        word = e[0]
                        raise StopIteration("getWordTag: word[%s] found --> cell[%d,%d]"%(word,i,j))

        except StopIteration as si:
            print("StopIteration: %s"%str(si))

        return word



