import sys


from antlr4 import *
from antlr4.error.ErrorListener import ErrorListener

from TaskLexer import TaskLexer
from TaskParserListener import TaskParserListener
from TaskParser import TaskParser
from CreateTreeTaskParserVisitor import CreateTreeTaskParserVisitor

import taskValidator

  
class ThrowErrorListener(ErrorListener):
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        raise e

    def reportAmbiguity(self, recognizer, dfa, startIndex, stopIndex, exact, ambigAlts, configs):
        raise Exception("Task-Language could not be parsed")

    def reportAttemptingFullContext(self, recognizer, dfa, startIndex, stopIndex, conflictingAlts, configs):
        raise Exception("Task-Language could not be parsed")

    def reportContextSensitivity(self, recognizer, dfa, startIndex, stopIndex, prediction, configs):
        raise Exception("Task-Language could not be parsed")


def checkTaskLanguage(_taskLanguage):
    try:
        lexer = TaskLexer(InputStream(_taskLanguage))
        lexer._listeners.append(ThrowErrorListener())
        stream = CommonTokenStream(lexer)
        parser = TaskParser(stream)
        tree = parser.program() 
        visitor = CreateTreeTaskParserVisitor()
        # printer = TaskParserListener()
        t = visitor.visit(tree)
        
        retVal = taskValidator.isValid(t)


    except Exception as expression:
        print expression
        return -1, str(expression.message).replace("'","-")
    return 0, "Success"


if __name__ == '__main__':
    checkTaskLanguage() 

