# Generated from TaskParser.g4 by ANTLR 4.7.2
from antlr4 import *

# This class defines a complete generic visitor for a parse tree produced by TaskParser.

class TaskParserVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by TaskParser#program.
    def visitProgram(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TaskParser#template.
    def visitTemplate(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TaskParser#innerTemplate.
    def visitInnerTemplate(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TaskParser#instance.
    def visitInstance(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TaskParser#innerInstance.
    def visitInnerInstance(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TaskParser#transportOrderStep.
    def visitTransportOrderStep(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TaskParser#innerTransportOrderStep.
    def visitInnerTransportOrderStep(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TaskParser#task.
    def visitTask(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TaskParser#innerTask.
    def visitInnerTask(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TaskParser#transportOrder.
    def visitTransportOrder(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TaskParser#expression.
    def visitExpression(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TaskParser#binOperation.
    def visitBinOperation(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TaskParser#unOperation.
    def visitUnOperation(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TaskParser#con.
    def visitCon(self, ctx):
        return self.visitChildren(ctx)


