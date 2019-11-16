import nltk, copy, collections


class CFNDataStructures():

    __grammarProductions = set()
    __startProductionRules = set()
    __unitProductionRules = set()
    __hybridProductionRules = set()
    __longProductionRules = set()
    __cnfRules = set()
    __nonTerminals = set()
    __removeProductionRules = set()
    __nonTerminalsDict = {}
    __newProductions = set()
    __terminalProductions = set()
    __originalGrammarProductionCount = 0
    __newRuleCounter = 1
    __grammarProductionCount = 0
    __unitProductionRulesCount = 0
    __hybridProductionRulesCount = 0
    __longProductionRulesCount = 0
    __cnfRulesCount = 0
    __nonTerminalsCount = 0
    __removeProductionRulesCount = 0
    __terminalProductionsCount = 0
    __nonTerminalsDictCount = 0

    def __init__(self, grammarProductions):
        self.name = 'CFNDataStructures'
        #self.__startProductionRules = set()
        #self.unitProductionRules = set()
        #self.hybridProductionRules = set()
        #self.longProductionRules = set()
        #self.cnfRules = set()
        #self.nonTerminals = set()
        #self.removeProductionRules = set()
        #self.nonTerminalsDict = {}
        #self.newProductions = set()
        self.__grammarProductions = grammarProductions.copy()
        self.__setoriginalGrammarProductionCount(len(grammarProductions))

        print("CFNDataStructures --> Constructor")

    def __setoriginalGrammarProductionCount(self,value):
        CFNDataStructures.__originalGrammarProductionCount = value

    def getstartProductionRules(self):
        return CFNDataStructures.__startProductionRules

    def getunitProductionRules(self):
        return self.__unitProductionRules

    def gethybridProductionRules(self):
        return self.__hybridProductionRules

    def getlongProductionRules(self):
        return self.__longProductionRules

    def getcnfRules(self):
        return self.__cnfRules

    def getremoveProductionRules(self):
        return self.__removeProductionRules

    def setnonTerminals(self):
        for i in self.__grammarProductions:
            self.__nonTerminals.add(i.lhs())
            for e in i.rhs():
                if isinstance(e,nltk.grammar.Nonterminal):
                    self.__nonTerminals.add(e)



    def getnonTerminals(self):
        return self.__nonTerminals

    def getnonTerminalsDict(self):
        return self.__nonTerminalsDict

    def getnewProductions(self):
        return self.__newProductions

    def getgrammarProductions(self):
        return self.__grammarProductions

    def setterminalProductions(self,productionsList):
        for i in productionsList:
            if len(i.rhs()) == 1 and i.is_lexical():
                self.__terminalProductions.add(i)

    def getterminalProductions(self):
        return self.__terminalProductions

    #update production set
    def updateGrammarProductions(self):
        for prod in self.getremoveProductionRules():
            self.getgrammarProductions().discard(prod)
        self.getgrammarProductions().update(self.getnewProductions())

    #Long Rule Count - Do this first
    def toCNFLongRuleConversion(self):
        print("** Running Long Rule cnf conversion Analysis")
        for prod in self.getgrammarProductions():
            if len(prod.rhs()) > 2:
                self.getlongProductionRules().add(prod)
                print("** Applying Long Rule cnf conversion to prodution [%s]"%str(prod))
                self.getremoveProductionRules().add(prod)
                #tempProds = (prod)
                lhs = prod.lhs()
                rhsList = list(prod.rhs())

                while True:
                    xTempNonTerminal = 'X'+str(self.__newRuleCounter)
                    xNonTerminal = nltk.grammar.Nonterminal(xTempNonTerminal)
                    tempRHSList = [rhsList.pop(0),rhsList.pop(0)]
                    newXProd = nltk.grammar.Production(xNonTerminal,tempRHSList)
                    print("**New Production [%s] created"%str(newXProd))
                    self.getnonTerminals().add(xNonTerminal)
                    self.getnewProductions().add(newXProd)
                    rhsList.insert(0,xNonTerminal)
                    if len(rhsList) <= 2:
                        newEndProduction = nltk.grammar.Production(lhs,rhsList)
                        print("**New Production [%s] created"%str(newEndProduction))
                        self.getnewProductions().add(newEndProduction)
                        break
                    self.__newRuleCounter += 1

        #update production set
        self.updateGrammarProductions()
    #End update of long rule

    #Hybrid Rule Conversion
    def toCNFHybridRuleConversion(self):
        print("** Running Hybrid Rule cnf conversion Analysis")

        for prod in self.getgrammarProductions():

           if len(prod.rhs()) == 2 and not prod.is_nonlexical():
               print("** Applying Hybrid Rule cnf conversion to production [%s]"%str(prod))
               self.gethybridProductionRules().add(prod)

               rhsIndex = 0
               tempRHSList = []
               for rhs in prod.rhs():
                   if not isinstance(rhs,nltk.grammar.Nonterminal):
                       print("Found terminal [%s] as a rhs attribute of production [%s]"%(rhs,str(prod)))
                       self.getremoveProductionRules().add(prod)
                       #rhs = rhs.unicode_repr()
                       newNonTerminal = nltk.grammar.Nonterminal(rhs)
                       print(newNonTerminal._symbol)
                       self.getnonTerminals().add(newNonTerminal)
                       print("**New NonTerminal [%s] created from string [%s]"%(str(newNonTerminal),str(rhs)))
                       newProduction1 = nltk.grammar.Production(newNonTerminal,[rhs])
                       print("**New Production [%s] created"%str(newProduction1))
                       self.getnewProductions().add(newProduction1)
                       if rhsIndex == 0:
                          tempRHSList.insert(0,prod.rhs()[1])
                       else:
                          tempRHSList.insert(0,prod.rhs()[0])
                       tempRHSList.insert(rhsIndex,newNonTerminal)
                       newProduction2 = nltk.grammar.Production(prod.lhs(),tempRHSList)
                       print("**New Production [%s] created"%str(newProduction2))
                       self.getnewProductions().add(newProduction2)
                #End for-loop
            #End if
        #End for-loop
        #update production set
        self.updateGrammarProductions()


    #End function

    #End Hybrid Rule Conversion

    #Unit Production Rule Conversion
    def toCNFUnitProductionRuleConversion(self):
        print("** Running Unit Production Rule cnf conversion Analysis")
        for prod in self.getgrammarProductions():
           if len(prod.rhs()) == 1 and prod.is_nonlexical():
               print("** Applying Unit Production Rule cnf conversion to prodution [%s]"%str(prod))
               self.getunitProductionRules().add(prod)
        #End for-loop
        #get all leftcorner non-terminals per unit production
        newProductionSet = set()
        for unit in self.getunitProductionRules():
            unitLHS = unit.lhs()
            symbol = unit.lhs()
            notComplete = True
            count = 0
            while notComplete:
                #Outter Most Unit Set
                recursionCount = 0
                try:
                    if symbol in self.getnonTerminalsDict():
                        unitLFTCornerSet = self.getnonTerminalsDict().get(symbol)
                        print("Symbol [%s], lftCornerSet [%s], recursion count [%d]"%(str(symbol),str(unitLFTCornerSet),recursionCount))
                        #unitLFTCornerSet = list(unitLFTCornerSet)
                        if symbol in unitLFTCornerSet:
                            unitLFTCornerSet.remove(symbol)
                        isRecursion = False

                        for item in unitLFTCornerSet:
                            print("item [%s]"%str(item))
                            for i in self.getgrammarProductions():
                                print("i [%s]"%str(i))
                                if i.lhs() == item:
                                    print("lhs [%s], item [%s]"%(str(i.lhs()),str(item)))
                                    if len(i.rhs()) == 1:
                                        print("i rhs length [%d]"%len(i.rhs()))
                                        if not isinstance(item,nltk.grammar.Nonterminal):
                                            print("Not instance of Nonterminal [%s]"%str(item))
                                            #is a terminal, make new production for this unit
                                            newProduction = nltk.grammar.Production(unitLHS,i.rhs())
                                            newProductionSet.add(newProduction)
                                            self.getnewProductions().add(newProduction)
                                            print("**New Production [%s] created"%str(newProduction))
                                        else:
                                            #recursive search
                                            print("Is a Nonterminal [%s]"%str(item))
                                            symbol = i.rhs()[0]
                                            print("***INFO***: New leftcorner lookup value [%s]"%str(symbol))
                                            if isinstance(symbol,nltk.grammar.Nonterminal):
                                                isRecursion = True
                                                recursionCount += 1
                                                raise StopIteration("StopIteration: Nonterminal Found, isRecursion[%s]"%isRecursion)
                                            else:
                                               print("Not instance of Nonterminal [%s]"%str(symbol))
                                               #is a terminal, make new production for this unit
                                               newProduction = nltk.grammar.Production(unitLHS,[symbol])
                                               newProductionSet.add(newProduction)
                                               self.getnewProductions().add(newProduction)
                                               print("**New Production [%s] created"%str(newProduction))
                                               #raise StopIteration("StopIteration: Single terminal found")
                                    else:
                                        #in CNF form, add new production
                                        #print("i rhs length > 1 [%d] i [%s]"(len(i.rhs()),str(i)))
                                        newProduction = nltk.grammar.Production(unitLHS,i.rhs())
                                        newProductionSet.add(newProduction)
                                        self.getnewProductions().add(newProduction)
                                        print("**New Production [%s] created"%str(newProduction))
                                        #raise StopIteration("StopIteration: Multiple RHS found")
                            #end loop on grammar productions

            


                except StopIteration:
                    print("StopIteration Raised, isRecursion[%s] notComplete[%s]"%(isRecursion,notComplete))
                    if isRecursion:
                        continue
                    else:
                        notComplete = False
                else:
                    print("Symbol [%s] not in nonterminal dict"%str(symbol))



            #mark unit production for removal
            self.getremoveProductionRules().add(unit)

        #End unit production search

        #update production set
        self.updateGrammarProductions()
    #End Unit Production Rule Conversion


    def printDataStructureReport(self):
        CFNDataStructures.__grammarProductionCount = len(self.getgrammarProductions())
        CFNDataStructures.__cnfRulesCount = len(self.getcnfRules())
        CFNDataStructures.__hybridProductionRulesCount = len(self.gethybridProductionRules())
        CFNDataStructures.__longProductionRulesCount = len(self.getlongProductionRules())
        CFNDataStructures.__nonTerminalsCount = len(self.getnonTerminals())
        CFNDataStructures.__unitProductionRulesCount = len(self.getunitProductionRules())
        CFNDataStructures.__removeProductionRulesCount = len(self.getremoveProductionRules())
        CFNDataStructures.__terminalProductionsCount = len(self.getterminalProductions())
        CFNDataStructures.__nonTerminalsDictCount = len(self.getnonTerminalsDict())
        print("***** CNF Data Structure Report: \n*** grammarProductions count at start [%d]"%CFNDataStructures.__originalGrammarProductionCount)
        print("*** grammarProductions count[%d]"%CFNDataStructures.__grammarProductionCount)
        print("*** cnfRulesCount count[%d]"%CFNDataStructures.__cnfRulesCount)
        print("*** hybridProductionRulesCount count[%d]"%CFNDataStructures.__hybridProductionRulesCount)
        print("*** longProductionRulesCount count[%d]"%CFNDataStructures.__longProductionRulesCount)
        print("*** nonTerminalsCount count[%d]"%CFNDataStructures.__nonTerminalsCount)
        print("*** unitProductionRulesCount count[%d]"%CFNDataStructures.__unitProductionRulesCount)
        print("*** removeProductionRulesCount count[%d]"%CFNDataStructures.__removeProductionRulesCount)
        print("*** terminalProductionsCount count[%d]"%CFNDataStructures.__terminalProductionsCount)
        print("*** nonTerminalsDict count[%d]"%CFNDataStructures.__nonTerminalsDictCount)

