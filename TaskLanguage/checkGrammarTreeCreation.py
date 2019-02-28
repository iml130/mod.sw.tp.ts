from antlr4 import *
from TaskLexer import TaskLexer
from TaskParserListener import TaskParserListener
from TaskParser import TaskParser
from CreateTreeTaskParserVisitor import CreateTreeTaskParserVisitor
import sys

def checkTaskLanguage(_taskLanguage):
    try:
        lexer = TaskLexer(InputStream(_taskLanguage))
        stream = CommonTokenStream(lexer)
        parser = TaskParser(stream)
        tree = parser.program() 
        visitor = CreateTreeTaskParserVisitor()
        # printer = TaskParserListener()
        t = visitor.visit(tree)
 
    except Exception as expression:
        print expression
        return -1, expression.message
    return 0, "Success"


if __name__ == '__main__':
    checkTaskLanguage() 

