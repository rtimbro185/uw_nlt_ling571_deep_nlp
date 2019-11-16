import nltk, io, re, pprint


##############################################################################################
#   Open a file for Output -
#   w - Opens a file for appending. Overwrites the file if the file exists.
#       If the file does not exist, creates a new file for writing.
##############################################################################################
def outputListToFile(content,fileName,path):
    print("OutPutToFile: Entered, FileName[%s] Path[%s]" %(fileName,path))

    try:
        print("Content to write to file [ %s ]"%str(content))
        fileName = path+fileName
        file = open(fileName,'a') #

        for e in content:
            #file.writelines(str(e))
            file.write(str(e)+"\n")

        file.close()
    except Exception as e:
        print("*****ERROR*****: outputToFile, Caught Exception %s"%str(e))

#################################################################################################

##############################################################################################
#
#       If the file does not exist, creates a new file for writing.
##############################################################################################
def outputToFile(content,fileName,path):
    print("OutPutToFile: Entered, FileName[%s] Path[%s]" %(fileName,path))

    try:
        print("Content to write to file:\n [ %s ]"%str(content))
        fileName = path+fileName
        file = open(fileName,'a')
        #file.write("\n")
        for c in content:
            file.write(str(c)+'\n')

        file.flush()
        file.close()
    except Exception as e:
        print("*****ERROR*****: outputToFile, Caught Exception %s"%str(e))

#################################################################################################

####################################################################################################
# File IO - Opens a file based on name passed into function
####################################################################################################
def openSentences(fileName):
    print("\nEntered openSentencesClean: Sentence file name to open [%s]" %fileName)
    try:
        fileName = './sentences/'+fileName
        fsentences = open(fileName,'r')
        sentences = fsentences.readlines()
        #sentences = fsentences.read()
        sentencesList = []

        for sentence in sentences:
            sentence = sentence.replace('\n','')
            #sentence = re.sub(r"\,|\?|\.|\n","",sentence)
            #print(sentence)
            sentencesList.append(sentence)

        fsentences.close()
        print("Exiting openSentences: file name [%s]" %fileName)
    except Exception as e:
        print("******ERROR*****: openSentencesClean, Caught Exception: %s"%str(e))

    return sentencesList

#######################################################################################################
#   print dictionary to file
#######################################################################################################
def pPrintPCFG(dict,fileName,path):
    print("\nEntered pPrintPCFG: file name to open [%s] for writing" %fileName)

    try:
        fileName = path+fileName
        file = open(fileName,'a')
        keys = dict.keys()
        for key in keys:
            tempStr = [str(key),' ', '[', str(dict[key]),']','\n']
            for c in tempStr:
                file.write(c)

        file.close()
    except IOError as io:
        print("pPrintPCFG: Caught an IOError; %s"%str(io))
###########################################################################################################

###########################################################################################################
#   HW-4 print induced pcfg to file
###########################################################################################################
def pPrintPCFGToFile(pcfg,fileName,path):
    print("\nEntered pPrintPCFG: file name to open [%s] for writing" %fileName)

    try:
        fileName = path+fileName
        file = open(fileName, 'w')

        file.write('%start TOP\n')
        for prod in pcfg.productions():
            file.write(str(prod)+'\n')

        #print(pcfg,file=file)

        file.flush()
        file.close()
    except IOError as io:
        print("pPrintPCFG: Caught an IOError; %s"%str(io))


#############################################################################################
#  HW4 - Open pcfg grammar file
#############################################################################################
def loadPCFGGrammarFromFile(path,fileName,start=None):
    print("openGrammarFile: file [%s], path[%s]" %(fileName,path))
    pcfg = None

    #try:

    grammar = nltk.data.load(path+fileName)
        #pcfg = nltk.grammar.PCFG(grammar.start(),grammar.productions())

    #except Exception as e:
        #print("*****ERROR*****:Caught Exception %s"%str(e))

    return grammar
##############################################################################################
##############################################################################################
#   Open a file for Output - write only!!!
#   w - Opens a file for writing only. Overwrites the file if the file exists.
#       If the file does not exist, creates a new file for writing.
##############################################################################################
from nltk.tree import Tree
def outputTreeToFile(content,fileName,path):
    print("OutPutToFile: Entered, FileName[%s] Path[%s]" %(fileName,path))

    try:
        print("Content to write to file:\n [ %s ]"%str(content))
        fileName = path+fileName
        file = open(fileName,'a')
        #file.write("\n")
        for tree in content:
            print(tree,file=file,flush=True)
            #file.write(str(c)+'\n')

        #file.flush()
        file.close()
    except Exception as e:
        print("*****ERROR*****: outputToFile, Caught Exception %s"%str(e))

#################################################################################################
