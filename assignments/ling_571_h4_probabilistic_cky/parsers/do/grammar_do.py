import nltk, pprint, copy, math

class GrammarDO():

    grammarProductions = set()
    nonTerminalProductions = set()
    startProductionRules = set()
    cnfRules = []
    nonTerminals = set()
    nonTerminalsDict = {}
    nonTerminalsParentsDict = {}
    terminalProductions = set()
    grammarProductionCount = 0
    nonTerminalsCount = 0
    terminalProductionsCount = 0
    nonTerminalsDictCount = 0
    nonTerminalsParentsDictCount = 0
    wordsToParseCount = 0
    unrecognizedTokensList = []
    nonParsedSentences = []



    def __init__(self, grammar):
        self.name = 'GrammarDO'
        self.grammar = grammar
        self.grammarProductions = grammar.productions()
        self.setnonTerminals()
        self.setnonTerminalsDict()
        self.setterminalProductions(self.grammarProductions)
        self.setnonTerminalProductions(self.grammarProductions)
        self.setnonTerminalsParentsDict()
        #self.initCnfRules()

    def getstartProductionRules(self):
        return self.startProductionRules

    def setnonTerminals(self):
        for i in self.grammarProductions:
            self.nonTerminals.add(i.lhs())
            for e in i.rhs():
                if isinstance(e,nltk.grammar.Nonterminal):
                    self.nonTerminals.add(e)

    def setnonTerminalsParentsDict(self):
        #parents = set()
        for i in self.nonTerminals:
            parents = self.grammar.leftcorner_parents(i)
            #parents.discard(i)
            self.nonTerminalsParentsDict.__setitem__(i,parents)

    def getnonTerminalProductions(self):
        return self.nonTerminalProductions

    def getnonTerminalsParentsDict(self):
        return self.nonTerminalsParentsDict

    def getnonTerminals(self):
        return self.nonTerminals

    def setnonTerminalsDict(self):
        for i in self.getnonTerminals():
            self.getnonTerminalsDict().__setitem__(i,self.grammar.leftcorners(i))

    def getnonTerminalsDict(self):
        return self.nonTerminalsDict

    def getgrammarProductions(self):
        return self.grammarProductions

    def setnonTerminalProductions(self,productionsList):
        for i in productionsList:
            if i.is_nonlexical():
                self.nonTerminalProductions.add(i)

    def setterminalProductions(self,productionsList):
        for i in productionsList:
            if len(i.rhs()) == 1 and i.is_lexical():
                self.terminalProductions.add(i)

    def getterminalProductions(self):
        return self.terminalProductions

    def setwordsToParseCount(self,value):
        self.wordsToParseCount = value

    def getwordsToParseCount(self):
        return self.wordsToParseCount

############################################################################################################################
#####HW4-added to find unrecognized in sentences that the grammar isn't accounting for
    def setUnrecognizedTokensList(self,msg):
        self.unrecognizedTokensList.append(msg.split(':')[1])

    #HW4-added to find unrecognized in sentences that the grammar isn't accounting for
    def getUnrecognizedTokensList(self):
        return self.unrecognizedTokensList
#############################################################################################################################

####HW4-adding attribute to track unparsed sentences
    def setNonParsedSentences(self,sentence):
        self.nonParsedSentences.append(sentence)

    def getNonParsedSentences(self):
        return self.nonParsedSentences
#############################################################################################################################

####HW4-adding attribute to track Rules######################################################################################
    def setCnfRules(self,rule):
        self.cnfRules.append(rule)

    def getCnfRules(self):
        return self.cnfRules

    def initCnfRules(self):
        for prod in self.grammarProductions:
            self.cnfRules.append(prod)
#############################################################################################################################



#############################################################################################################################
# HW-3; CKY Parser Implementation; TODO-Write up readme on the use of _symbol and casefold() methods
# HW-4; Updated to include probabilities
#############################################################################################################################
    def findWordPartsOfSpeech(self,word):
        resultSet = {} #HW4-modify from set to dictionary object to capture probability
        wordFound = False
        nonTerminal = None
        wordNonTerminal = None
        hasWordNonTerminal = False
        for i in self.getgrammarProductions():
            if i.is_lexical and not isinstance(i.rhs()[0],nltk.grammar.Nonterminal):
                if i.rhs()[0] == word:
                    nonTerminal = i.lhs()
                    #if i.lhs()._symbol.casefold() == word.casefold():#HW4-TODO: Note removal of casefold, 'List' versus 'list' both in grammar
                    if i.lhs()._symbol == word:
                        wordNonTerminal = i.lhs()
                        hasWordNonTerminal = True
                    else:
                       prob = i.prob()#HW4-TODO: Note the finding of prob() in NLTK documentation
                       resultSet.__setitem__(nonTerminal,prob)
                       #resultSet.add(nonTerminal)
                    wordFound = True
                    #break
        if hasWordNonTerminal:#Needed to find all of the Nonterminal parts of speech that the CNF conversion turned into Nonterminals
            for i in self.getgrammarProductions():
                if i.rhs()[0] == wordNonTerminal:
                    #resultSet.add(i.lhs())
                    prob = i.prob()
                    resultSet.__setitem__(i.lhs(),prob)
        #TODO: if the words not found raise an exception and skip this sentence
        if not len(resultSet) > 0 :
            resultSet = None

        return resultSet
## End findWordPartsOfSpeech(self,word)#################################################################################

########################################################################################################################
#  HW-3; find subconstituent
#  HW-4; update to include probabilities
########################################################################################################################
    def findSubConstituent(self,B,Bprob,C,Cprob):
        #print("findSubConstituent: B[%s] C[%s]"%(str(B),str(C)))
        #constituents = set()
        constituents = {} #HW4-Updated to include probabilities
        for i in self.getgrammarProductions():
            #print("findSubConstituent: grammar production [%s]"%str(i))
            if len(i.rhs()) == 2:
                if i.rhs()[0] == B and i.rhs()[1] == C:
                    prob = i.prob()
                    #constituents.add(i.lhs())
                    #totalProb = prob*Bprob*Cprob #HW4-updated to sum probabilities
                    totalProb_log = math.log1p(prob)*math.log1p(Bprob)*math.log1p(Cprob) #HW4-updated to sum probabilities
                    #constituents.__setitem__(i.lhs(),totalProb)
                    constituents.__setitem__(i.lhs(),totalProb_log)
                    #print("***** FOUND *****: findSubConstituent;[%s]"%str(constituents))
        if not len(constituents) > 0:
            constituents = None
        #else:
            #print("***** Return FOUND *****: findSubConstituent;[%s]"%str(constituents))

        return constituents
# End findSubConstituent(self,B,C)######################################################################################
########################################################################################################################
#  HW-4; TODO: READ_ME: Filter utility function to remove lower probability constituents
########################################################################################################################
    def removeLowerProbabilityPointer(self,kConstituent,row,col,pointers):



        constList = pointers[kConstituent]
        const = constList[0]
        constI = const.get("i")
        constJ = const.get("j")


        return pointers
########################################################################################################################
#
########################################################################################################################
    def printDataStructureReport(self):
        self.grammarProductionCount = len(self.getgrammarProductions())
        self.nonTerminalsCount = len(self.getnonTerminals())
        self.terminalProductionsCount = len(self.getterminalProductions())
        self.nonTerminalsDictCount = len(self.getnonTerminalsDict())
        self.nonTerminalsParentsDictCount = len(self.getnonTerminalsParentsDict())

        pprint.pprint("********** CNF Data Structure Report **********")
        pprint.pprint("*** grammarProductions count[%d]"%self.grammarProductionCount)
        pprint.pprint("*** nonTerminalsCount count[%d]"%self.nonTerminalsCount)
        pprint.pprint("*** terminalProductionsCount count[%d]"%self.terminalProductionsCount)
        pprint.pprint("*** nonTerminalsDict count[%d]"%self.nonTerminalsDictCount)
        pprint.pprint("*** nonTerminalsParentsDict count[%d]"%self.nonTerminalsParentsDictCount)
        pprint.pprint("*** unrecognized sentence words:\n %s"%self.getUnrecognizedTokensList())
        pprint.pprint("*** non-parsed sentences:\n%s"%self.getNonParsedSentences())




