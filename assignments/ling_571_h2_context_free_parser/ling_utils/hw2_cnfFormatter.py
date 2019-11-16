import copy

import nltk
from ling_utils.cnf_dataStructures import CFNDataStructures


###########################################################################################################################
# **HW2**
#       Convert GCF Grammar file to a CNF Grammar file
# **HW2**
###########################################################################################################################
cfnDataStructures = CFNDataStructures()

def convertGCFToCNF(productionsList,startSymbol,grammar):
    rulesDicKey = 0
    for i in productionsList:
        lhs = i.lhs()
        rhsList = i.rhs()
        if lhs == startSymbol:
            cfnDataStructures.startProductionRules.add(i)
        if len(rhsList) > 2:
            cfnDataStructures.longProductionRules.add(i)
        elif (len(rhsList) == 2 and not i.is_nonlexical()):
            cfnDataStructures.hybridProductionRules.add(i)
        elif (len(rhsList) == 1 and i.is_nonlexical()):
            cfnDataStructures.unitProductionRules.add(i)
        else:
            cfnDataStructures.cnfRules.add(i)

    #End looping through production list to separate out the rule types
    print("\nstartProductionRules: %s" %str(cfnDataStructures.getstartProductionRules()))
    print("\nlongProductionRules: %s" %str(cfnDataStructures.getlongProductionRules()))
    print("\nhybridProductionRules: %s" %str(cfnDataStructures.gethybridProductionRules()))
    print("\nunitProductionRules: %s" %str(cfnDataStructures.getunitProductionRules()))
    print("\ncnfRules: %s" %str(cfnDataStructures.getcnfRules()))


    subNameCount = 1
    #create copy of productionsList to update while iterating over production lists
    origProductionsList = copy.deepcopy(productionsList)

    try:
        print("Starting productions list count [%d]"%len(productionsList))
        print("Original Production list: [ %s ]"%productionsList)

        #loop through productions to find all long rules
        print("\nStarting Long Rule Analysis, production list count [%d]"%len(productionsList))
        for prod in productionsList:
            count = 0
            prodLHS = prod.lhs()
            prodRHS = prod.rhs()
            print("Production LHS[%s] and RHS[%s]" %(str(prodLHS),str(prodRHS)))
            prodRHSLength = len(prodRHS)

            if prodRHSLength > 2:
                print("Appling greater than 2 rule, Production index[%d] length[%d] content[%s]" %(count,prodRHSLength,prod))
                newProds = cnfConversionRuleLongProductions(prod,subNameCount)
                print("Removing original production[%s] from production list"%str(prod))

                try:
                    origProductionsList.remove(prod)
                    cfnDataStructures.removedProductionRules.add(prod)
                    origProductionsList.extend(newProds)
                except Exception as e:
                    print("****WARNING****: production[%s] does not exist in original production list"%str(prod))

                print("Added these new productions to the list: [ %s ]" %str(newProds))
                subNameCount = subNameCount + len(newProds) - 1
            #End If condition
            count += 1
        #End for-loop through productions to find long rules
        print("\nCompleted Long Rule Analysis: prodL1 [%d], prodL2 [%d] "%(len(productionsList),len(origProductionsList)))
        print("Completed Long Rule Analysis; Long Rule: Updated Production List [ %s ]\n"%origProductionsList)
        productionsList = []
        #productionsList = copy.deepcopy(origProductionsList)
        productionsList.extend(copy.deepcopy(origProductionsList))
        print("\n*****TEST Data Structures*****: cnfRules: size[%d] %s" %(cfnDataStructures.getcnfRules.__sizeof__(),str(cfnDataStructures.getcnfRules())))
        print("*****TEST Data Structures*****: removedProductionRules: size [%d] %s" %(cfnDataStructures.removedProductionRules.__sizeof__(),str(cfnDataStructures.removedProductionRules)))
        #########################################################################################################################

        #loop through productions to find all non lexical rules
        print("\nStarting Hybrid Rule Analysis, production list count [%d]"%len(productionsList))
        for prod in productionsList:
            count = 0
            prodLHS = prod.lhs()
            prodRHS = prod.rhs()
            print("Production LHS[%s] and RHS[%s]" %(str(prodLHS),str(prodRHS)))
            prodRHSLength = len(prodRHS)

            if prodRHSLength == 2 and not prod.is_nonlexical():
                print("Appling non-lexical rule, Production index[%d] length[%d] content[%s]" %(count,prodRHSLength,prod))
                newProds = cnfConversionRuleHybride(prod)
                print("Removing original production[%s] from production list"%str(prod))
                try:
                    origProductionsList.remove(prod)
                    cfnDataStructures.removedProductionRules.add(prod)
                    origProductionsList.extend(newProds)
                except Exception as e:
                    print("****WARNING****: production[%s] does not exist in original production list"%str(prod))

                print("Added these new productions to the list: [ %s ]" %str(newProds))
                subNameCount = subNameCount + len(newProds) - 1
            #End if condition
            count += 1
        #End for-loop through productions of non-lexical rules
        print("\nCompleted Hybrid Rule Analysis: prodL1 [%d], prodL2 [%d] "%(len(productionsList),len(origProductionsList)))
        print("Completed Hybrid Rule Analysis; Hybrid Rule: Updated Production List [ %s ]\n"%origProductionsList)
        productionsList = []
        #productionsList = copy.deepcopy(origProductionsList)
        productionsList.extend(copy.deepcopy(origProductionsList))
        print("\n*****TEST Data Structures*****: cnfRules: size[%d] %s" %(cfnDataStructures.getcnfRules.__sizeof__(),str(cfnDataStructures.getcnfRules())))
        print("*****TEST Data Structures*****: removedProductionRules: size[%d]\n %s" %(cfnDataStructures.removedProductionRules.__sizeof__(),str(cfnDataStructures.removedProductionRules)))

        #Test Data Structure - Nonterminals
        for i in productionsList:
            cfnDataStructures.nonTerminals.add(i.lhs())
            for e in i.rhs():
                if not isinstance(e,str) and e not in cfnDataStructures.nonTerminals:
                    cfnDataStructures.nonTerminals.add(e)
                #end if
            #end inner for loop
        #end outer for loop
        print("*****TEST Data Structures*****: nonTerminals: size[%d]\n %s" %(cfnDataStructures.nonTerminals.__sizeof__(),str(cfnDataStructures.nonTerminals)))

        ###########################################################################################################################

        #loop through productions to find all unit productions rules
        #Test Data Structure - Nonterminal Dictionary
        for i in cfnDataStructures.nonTerminals:
            try:
                tempSet = grammar.leftcorners(i)
                cfnDataStructures.nonTerminalsDict.__setitem__(i,tempSet)
            except Exception as e:
                print("*****WARNING*****: Caught Exception getting left corners; %s"%str(e))
        print("*****TEST Data Structures*****: nonTerminalsDictionary: size[%d]\n %s" %(cfnDataStructures.nonTerminalsDict.__sizeof__(),str(cfnDataStructures.nonTerminalsDict)))

        print("\nStarting Unit Production Rule Analysis, production list count [%d]"%len(productionsList))
        for prod in productionsList:
            count = 0
            prodLHS = prod.lhs()
            prodRHS = prod.rhs()
            print("Production LHS[%s] and RHS[%s]" %(str(prodLHS),str(prodRHS)))
            prodRHSLength = len(prodRHS)

            if prodRHSLength == 1 and prod.is_nonlexical():
                print("Appling single, Unit Productions Rule, Production index[%d] length[%d] content[%s]" %(count,prodRHSLength,prod))
                newProds = cnfConversionRuleUnitProductions(prod,productionsList)
                print("Removing original production[%s] from production list"%str(prod))
                try:
                    origProductionsList.remove(prod)
                    origProductionsList.extend(newProds)
                except Exception as e:
                    print("****WARNING****: production[%s] does not exist in original production list"%str(prod))

                print("Added these new productions to the list: [ %s ]" %str(newProds))
                subNameCount = subNameCount + len(newProds) - 1
            #End If Condition
            count += 1
        #End for-loop of productionsList
        print("\nCompleted Unit Production Rule Analysis: prodL1 [%d], prodL2 [%d] "%(len(productionsList),len(origProductionsList)))
        print("Completed Unit Production Rule Analysis; Unit Productions Rule: Updated Production List [ %s ]\n"%origProductionsList)
        productionsList = []
        print("\n*****TEST Data Structures*****: cnfRules: count[%d] size[%d] %s" %(cfnDataStructures.cnfRulesCount,cfnDataStructures.getcnfRules.__sizeof__(),str(cfnDataStructures.getcnfRules())))
        ####################################################################################################################################

    except Exception as e:
        print("Caught Exception: " +str(e))

    return origProductionsList

#######################################################################
#   **HW2**     CNF Conversion - Hybrid Rule
#   Desc: Rules that mix terminals with non-terminals on the RHS
#   Parameters:
#       -production - Is the production rewrite
#   Return type: list(Production)
#######################################################################################################################
def cnfConversionRuleHybride(production):
    print("\nEntered cnfConversionRuleHybride: Production to Convert [%s]" %production)
    newSubProductionsList = set()
    lhs = production.lhs()
    rhsTuple = list(production.rhs())
    print("RHS [ %s ]"%str(rhsTuple))
    print("RHS [%s] type is [%s]" %(rhsTuple[0], type(rhsTuple[0])))
    print("RHS [%s] type is [%s]" %(rhsTuple[1], type(rhsTuple[1])))

    terminalIndex = 0
    tempProd = None
    try:
        for i in rhsTuple:
            if isinstance(i,str):
                print("instance of string value [%s]"%i)
                temp = i.capitalize()
                tempRHSList = [i]
                tempProd = nltk.grammar.Production(nltk.grammar.Nonterminal(temp),tempRHSList)
                print("New Production [%s]" %str(tempProd))
                terminalIndex = rhsTuple.index(i)
                print("Termainal Index [%d]"%terminalIndex)
                newSubProductionsList.add(tempProd)
                cfnDataStructures.cnfRules.add(tempProd)
                rhsTuple.remove(i)

        rhsTuple.insert(terminalIndex,tempProd.lhs())
        print("Temp RHS List [ %s ]"%str(rhsTuple))
        tempProd = nltk.grammar.Production(nltk.grammar.Nonterminal(lhs),rhsTuple)
        print("New Production [%s]" %str(tempProd))
        newSubProductionsList.add(tempProd)
        cfnDataStructures.cnfRules.add(tempProd)

    except Exception as e:
        print("*****ERROR*****: Caught Exception %s" %str(e))

    print("Exiting cnfConversionRuleHybride: Returning New Sub-Production List: [ %s ]" %str(newSubProductionsList))
    return list(newSubProductionsList)
#######################################################################

#######################################################################
#   **HW2**         CNF Conversion - Unit Productions Rule
#   Desc: Rules that have a single non-terminal on the RHS
#   Parameters:
#       -production - Is the production rewrite
#       -productionsList - The original List of productions to evaluate for unfolding the non-terminal
#       -subName - Is the count index of new non-terminal symbol
#   Return type: list(Production)
##################################################################################################################
def cnfConversionRuleUnitProductions(production,productionsList):
    print("\nEntered cnfConversionRuleUnitProductions: Production analyze Convert [%s]" %production)
    newSubProductionsList = set()
    lhs = production.lhs()
    rhsSymbol = production.rhs()[0]

    print("RHS Symbol to analyze[%s]"%str(rhsSymbol))

    #Test Data Structure -
    if rhsSymbol in cfnDataStructures.getnonTerminalsDict():
        tempSet = cfnDataStructures.getnonTerminalsDict().get(rhsSymbol)
        print("*****Test Data Structures*****: [%s] found in Nonterminal Dictionary, leftcorners are [%s]"%(str(rhsSymbol),str(tempSet)))

        for i in tempSet:
            terminalList = unpackNonterminal(i,productionsList)
            print("*****Test Data Structures*****: Returned terminal list [%s] to be made into new productions"%terminalList)
            for e in terminalList:
                temp = [e]
                newProduction = nltk.grammar.Production(lhs,temp)
                print("*****Test Data Structures*****: New Production, [%s], has been created"%str(newProduction))
                newSubProductionsList.add(newProduction)
                cfnDataStructures.cnfRules.add(newProduction)

    try:
        #Verify the single symbol is a non-terminal
        if not isinstance(rhsSymbol,str):
            #loop through productions list and where lhs is equal to
            #Unpack Nonterminal
            #terminal = unpackUnitProduction(rhsSymbol,productionsList)
            terminalList = unpackNonterminal(rhsSymbol,productionsList)
            print("Returned terminal list [%s] to be made into new productions"%terminalList)

            for i in terminalList:
                temp = [i]
                newProduction = nltk.grammar.Production(lhs,temp)
                print("New Production, [%s], has been created"%str(newProduction))
                newSubProductionsList.add(newProduction)
        else:
            print("[%s] unpacking not required" %rhsSymbol)

    except Exception as e:
        print("*****ERROR*****: Caught Exception: %s"%str(e))

    print("Exiting cnfConversionRuleUnitProductions: Returning New Sub-Production List: [ %s ]" %str(newSubProductionsList))
    return list(newSubProductionsList)
############################################################################################################################

#######################################################################
#   **HW2**         CNF Conversion - Long Productions
#   Desc: Rules in which the length of the RHS is greater than two
#   Parameters:
#       -production - Is the production rewrite
#       -subName - Is the count index of new non-terminal symbol
#   Return type: list(Production)
# #########################################################################################################################
def cnfConversionRuleLongProductions(production,subName):
    print("\nEntered cnfConversionRuleLongProductions: Production to Convert[%s] subNameSuffix[%d]" %(production,subName))
    newProductionsList = set()
    count = subName
    nonTerminalRootValue = 'X'
    lhs = production.lhs()
    rhsList = list(production.rhs())
    try:
        while len(rhsList) > 2:
            lhsSymbol = nonTerminalRootValue + str(count)
            tempList = [rhsList.pop(0),rhsList.pop(0)]
            print("RHS List [%s]" %str(tempList))
            newProduction = nltk.grammar.Production(nltk.grammar.Nonterminal(lhsSymbol),tempList)
            print("New NonTerminal Production [%s]" %str(newProduction))
            newProductionsList.add(newProduction)
            cfnDataStructures.cnfRules.add(newProduction)
            rhsList.insert(0,newProduction.lhs())
            print("New RHS Production List [%s]" %str(rhsList))
            count += 1

        newProduction = nltk.grammar.Production(nltk.grammar.Nonterminal(lhs),rhsList)
        print("New Production [%s]" %str(newProduction))
        newProductionsList.add(newProduction)
    except Exception as e:
        print("*****ERROR*****: Caught Exception %s"%str(e))

    print("Exiting cnfConversionRuleLongProductions: Returning New Sub-Production List: [ %s ]" %str(newProductionsList))
    return list(newProductionsList)
#############################################################################################################################






######################################################################################################
#   **HW2**    CNF Conversion - Unit Production - Subprocess
#   Desc: unpack a Nonterminal down to it's individual terminal reference
#   Parameters:
#       -symbol - Is the Nonterminal to unpack
#       -productionList - Is the complete list of grammar production rules to analyse
#   Return type: str(terminal)
######################################################################################################

def unpackNonterminal(symbol,productionList):
    print("Entered unpackNonterminal: symbol[%s]" %symbol)
    terminal = ''
    terminalSet = set()
    try:
        for prod in productionList:
            try:
                prodLHS = prod.lhs()
                if symbol == prodLHS:
                    #loop through production to find terminal
                    print("Symbols Equal, input[%s] production[%s] lhs[%s]" %(str(symbol), str(prod), str(prodLHS)))
                    #set content loop

                    if not prod.rhs()[0] in terminalSet:
                        if not isinstance(prod.rhs()[0],str): #Base terminating condition
                            print("RHS [%s] is a Nonterminal" %str(prod.rhs()[0]))
                            #tempRHS = unpackNonterminal(tempRHS,productionList)
                            print("Recursive trace [%s]-->[%s]" %(str(prodLHS), str(prod.rhs()[0])))
                            symbol = prod.rhs()[0]
                            raise StopIteration("Nonterminal [%s] found moving to next symbol"%str(prod.rhs()[0]))
                        else:
                            print("RHS [%s] is a terminal, add to terminal set [%s]"%(str(prod.rhs()[0]),str(terminalSet)))
                            terminal = prod.rhs()[0]
                            terminalSet.add(terminal)
                            #loop through production set to find all matching terminations
                            for e in productionList:
                                if prodLHS == e.lhs():
                                    print("adding [%s] to terminalSet[%s]"%(str(e.rhs()[0]),str(terminalSet)))
                                    terminalSet.add(e.rhs()[0])



            except StopIteration as si:
                print("****INFO***: Caught StopIteration; %s"%si.value)

    except Exception as e:
        print("*****ERROR*****: Caught Exception %s" %str(e))

    print("Exit unpackNonterminal: Terminals[%s]" %str(terminalSet))
    return list(terminalSet)
##############################################################################################################################
