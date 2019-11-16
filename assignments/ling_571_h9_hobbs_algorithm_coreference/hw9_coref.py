"""#### LING 571: Homework #9 - Ryan Timbrook #######################################################################
    Thesaurus-based words sense disambiguation
Author: Ryan Timbrook
Date: 03/15/2016

Program Name: hw9_coref.py - Program which implements the automatic processing phase of your Hobbs algorithm-based
                                pronoun resolution approach

    Invoked as: hw9_coref.py <input_grammar_filename> <test_sentence_filename> <output_filename>
    where:
        <input_grammar_filename>: The name of the file that holds the grammar to be used to parse the sentences.
        <test_sentence_filename>: The name of the file that holds the pairs of sentences that form contexts
                                    for pronoun resolution.
        <output_filename>: The name of the file to which the results of automatic processing for this assignment
                            will be written, either:
                                Parsing and pronoun identification only, or
                                Parsing through candidate antecedent identification
        """

import sys, nltk
from collections import defaultdict, OrderedDict, deque
from nltk.tree import ParentedTree
from nltk.util import breadth_first
from nltk.corpus import names

#####################################################################################################################
#  Main Controller Function
#####################################################################################################################
def main(argv):
    if argv is None:
        argv = sys.argv
    c = 0
    for arg in argv:
        print("hw9_coref.main: argv%d[%s]"%(c,argv[c]))
        c+=1

    #Load Feature-based grammar
    grammar = nltk.data.load(argv[1])
    buildAgreementTable()

    #Load Test Sentences
    sents = open(argv[2])

    #Open output file for writing
    outputFile = open(argv[3],'a')
    sentPairs = []
    pronouns = []
    for sent in sents.readlines():
        if sent != '\n':
            sent = sent[:-1]
            sentPairs.append(sent)
        else:
            #parse sentence pairs
            discourse = nesteddict()
            earley = nltk.parse.EarleyChartParser(grammar)
            pronouns = findPronouns(sentPairs,earley,grammar)
            for pronoun in pronouns:
                discourse.update({'NUM_SENT':len(sentPairs),'NUM_PRO':len(pronouns)})
                outputFile.write(pronoun+' ')
                for s in sentPairs:
                    parses = list(earley.chart_parse(nltk.word_tokenize(s)).parses(grammar.start()))
                    if len(parses) == 0:
                        outputFile.write(str('\n'))
                        print("NO PARSES --> for %s:\n"%s)
                    else:
                        for tree in parses:
                            outputFile.write(tree._pformat_flat('','()',quotes=False)+'   ')
                            break
                outputFile.write(str('\n'))
                hobbs(discourse,pronoun,sentPairs,earley,grammar,outputFile)
            outputFile.write(str('\n'))
            outputFile.flush()
            #clear sentence pairs list before getting the next grouping
            sentPairs = []


    outputFile.flush()
    outputFile.close()
######################################################################################################################
#
######################################################################################################################
def hobbs(discourse,pronoun,sentPairs,earley,grammar,outputFile):
    trees = []
    trees.append(getParses(sentPairs[1],earley,grammar))

    #step 1 - Begin at NP immediately dominating pronoun
    discourse.update({'SENT':0})
    discourse = hobbsStartingPoint(discourse,pronoun,trees[0])

    #step 2 - Climb tree to NP or S node
    discourse.update(hobbsNPCrawlClimb(discourse['START_NP_POSITION'],trees[0],discourse))

    #step 3 - Traverse branches below X, BF, LR
    discourse.update(hobbsNPCrawlTraverse(discourse,trees[0],pronoun,outputFile))
    if discourse['ANTECEDENT_FOUND'] == True:
        pass
        return

    #step 4 - If node X is the highest S node in sentence, traverse previous sentences (most recent first)
    trees.append(getParses(sentPairs[0],earley,grammar))
    discourse.update({'SENT':1})
    discourse.update({'X':None,'p':None,'TOP_S':False,'START_NP_POSITION':None})
    discourse.update(hobbsNPCrawlSearch(trees[1],discourse,pronoun,outputFile))



######################################################################################################################
#  Hobbs Algorithm; get starting point (NP immediately dominating pronoun)
#######################################################################################################################
def hobbsStartingPoint(discourse,pronoun,tree):
    startingNPPosition = None
    pronounPosition = tree.leaf_treeposition(tree.leaves().index(pronoun))
    pronounParent = tree[pronounPosition[:-1]]
    discourse.update({'CAT_PRO':pronounParent.label(),'ORTH_PRO':pronoun})
    discourse.update({'CAT_PROP_ANT':None,'ORTH_PROP_ANT':None,'ANTECEDENT_FOUND':False})

    for npNode in breadthFirstSearch(tree.root(),getChildNodes):
        if npNode.label() == 'NP':
            startingNPPosition = npNode.treeposition()
            break

    discourse.update({'START_NP_POSITION':startingNPPosition})
    return discourse

######################################################################################################################
#  Hobbs Algorithm; node crawl; climb tree to NP or S node
#######################################################################################################################
def hobbsNPCrawlClimb(start,tree,discourse):
    path = defaultdict(list)
    decrement = 1

    while True:
        if tree[start[:-decrement]].label() == 'NP':
            path[tree[start[:-decrement]].label()].append(start[:-decrement])
            discourse.update({'X':tree[start[:-decrement]].label(),'p':path,'NP_Climb_POSITION':start[:-decrement]})

            break
        elif tree[start[:-decrement]].label() == 'S':
            path[tree[start[:-decrement]].label()].append(start[:-decrement])
            discourse.update({'X':tree[start[:-decrement]].label(),'p':path})
            isTopSNode(discourse,start[:-decrement],tree)
            break

        path[tree[start[:-decrement]].label()].append(start[:-decrement])
        decrement+=1

    return discourse

######################################################################################################################
#  Hobbs Algorithm; node crawl; traverse branches below X, and left of p: BR,LR
#######################################################################################################################
def hobbsNPCrawlTraverse(discourse,tree,pronoun,outputFile):

    if discourse['X'] == 'S' and discourse['TOP_S'] == True:
        outputFile.write(tree._pformat_flat('','()',quotes=False)+'\n')
        return discourse

    hobbsNPCrawlSearch(tree,discourse,pronoun,outputFile)

    return discourse

#######################################################################################################################
#
#######################################################################################################################
def hobbsNPCrawlSearch(tree,discourse,pronoun,outputFile):
    pathSteps = defaultdict(list)
    searchNode = tree.root()
    if discourse['TOP_S'] != True:
        firstPass = True
        for tnode in breadthFirstSearch(searchNode,getChildNodes):
            if tnode.label() == 'S':
                if isTopSNode(discourse,tnode.treeposition(),tree) and firstPass:
                    pathSteps[tnode.label()].append(tnode.treeposition())
                    discourse.update({'X':tnode.label(),'p':pathSteps})
                    performProposeAntecedent(tnode,outputFile,pronoun,discourse,tree)
                    if discourse['ANTECEDENT_FOUND'] == True:
                        pass
                        break
                else:
                    print("Top S...")
                    break

            if tnode.label() == 'NP' and discourse['START_NP_POSITION'] is None:
                pathSteps[tnode.label()].append(tnode.treeposition())
                discourse.update({'X':tnode.label(),'p':pathSteps,'START_NP_POSITION':tnode.treeposition()})
                #propose NP
                performProposeAntecedent(tnode,outputFile,pronoun,discourse,tree)

                if discourse['ANTECEDENT_FOUND'] == True:
                    pass
                    break

            elif tnode.label() == 'NP' and not discourse['START_NP_POSITION'] is None:
                if discourse['SENT'] == 0 and not isBelowNode(tree,tnode.treeposition(),discourse['START_NP_POSITION']):
                    break
                pathSteps[tnode.label()].append(tnode.treeposition())
                discourse.update({'X':tnode.label(),'p':pathSteps})
                #Did pass through Nom?
                #npInd = list(tree.treepositions()).index(tnode.treeposition())
                #npC = tree[list(tree.treepositions())[npInd+1]].label()

                npPosit = list(tree.treepositions()).index(discourse['p']['NP'][-1])
                nomPosit = list(tree.treepositions()).index(discourse['p']['Nom'][-1])
                try:
                    if npPosit - nomPosit > 1:
                        performProposeAntecedent(tnode,outputFile,pronoun,discourse,tree)
                        if discourse['ANTECEDENT_FOUND'] == True:
                            break
                    else:
                        print()

                except Exception as e:
                    print("caught exception np position count to nom --> %s"%str(e))
                    pass


            elif tnode.label() == 'SBAR':
                pathSteps[tnode.label()].append(tnode.treeposition())
                discourse.update({'X':tnode.label(),'p':pathSteps,'TOP_S':False})
                performProposeAntecedent(tnode,outputFile,pronoun,discourse,tree)
                if discourse['ANTECEDENT_FOUND'] == True:
                    pass
                    break

            else:
                pathSteps[tnode.label()].append(tnode.treeposition())

            firstPass = False

    return discourse

######################################################################################################################
#
######################################################################################################################
def isBelowNode(tree,i_node_position,j_node_position):
    i = list(tree.treepositions()).index(i_node_position)
    j = list(tree.treepositions()).index(j_node_position)
    if i > j:
        return True
    else:
        return False

######################################################################################################################
#
######################################################################################################################
def isTopSNode(discourse,position,tree):
    tPositions = list(tree.treepositions())
    if position == tPositions[0]:
        discourse.update({'TOP_S':True})
        return True
    else:
        discourse.update({'TOP_S':False})
        return False

#######################################################################################################################
#
#######################################################################################################################
def findPronouns(sentPairs,earley,grammar):
    pronouns = []
    for proximalSent in reversed(sentPairs):
        partsOfSpeech = list(earley.chart_parse(nltk.word_tokenize(proximalSent)).parses(grammar.start()))[0].pos()
        for pos in partsOfSpeech:
            if pos[1] == 'PRP' or pos[1] == 'PossPro':
                pronouns.append(pos[0])
        break

    return pronouns

#######################################################################################################################
#
#######################################################################################################################
def performProposeAntecedent(tnode,outputFile,pronoun,discourse,tree):

    if discourse['X'] != 'S' and discourse['X'] != 'SBAR':

        for snode in breadthFirstSearch(tnode,getChildNodes):
            if snode.label() == 'NNP' or snode.label() == 'NN' or snode.label() == 'NNS':
                discourse.update({'CAT_PROP_ANT':snode.label(),'PARENT_POSIT_PROP_ANT':snode.treeposition()})
                posLex = snode.pos()[0][0]
                posLexPosition = tree.leaf_treeposition(tree.leaves().index(posLex))
                discourse.update({'ORTH_PROP_ANT':posLex,'ORTH_POSIT_PROP_ANT':posLexPosition})
                break

    outputFile.write(tnode._pformat_flat('','()',quotes=False)+'\n')
    proposed = proposeAntecedentConstraints(pronoun,discourse,tree)
    if discourse['X'] != 'S':
        outputFile.write(proposed+'\n')

    if proposed == 'Accept':
        discourse.update({'ANTECEDENT_FOUND':True})
    else:
        discourse.update({'ANTECEDENT_FOUND':False})
        discourse.update({'CAT_PRO':'','CAT_PROP_ANT':'','ORTH_PROP_ANT':'','ORTH_PROP_ANT':'','ORTH_POSIT_PROP_ANT':'','PARENT_POSIT_PROP_ANT':'','TOP_S':False})
    discourse.update({'X':'','p':None})
#######################################################################################################################
#
#######################################################################################################################
def proposeAntecedentConstraints(pronoun,discourse,tree):
    if discourse['X'] == 'S':
        return ''

    POS = agrTable
    reason = ''
    features = defaultdict(list)

    agree,gramAgr,posAgr,numAgr,perAgr,genAgr = False,False,False,False,False,False

    #get Parts of Speech constraints; Number, Person, Gender
    for element in POS:
        if discourse['CAT_PROP_ANT'] == POS[element]['CAT'] and discourse['ORTH_PROP_ANT'] in POS[element]['ORTHS']:
            features['propAntNum'].append(POS[element]['NUM'])
            features['propAntPer'].append(POS[element]['PERSON'])
            features['propAntGen'].append(POS[element]['GENDER'])
        elif discourse['CAT_PRO'] in POS[element]['CAT'] and discourse['ORTH_PRO'] in POS[element]['ORTHS']:
            features['proNum'].append(POS[element]['NUM'])
            features['proPer'].append(POS[element]['PERSON'])
            features['proGen'].append(POS[element]['GENDER'])
            features['proCat'].append(POS[element]['CAT'])

    try:
        #POS Agreement Condition Check
        for anum in features['propAntNum']:
            for pnum in features['propAntNum']:
                if pnum == anum:
                    numAgr = True; break
            if numAgr: break
        if not numAgr:
            if varAgr(features['propAntNum']) or varAgr(features['proNum']):
                numAgr = True
        if not numAgr:
            reason = reason+'Reject - Number '

        for aper in features['propAntPer']:
            for pper in features['proPer']:
                if aper == pper:
                    perAgr = True; break
            if perAgr: break
        if not perAgr:
            if varAgr(features['propAntPer']) or varAgr(features['proPer']):
                perAgr = True
        if not perAgr:
            reason = reason+'Reject - Person '

        for agen in features['propAntGen']:
            for pgen in features['proGen']:
                if agen == pgen:
                    genAgr = True; break
            if genAgr: break
        if not genAgr:
            if varAgr(features['propAntGen']) or varAgr(features['proGen']):
                genAgr = True
        if not genAgr:
            reason = reason+'Reject - Gender '

        if numAgr and perAgr and genAgr:
            posAgr = True

    except Exception as e:
        print("POS Agreement Constraint Validation: caught exception %s"%str(e))
        posAgr = False
        pass

    try:
        #Grammatical Role Validation; Subj > Object > IndObj > Oblique > AdvP
        for nps in list(tree.subtrees(filter=lambda x: x.label()=='NP')):
            subjRange = len(nps.treepositions());break
        for vps in list(tree.subtrees(filter=lambda x: x.label()=='VP')):
            objRange = list(tree.treepositions()).index(vps.treeposition());break
        gramRangeMarker = list(tree.treepositions()).index(discourse['ORTH_POSIT_PROP_ANT'])

        if valInFeature('SBJ',features['proCat']) and gramRangeMarker <= subjRange:
            gramAgr = True
        elif valInFeature('OBJ',features['proCat']) and gramRangeMarker >= objRange:
            gramAgr = True
        else:
            reason = reason+'Reject - Grammatical Role Violation'


    except ValueError as ve:
        print("Grammatical Role Validation: caught exception %s"%str(ve))
        gramAgr = False
        pass

    if posAgr and gramAgr:
        agree = True
        reason = 'Accept'

    return reason

######################################################################################################################
#
#######################################################################################################################
def varAgr(feature):
    for f in feature:
        if '?' in f[0]:
            return True
    else:
        return False

######################################################################################################################
#
#######################################################################################################################
def valInFeature(val, feature):
    for f in feature:
        if val in f:
            return True
    else:
        return False

######################################################################################################################
#
#######################################################################################################################
def breadthFirstSearch(tree,nodeChildren=iter,maxdepth=-1):
    queue = deque([(tree, 0)])
    while queue:
        node, depth = queue.popleft()
        yield node

        if depth != maxdepth:
            try:
                queue.extend((child, depth + 1) for child in nodeChildren(node))
            except TypeError:
                pass

######################################################################################################################
#
######################################################################################################################
def getChildNodes(tree):
    childNodes.clear()
    traverseTree(tree)
    chNodes = childNodes

    return chNodes

#######################################################################################################################
#
#######################################################################################################################
def traverseTree(tree):
    try:
        tree.label()
    except AttributeError:
        return
    else:
        if tree.height()==2:#child nodes
            return
        for child in tree:
            childNodes.append(child)
            traverseTree(child)

#######################################################################################################################
#
#######################################################################################################################
def getParses(sent,earley,grammar):
    tree = list(earley.chart_parse(nltk.word_tokenize(sent)).parses(grammar.start()))[0]
    ptree = ParentedTree.fromstring((str(tree)))
    return ptree

#######################################################################################################################
#
#######################################################################################################################
def buildAgreementTable():
    orths = []
    try:
        for i, line in enumerate(open('agreement.txt','r').readlines()):
            if line != '\n':
                pairs = line.replace('\n','').split(';')
                for e in pairs:
                    agrTable[i].update({e.split(':')[0]:e.split(':')[1]})
        for e in agrTable:
            orths = agrTable[e]['ORTHS'].split('|')
            agrTable[e].update({'ORTHS':orths})

    except IndexError:
        pass

    return agrTable

#######################################################################################################################
#   Declare and return a nested Dictionary object
#######################################################################################################################
def nesteddict():
    return defaultdict(nesteddict)

#######################################################################################################################
#
#######################################################################################################################
def gender_features(word):
    return{'last_letter':word[-1]}


#####################################################################################################################
# Globals
#####################################################################################################################
#discourse = defaultdict()
agrTable = nesteddict()
childNodes = []

#######################################################################################################################
# In-line process flow to call the main controller function
#######################################################################################################################
if __name__ == '__main__': main(sys.argv)