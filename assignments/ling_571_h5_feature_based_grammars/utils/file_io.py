import nltk
from utils.exceptions import ZeroParseException
#############################################################################################
#   HW5 - Load a grammar
#   :param path: -Path location to file location
#   :param fileName: - Name of the file to open
#############################################################################################
def loadGrammar(path,fileName):
    print("utils.io.file_io.loadGrammar: file [%s], path[%s]" %(fileName,path))
    grammar = None

    try:

        grammar = nltk.data.load(path+fileName)

    except Exception as e:
        print("*****ERROR*****:utils.io.file_io.loadGrammar: Caught Exception %s"%str(e))

    return grammar

#############################################################################################
#   HW5 - Output parse to a file
#   :param parse: -Sentence parse to be printed to file
#   :param path: -Path location to file location
#   :param fileName: - Name of the file to open
#############################################################################################
def parseOutput(parse,fileName,path=None):
    print("utils.io.file_io.parseOutput: fileName [%s], path[%s], parse[%s]" %(fileName,path,parse))

    try:
        fileName = path+fileName
        file = open(fileName,'a')

        try:
            if len(parse) > 0:
                singleLineOutput = nltk.Tree._pformat_flat(parse)
                file.write(str(singleLineOutput)+'\n')
            else:
                raise ZeroParseException("Parse length is Zero; parse[%s]"%parse)

        except ZeroParseException as zpe:
            print("*****INFO*****: utils.io.file_io.parseOutput: Caught ZeroParseException"%str(zpe))
            parse = ' '
            file.write(str(parse)+'\n')

        file.flush()
        file.close()
    except IOError as io:
        print("*****ERROR*****:utils.io.file_io.parseOutput: Caught Exception %s"%str(io))
        raise IOError("Caught error in utils.io.file_io.openSentences: propagating exception up; %s"%str(io))
#############################################################################################
#   HW5 - Open a Sentence File
#   :param path: -Path location to file location
#   :param fileName: - Name of the file to open
#############################################################################################
def openSentences(path,fileName):
    print("utils.io.file_io.openSentences: fileName [%s], path[%s]" %(fileName,path))
    sentencesList = []

    try:
        fsentences = open(path+fileName,'r')
        sentences = fsentences.readlines()

        for sentence in sentences:
            sentence = sentence.replace('\n','')
            sentencesList.append(sentence)

        fsentences.close()

    except IOError as io:
        print("*****ERROR*****:utils.io.file_io.openSentences: Caught Exception %s"%str(io))
        raise IOError("Caught error in utils.io.file_io.openSentences: propagating exception up; %s"%str(io))
    return sentencesList

