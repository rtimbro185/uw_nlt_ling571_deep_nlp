"""#### LING 571: Homework #8 - Ryan Timbrook #######################################################################
    Thesaurus-based words sense disambiguation
Author: Ryan Timbrook
Date: 03/8/2016

Program Name: hw8_resnik_wsd.py - implements thesaurus-based word sense disambiguation using
                                    a simplified "Resnik similarity" approach
    Invoked as: hw8_resnik_wsd.py <information_content_file_type> <wsd_test_filename> <output_filename>
    where:
        <information_content_file_type>: This string should specify the source of the information content file.
        <wsd_test_filename>: This is the name of the file that contains the lines of "probe-word, noun group words"
            pairs on which to evaluate your system.
        <output_filename>: This is the name of the file to which you should write your results.
        """
import sys, itertools
from collections import defaultdict, OrderedDict, Counter
from operator import itemgetter
from nltk.corpus import*
from nltk.corpus.reader.wordnet import information_content

#####################################################################################################################
#  Main Controller Function
#####################################################################################################################
def main(argv):
    if argv is None:
        argv = sys.argv
    c = 0
    for arg in argv:
        print("hw8_dist_similarity.main: argv%d[%s]"%(c,argv[c]))
        c+=1

    #Open output file for writing
    outputFile = open(argv[3],'a')

    #Read in file of (probe word, noun group) pairs
    wsdContexts = open(argv[2],'r')

    #Load IC values for WordNet from a file
    brownIC = wordnet_ic.ic('ic-brown-resnik-add1.dat')
    for line in wsdContexts.readlines():
        probeWord = line.split('\t')[0]
        nounGroup = line.split('\t')[1].replace('\n','').split(',')
        simMeasure(brownIC,probeWord,nounGroup,outputFile)

    outputFile.flush()
    outputFile.close()

## End main(argv)#####################################################################################################

#####################################################################################################################
#
#####################################################################################################################
def simMeasure(brownIC,probeWord,nounGroup,outputFile):
    concepts = []
    highestSims = defaultdict()
    probWordSynSet = [str(syn.name()) for syn in wordnet.synsets(probeWord, pos=wordnet.NOUN)]
    #nounWords = ()
    for ngWord in nounGroup:
        wspKey = probeWord+','+ngWord
        ngWordSynSet = [str(syn.name()) for syn in wordnet.synsets(ngWord, pos=wordnet.NOUN)]
        for ngWordSenses in ngWordSynSet:
            for pWordSenses in probWordSynSet:
                concepts.extend(lch(pWordSenses,ngWordSenses,brownIC))

        #Apply vote to highest Subsumer sense pairs
        highestSims.update(scoreHighestSubSumers(concepts,probeWord,ngWord))

        #Output similarity between the probe word and each noun group word
        outputFile.write('('+probeWord+','+ngWord+','+str(highestSims[wspKey]['sim_score'])+')'+'\t')


    preferredSense = getPreferredSense(highestSims)

    #Print Preferred Sense
    outputFile.write('\n')
    outputFile.write(preferredSense+'\n')

    return None

#####################################################################################################################
#
#####################################################################################################################
def lch(s_i, s_j, brownIC):
    ic = float()
    conceptICs = []
    rows = []

    s_i_hyperPaths = wordnet.synset(s_i).hypernym_paths()
    ij_commonHypernms = wordnet.synset(s_i).common_hypernyms(wordnet.synset(s_j))

    commonHypernsCount = len(ij_commonHypernms)
    for common in ij_commonHypernms:
        for i, i_path in enumerate(s_i_hyperPaths):
            commonDepthRanking = defaultdict()
            commonDepthRanking.__setitem__('cs',common.name())
            commonDepthRanking.__setitem__('path',i)
            commonDepthRanking.__setitem__('path_steps',len(i_path))
            step = 0
            steps = len(i_path)
            for path in i_path:
                if common.name() == path.name():
                    step = steps
                    commonDepthRanking.__setitem__('cs_path_step',step)
                    commonDepthRanking.__setitem__('cs_path_step_dist',int(len(i_path)-step))
                    rows.append(commonDepthRanking)
                    break
                else:
                    steps -= 1
            else:
                commonDepthRanking.__setitem__('cs_path_step',-1)
                commonDepthRanking.__setitem__('cs_path_step_dist',-1)
                rows.append(commonDepthRanking)
    #else:
        #print("lch: no common ancestry found for [%s] --> [%s]"%(s_i,s_j))


    lcsData = max(rows,key=itemgetter('cs_path_step_dist'))
    lcs = lcsData['cs']
    lcsHyposCount = len(wordnet.synset(lcs).hyponyms())
    ic = information_content(wordnet.synset(lcs),brownIC)
    conceptICs.append((ic,lcs,s_i,s_j))

    return conceptICs
#####################################################################################################################
#
#####################################################################################################################
def scoreHighestSubSumers(concepts,probeWord,ngWord):
    highestSims = nesteddict()
    senses_i = defaultdict(list)
    senses_j = defaultdict(list)

    childSenses = []
    #Find Highest Similarity
    highestSimSubSumer = (0,None,None,None)
    highestSimSubSumer = max(concepts,key=itemgetter(0))
    key = probeWord+','+ngWord
    for concept in concepts:
        if concept[1] == highestSimSubSumer[1]:
            highestSims[key]['sim_score'] = concept[0]
            #group noun word - sense
            senses_i[probeWord].append(concept[2])
            senses_j[ngWord].append(concept[3])


    highestSims[key]['senses'] = [senses_i,senses_j]


    return highestSims

#####################################################################################################################
#
#####################################################################################################################
def getPreferredSense(highestSims):
    preferredSense = None
    #Find best scoring word (sense) pairs
    wPairTopSims = defaultdict()
    subsumerSupport = []
    mifSense = defaultdict()
    for wPair, wSims in highestSims.items():
        scores_i = []
        s_i = wSims['senses'][0]
        for s in s_i:
            scores_i.extend(s_i[s])
            if s_i[s][0] in mifSense:
                if mifSense[s_i[s][0]] > wSims['sim_score']:
                    mifSense.update({s_i[s][0]:wSims['sim_score']})
            else:
                mifSense.update({s_i[s][0]:wSims['sim_score']})
        c_sense_i = Counter(scores_i)

        i = 0
        i_sense = None
        for sense in c_sense_i:
            v = c_sense_i[sense]
            if v > i:
                i = v
                i_sense = sense

        wPairTopSims.update({wPair:i_sense})

    #Filter out prefferred sense
    topSensesCount = defaultdict()
    for key, value in wPairTopSims.items():
        if value in topSensesCount:
            topSensesCount[value] += 1
        else:
            topSensesCount[value] = 1

    p = 0
    p_sense = None
    for sense in topSensesCount:
        v = topSensesCount[sense]
        if v > p:
            p = v
            p_sense = sense
    """elif v == p:
        if mifSense[sense] > mifSense[p_sense]:
            p = v
            p_sense = sense"""

    preferredSense = p_sense

    return preferredSense

#######################################################################################################################
#   Declare and return a nested Dictionary object
#######################################################################################################################
def nesteddict():
    return defaultdict(nesteddict)

#######################################################################################################################
# In-line process flow to call the main controller function
#######################################################################################################################
if __name__ == '__main__': main(sys.argv)