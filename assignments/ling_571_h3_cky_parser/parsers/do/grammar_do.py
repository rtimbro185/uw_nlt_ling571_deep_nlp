import nltk, pprint, copy
from utils import common_utils
from collections import defaultdict

class GrammarDO():

    __grammarProductions = set()
    __nonTerminalProductions = set()
    __startProductionRules = set()
    __cnfRules = set()
    __nonTerminals = set()
    __nonTerminalsDict = {}
    __nonTerminalsParentsDict = {}
    __terminalProductions = set()
    __grammarProductionCount = 0
    __nonTerminalsCount = 0
    __terminalProductionsCount = 0
    __nonTerminalsDictCount = 0
    __nonTerminalsParentsDictCount = 0
    __wordsToParseCount = 0


    def __init__(self, grammar):
        self.name = 'GrammarDO'
        self.__grammar = grammar
        self.__grammarProductions = grammar.productions()
        self.setnonTerminals()
        self.setnonTerminalsDict()
        self.setterminalProductions(self.__grammarProductions)
        self.setnonTerminalProductions(self.__grammarProductions)
        self.setnonTerminalsParentsDict()


    def getstartProductionRules(self):
        return self.__startProductionRules

    def setnonTerminals(self):
        for i in self.__grammarProductions:
            self.__nonTerminals.add(i.lhs())
            for e in i.rhs():
                if isinstance(e,nltk.grammar.Nonterminal):
                    self.__nonTerminals.add(e)

    def setnonTerminalsParentsDict(self):
        #parents = set()
        for i in self.__nonTerminals:
            parents = self.__grammar.leftcorner_parents(i)
            #parents.discard(i)
            self.__nonTerminalsParentsDict.__setitem__(i,parents)

    def getnonTerminalProductions(self):
        return self.__nonTerminalProductions

    def getnonTerminalsParentsDict(self):
        return self.__nonTerminalsParentsDict

    def getnonTerminals(self):
        return self.__nonTerminals

    def setnonTerminalsDict(self):
        for i in self.getnonTerminals():
            self.getnonTerminalsDict().__setitem__(i,self.__grammar.leftcorners(i))

    def getnonTerminalsDict(self):
        return self.__nonTerminalsDict

    def getgrammarProductions(self):
        return self.__grammarProductions

    def setnonTerminalProductions(self,productionsList):
        for i in productionsList:
            if i.is_nonlexical():
                self.__nonTerminalProductions.add(i)

    def setterminalProductions(self,productionsList):
        for i in productionsList:
            if len(i.rhs()) == 1 and i.is_lexical():
                self.__terminalProductions.add(i)

    def getterminalProductions(self):
        return self.__terminalProductions

    def setwordsToParseCount(self,value):
        self.__wordsToParseCount = value

    def getwordsToParseCount(self):
        return self.__wordsToParseCount

    #HW-3; CKY Parser Implementation; TODO-Write up readme on the use of _symbol and casefold() methods
    def findWordPartsOfSpeech(self,word):
        resultSet = set()
        wordFound = False
        nonTerminal = None
        wordNonTerminal = None
        hasWordNonTerminal = False
        for i in self.getgrammarProductions():
            if i.is_lexical and not isinstance(i.rhs()[0],nltk.grammar.Nonterminal):
                if i.rhs()[0].casefold() == word.casefold():
                    nonTerminal = i.lhs()
                    if i.lhs()._symbol.casefold() == word.casefold():#Note: Add the finding of this _symbol method to readme
                        wordNonTerminal = i.lhs()
                        hasWordNonTerminal = True
                    else:
                       resultSet.add(nonTerminal)
                    wordFound = True
                    #break
        if hasWordNonTerminal:#Needed to find all of the Nonterminal parts of speech that the CNF conversion turned into Nonterminals
            for i in self.getgrammarProductions():
                if i.rhs()[0] == wordNonTerminal:
                    resultSet.add(i.lhs())

        #TODO: if the words not found raise an exception and skip this sentence
        if not len(resultSet) > 0 :
            resultSet = None

        return resultSet


#############################################################################################################
    #HW-3; find subconstituent
    def findSubConstituent(self,B,C):
        #print("findSubConstituent: B[%s] C[%s]"%(str(B),str(C)))
        constituents = set()
        for i in self.getgrammarProductions():
            #print("findSubConstituent: grammar production [%s]"%str(i))
            if len(i.rhs()) == 2:
                if i.rhs()[0] == B and i.rhs()[1] == C:
                    constituents.add(i.lhs())
                    #print("***** FOUND *****: findSubConstituent;[%s]"%str(constituents))
        if not len(constituents) > 0:
            constituents = None
        #else:
            #print("***** Return FOUND *****: findSubConstituent;[%s]"%str(constituents))

        return constituents

    def printDataStructureReport(self):
        self.__grammarProductionCount = len(self.getgrammarProductions())
        self.__nonTerminalsCount = len(self.getnonTerminals())
        self.__terminalProductionsCount = len(self.getterminalProductions())
        self.__nonTerminalsDictCount = len(self.getnonTerminalsDict())
        self.__nonTerminalsParentsDictCount = len(self.getnonTerminalsParentsDict())

        pprint.pprint("********** CNF Data Structure Report **********")
        pprint.pprint("*** grammarProductions count[%d]"%self.__grammarProductionCount)
        pprint.pprint("*** nonTerminalsCount count[%d]"%self.__nonTerminalsCount)
        pprint.pprint("*** terminalProductionsCount count[%d]"%self.__terminalProductionsCount)
        pprint.pprint("*** nonTerminalsDict count[%d]"%self.__nonTerminalsDictCount)
        pprint.pprint("*** nonTerminalsParentsDict count[%d]"%self.__nonTerminalsParentsDictCount)


class BaseParse():

    #__sentence = None
    #__parseCount = 0
    #__sentenceWordCount = 0
    #__parseList = []
    #__parseFound = False
    #__startSymbol = None
    #__nonTerminalMap = None
    #__parse = None

    def __init__(self,sentence,start):
        self.__sentence = sentence
        self.__startSymbol = start
        self.__sentenceWordCount = len(self.__sentence.split(' '))
        self.__parseList = []
        self.__parseFound = False
        self.__nonTerminalMap = None
        self.__parse = None
        self.__partsOfSpeechNonTerminalBackPointers = []
        self.__partsOfSpeechFinalNonTerminalBackPointers = []

    def __str__(self):
        return '%s%s\nNumber of parses: %d' % (self.__sentence,self.__parseList,len(self.__parseList))

    def findParses(self,finalList,completeList):
        self.__nonTerminalMap = completeList
        for e in finalList:
            if self.__startSymbol in e.keys():
                self.parseFound = True
                nonTerminalList = copy.copy(e.get(self.__startSymbol))
                for nt in nonTerminalList:
                    temp = nt.popitem()
                    if temp[1].get('i') == 0 and temp[1].get('j') == self.__sentenceWordCount:
                        self.__parse = '('+temp[0]._symbol
                    else:
                        self.reconstructParse(temp[0],temp[1],False)

                #end parse
                for i in nonTerminalList:
                    self.__parse = self.__parse+')'
                self.__parseList.append(self.__parse)

    def reconstructParse(self,nonTerminal,map,isComplete):
            while not isComplete:
                self.__parse = self.__parse+' ('+nonTerminal._symbol
                i = map.get('i')
                j = map.get('j')
                if i == 0 and j == 1:# signifies the start of the parse
                    self.__parse = self.__parse+')'
                    isComplete = True
                    return
                for dict in self.__nonTerminalMap.copy():
                    if nonTerminal in dict.keys():
                        temp = dict.get(nonTerminal)
                        nt = temp[0].get(nonTerminal)
                        if nt.get('i') == i and nt.get('j') == j:
                            #get both constituents
                            const1 = temp[1]
                            c1 = copy.copy(const1)
                            const2 = temp[2]
                            c2 = copy.copy(const2)
                            nonTermConst1 = c1.popitem()
                            nonTermConst2 = c2.popitem()
                            self.__parse = self.__parse+'('+nonTermConst1[0]._symbol
                            self.__parse = self.__parse+'('+nonTermConst2[0]._symbol
                            isComplete = True
                            return
                else:
                    self.reconstructParse(nonTerminal,map,isComplete)

    def printToFile(self,fileName,filePath):
        common_utils.outputToFile(self,fileName,filePath)

##############################################################################################################
  #HW-3 Backpointers
    def storeBackPointers(self,list):
        self.__partsOfSpeechNonTerminalBackPointers.append(list)

    def getBackPointers(self):
        return self.__partsOfSpeechNonTerminalBackPointers

    def clearBackPointers(self):
        self.__partsOfSpeechNonTerminalBackPointers.clear()

    def storeFinalBackPointers(self,list):
        self.__partsOfSpeechFinalNonTerminalBackPointers.append(list)

    def getFinalBackPointers(self):
        return self.__partsOfSpeechFinalNonTerminalBackPointers

    def clearFinalBackPointers(self):
        self.__partsOfSpeechFinalNonTerminalBackPointers.clear()

#############################################################################################################
