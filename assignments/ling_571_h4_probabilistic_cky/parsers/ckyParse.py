##############################################################################################################################
# HW3 - Backpointer object used to track flow of recursive function calling to reconstruct parse from Nonterminal
#        constituent mapping
#   *Note: HW4 - Updated to include start symbol, and parseList
##############################################################################################################################
class CKYBackPointer():

    slide = ''
    parse = []
    finalRecognition = {}
    wordTags = {}
    wordCount = 0
    parseList = []
    treeMatrix = [[]]
    startSymbol = None
    isComplete = False
    wordFound = False
    recursionComplete = False

    def __init__(self,wordTags=None,parseList=None,wordCount=None,startSymbol=None,finalRecognition=None):
        self.isComplete = False
        self.slide = 'left'
        self.wordTags = wordTags
        self.parseList = parseList
        self.wordCount = wordCount
        self.startSymbol = startSymbol

        self.finalRecognition = finalRecognition
##End class CKYBackPointer()##################################################################################################

##############################################################################################################################
# HW4 - representation of a rule A -> B...C
#
# *TODO: READ_ME: Note borrowing of this function from example_cky.py provided in homework assignment details
#
###############################################################################################################################
class Rule(object):
    def __init__(self, head, symbols):
        self.head = head
        self.symbols = symbols
        self._key = head, symbols
    def __eq__(self, other):
        return self._key == other._key
    def __hash__(self):
        return hash(self._key)

## End class Rule(object)########################################################################################################
class PCFGRule(Rule):

    headProbability = float()

    def setProbability(self,p):
        self.probability = p

    def getProbability(self):
        return property





#################################################################################################################################
# HW4 - build a grammar from a string of lines like "X -> YZ | b"
#
# *TODO: READ_ME: Note borrowing of this function from example_cky.py provided in homework assignment details
#
#################################################################################################################################
def get_grammar(string):
    grammar = set()
    for line in string.splitlines():
        head, symbols_str = line.split(' -> ')
        for symbols_str in symbols_str.split(' | '):
            symbols = tuple(symbols_str.split())
            grammar.add(Rule(head, symbols))
    return grammar
