import nltk, io, re

##############################################################################################
#   Open a file for Output - write only!!!
#   w - Opens a file for writing only. Overwrites the file if the file exists.
#       If the file does not exist, creates a new file for writing.
##############################################################################################
def outputListToFile(content,fileName,path):
    print("OutPutToFile: Entered, FileName[%s] Path[%s]" %(fileName,path))

    try:
        print("Content to write to file [ %s ]"%str(content))
        fileName = path+fileName
        file = open(fileName,'w')

        for e in content:
            #file.writelines(str(e))
            file.write(str(e)+"\n")

        file.close()
    except Exception as e:
        print("*****ERROR*****: outputToFile, Caught Exception %s"%str(e))

#################################################################################################

##############################################################################################
#   Open a file for Output - write only!!!
#   w - Opens a file for writing only. Overwrites the file if the file exists.
#       If the file does not exist, creates a new file for writing.
##############################################################################################
def outputGrammarToFile(content,fileName,path):
    print("OutPutToFile: Entered, FileName[%s] Path[%s]" %(fileName,path))

    try:
        print("Content to write to file [ %s ]"%str(content))
        fileName = path+fileName
        file = open(fileName,'w')

        file.write(str(content))

        file.close()
    except Exception as e:
        print("*****ERROR*****: outputToFile, Caught Exception %s"%str(e))

#################################################################################################

#############################################################################################
#   Open a grammar file
#############################################################################################
def openGrammarFile(fileName):
    print("Openning file [%s]" %fileName)
    try:
        grammar = nltk.data.load('./grammars/'+fileName)
    except Exception as e:
        print("*****ERROR*****:Caught Exception %s"%str(e))
    return grammar
##############################################################################################


####################################################################################################
# File IO - Opens a file based on name passed into function
####################################################################################################
def openSentencesClean(self,fileName):
    print("\nEntered openSentencesClean: Sentence file name to open [%s]" %fileName)
    try:
        fileName = './sentences/'+fileName
        fsentences = io.open(fileName,'r')
        sentences = fsentences.readlines()
        sentencesList = []

        for sentence in sentences:
            #sentence = sentence.replace('\n','')
            sentence = re.sub(r"\,|\?|\.|\n","",sentence)
            print(sentence)
            sentencesList.append(sentence)

        fsentences.close()
        print("Exiting openSentencesClean: sentence list[ %s ]"%str(sentencesList))
    except Exception as e:
        print("******ERROR*****: openSentencesClean, Caught Exception: %s"%str(e))

    return sentencesList
