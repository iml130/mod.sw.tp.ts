# Generated from TaskParser.g4 by ANTLR 4.7.2
# encoding: utf-8
from __future__ import print_function
from antlr4 import *
from io import StringIO
import sys


def serializedATN():
    with StringIO() as buf:
        buf.write(u"\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\3")
        buf.write(u"%Z\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7\4")
        buf.write(u"\b\t\b\4\t\t\t\3\2\3\2\3\2\7\2\26\n\2\f\2\16\2\31\13")
        buf.write(u"\2\3\3\3\3\3\3\3\3\3\3\3\4\3\4\3\4\6\4#\n\4\r\4\16\4")
        buf.write(u"$\3\5\3\5\3\5\3\5\3\5\3\6\3\6\3\6\3\6\3\6\6\6\61\n\6")
        buf.write(u"\r\6\16\6\62\3\7\3\7\3\7\3\7\3\7\3\b\3\b\3\b\3\b\3\b")
        buf.write(u"\3\b\3\b\3\b\3\b\6\bC\n\b\r\b\16\bD\3\t\3\t\3\t\3\t\3")
        buf.write(u"\t\3\t\3\t\3\t\7\tO\n\t\f\t\16\tR\13\t\3\t\3\t\3\t\3")
        buf.write(u"\t\3\t\3\t\3\t\2\2\n\2\4\6\b\n\f\16\20\2\2\2Z\2\27\3")
        buf.write(u"\2\2\2\4\32\3\2\2\2\6\"\3\2\2\2\b&\3\2\2\2\n\60\3\2\2")
        buf.write(u"\2\f\64\3\2\2\2\16B\3\2\2\2\20F\3\2\2\2\22\26\5\4\3\2")
        buf.write(u"\23\26\5\b\5\2\24\26\5\f\7\2\25\22\3\2\2\2\25\23\3\2")
        buf.write(u"\2\2\25\24\3\2\2\2\26\31\3\2\2\2\27\25\3\2\2\2\27\30")
        buf.write(u"\3\2\2\2\30\3\3\2\2\2\31\27\3\2\2\2\32\33\7\4\2\2\33")
        buf.write(u"\34\7\r\2\2\34\35\5\6\4\2\35\36\7\13\2\2\36\5\3\2\2\2")
        buf.write(u"\37 \7\16\2\2 !\7\f\2\2!#\7\r\2\2\"\37\3\2\2\2#$\3\2")
        buf.write(u"\2\2$\"\3\2\2\2$%\3\2\2\2%\7\3\2\2\2&\'\7\6\2\2\'(\7")
        buf.write(u"\24\2\2()\5\n\6\2)*\7\22\2\2*\t\3\2\2\2+,\7\25\2\2,-")
        buf.write(u"\7\26\2\2-.\7\23\2\2./\7\27\2\2/\61\7\24\2\2\60+\3\2")
        buf.write(u"\2\2\61\62\3\2\2\2\62\60\3\2\2\2\62\63\3\2\2\2\63\13")
        buf.write(u"\3\2\2\2\64\65\7\5\2\2\65\66\7\34\2\2\66\67\5\16\b\2")
        buf.write(u"\678\7\33\2\28\r\3\2\2\29C\5\20\t\2:;\7#\2\2;<\7 \2\2")
        buf.write(u"<=\7$\2\2=C\7\34\2\2>?\7#\2\2?@\7!\2\2@A\7%\2\2AC\7\34")
        buf.write(u"\2\2B9\3\2\2\2B:\3\2\2\2B>\3\2\2\2CD\3\2\2\2DB\3\2\2")
        buf.write(u"\2DE\3\2\2\2E\17\3\2\2\2FG\7#\2\2GH\7\35\2\2HI\7\34\2")
        buf.write(u"\2IJ\7#\2\2JK\7\36\2\2KP\7$\2\2LM\7\"\2\2MO\7$\2\2NL")
        buf.write(u"\3\2\2\2OR\3\2\2\2PN\3\2\2\2PQ\3\2\2\2QS\3\2\2\2RP\3")
        buf.write(u"\2\2\2ST\7\34\2\2TU\7#\2\2UV\7\37\2\2VW\7$\2\2WX\7\34")
        buf.write(u"\2\2X\21\3\2\2\2\t\25\27$\62BDP")
        return buf.getvalue()


class TaskParser ( Parser ):

    grammarFileName = "TaskParser.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [  ]

    symbolicNames = [ u"<INVALID>", u"CommentInProgram", u"TemplateStart", 
                      u"TaskStart", u"InstanceStart", u"WS", u"CommentInTemplate", 
                      u"CommentLineInTemplate", u"EmptyLineInTemplate", 
                      u"EndInTemplate", u"AttributeInTemplate", u"NLInTemplate", 
                      u"IndentationInTemplate", u"CommentInInstance", u"CommentLineInInstance", 
                      u"EmptyLineInInstance", u"EndInInstance", u"Equal", 
                      u"NLInInstance", u"IndentationInInstance", u"AttributeInInstance", 
                      u"ValueInInstance", u"CommentInTask", u"CommentLineInTask", 
                      u"EmptyLineInTask", u"EndInTask", u"NLInTask", u"Transport", 
                      u"From", u"To", u"TriggeredBy", u"OnDone", u"Comma", 
                      u"IndentationInTask", u"NewInstance", u"NewTask" ]

    RULE_program = 0
    RULE_template = 1
    RULE_innerTemplate = 2
    RULE_instance = 3
    RULE_innerInstance = 4
    RULE_task = 5
    RULE_innerTask = 6
    RULE_transportOrder = 7

    ruleNames =  [ u"program", u"template", u"innerTemplate", u"instance", 
                   u"innerInstance", u"task", u"innerTask", u"transportOrder" ]

    EOF = Token.EOF
    CommentInProgram=1
    TemplateStart=2
    TaskStart=3
    InstanceStart=4
    WS=5
    CommentInTemplate=6
    CommentLineInTemplate=7
    EmptyLineInTemplate=8
    EndInTemplate=9
    AttributeInTemplate=10
    NLInTemplate=11
    IndentationInTemplate=12
    CommentInInstance=13
    CommentLineInInstance=14
    EmptyLineInInstance=15
    EndInInstance=16
    Equal=17
    NLInInstance=18
    IndentationInInstance=19
    AttributeInInstance=20
    ValueInInstance=21
    CommentInTask=22
    CommentLineInTask=23
    EmptyLineInTask=24
    EndInTask=25
    NLInTask=26
    Transport=27
    From=28
    To=29
    TriggeredBy=30
    OnDone=31
    Comma=32
    IndentationInTask=33
    NewInstance=34
    NewTask=35

    def __init__(self, input, output=sys.stdout):
        super(TaskParser, self).__init__(input, output=output)
        self.checkVersion("4.7.2")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class ProgramContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(TaskParser.ProgramContext, self).__init__(parent, invokingState)
            self.parser = parser

        def template(self, i=None):
            if i is None:
                return self.getTypedRuleContexts(TaskParser.TemplateContext)
            else:
                return self.getTypedRuleContext(TaskParser.TemplateContext,i)


        def instance(self, i=None):
            if i is None:
                return self.getTypedRuleContexts(TaskParser.InstanceContext)
            else:
                return self.getTypedRuleContext(TaskParser.InstanceContext,i)


        def task(self, i=None):
            if i is None:
                return self.getTypedRuleContexts(TaskParser.TaskContext)
            else:
                return self.getTypedRuleContext(TaskParser.TaskContext,i)


        def getRuleIndex(self):
            return TaskParser.RULE_program

        def enterRule(self, listener):
            if hasattr(listener, "enterProgram"):
                listener.enterProgram(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitProgram"):
                listener.exitProgram(self)




    def program(self):

        localctx = TaskParser.ProgramContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_program)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 21
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << TaskParser.TemplateStart) | (1 << TaskParser.TaskStart) | (1 << TaskParser.InstanceStart))) != 0):
                self.state = 19
                self._errHandler.sync(self)
                token = self._input.LA(1)
                if token in [TaskParser.TemplateStart]:
                    self.state = 16
                    self.template()
                    pass
                elif token in [TaskParser.InstanceStart]:
                    self.state = 17
                    self.instance()
                    pass
                elif token in [TaskParser.TaskStart]:
                    self.state = 18
                    self.task()
                    pass
                else:
                    raise NoViableAltException(self)

                self.state = 23
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TemplateContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(TaskParser.TemplateContext, self).__init__(parent, invokingState)
            self.parser = parser

        def TemplateStart(self):
            return self.getToken(TaskParser.TemplateStart, 0)

        def NLInTemplate(self):
            return self.getToken(TaskParser.NLInTemplate, 0)

        def innerTemplate(self):
            return self.getTypedRuleContext(TaskParser.InnerTemplateContext,0)


        def EndInTemplate(self):
            return self.getToken(TaskParser.EndInTemplate, 0)

        def getRuleIndex(self):
            return TaskParser.RULE_template

        def enterRule(self, listener):
            if hasattr(listener, "enterTemplate"):
                listener.enterTemplate(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitTemplate"):
                listener.exitTemplate(self)




    def template(self):

        localctx = TaskParser.TemplateContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_template)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 24
            self.match(TaskParser.TemplateStart)
            self.state = 25
            self.match(TaskParser.NLInTemplate)
            self.state = 26
            self.innerTemplate()
            self.state = 27
            self.match(TaskParser.EndInTemplate)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class InnerTemplateContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(TaskParser.InnerTemplateContext, self).__init__(parent, invokingState)
            self.parser = parser

        def IndentationInTemplate(self, i=None):
            if i is None:
                return self.getTokens(TaskParser.IndentationInTemplate)
            else:
                return self.getToken(TaskParser.IndentationInTemplate, i)

        def AttributeInTemplate(self, i=None):
            if i is None:
                return self.getTokens(TaskParser.AttributeInTemplate)
            else:
                return self.getToken(TaskParser.AttributeInTemplate, i)

        def NLInTemplate(self, i=None):
            if i is None:
                return self.getTokens(TaskParser.NLInTemplate)
            else:
                return self.getToken(TaskParser.NLInTemplate, i)

        def getRuleIndex(self):
            return TaskParser.RULE_innerTemplate

        def enterRule(self, listener):
            if hasattr(listener, "enterInnerTemplate"):
                listener.enterInnerTemplate(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitInnerTemplate"):
                listener.exitInnerTemplate(self)




    def innerTemplate(self):

        localctx = TaskParser.InnerTemplateContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_innerTemplate)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 32 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 29
                self.match(TaskParser.IndentationInTemplate)
                self.state = 30
                self.match(TaskParser.AttributeInTemplate)
                self.state = 31
                self.match(TaskParser.NLInTemplate)
                self.state = 34 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==TaskParser.IndentationInTemplate):
                    break

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class InstanceContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(TaskParser.InstanceContext, self).__init__(parent, invokingState)
            self.parser = parser

        def InstanceStart(self):
            return self.getToken(TaskParser.InstanceStart, 0)

        def NLInInstance(self):
            return self.getToken(TaskParser.NLInInstance, 0)

        def innerInstance(self):
            return self.getTypedRuleContext(TaskParser.InnerInstanceContext,0)


        def EndInInstance(self):
            return self.getToken(TaskParser.EndInInstance, 0)

        def getRuleIndex(self):
            return TaskParser.RULE_instance

        def enterRule(self, listener):
            if hasattr(listener, "enterInstance"):
                listener.enterInstance(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitInstance"):
                listener.exitInstance(self)




    def instance(self):

        localctx = TaskParser.InstanceContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_instance)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 36
            self.match(TaskParser.InstanceStart)
            self.state = 37
            self.match(TaskParser.NLInInstance)
            self.state = 38
            self.innerInstance()
            self.state = 39
            self.match(TaskParser.EndInInstance)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class InnerInstanceContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(TaskParser.InnerInstanceContext, self).__init__(parent, invokingState)
            self.parser = parser

        def IndentationInInstance(self, i=None):
            if i is None:
                return self.getTokens(TaskParser.IndentationInInstance)
            else:
                return self.getToken(TaskParser.IndentationInInstance, i)

        def AttributeInInstance(self, i=None):
            if i is None:
                return self.getTokens(TaskParser.AttributeInInstance)
            else:
                return self.getToken(TaskParser.AttributeInInstance, i)

        def Equal(self, i=None):
            if i is None:
                return self.getTokens(TaskParser.Equal)
            else:
                return self.getToken(TaskParser.Equal, i)

        def ValueInInstance(self, i=None):
            if i is None:
                return self.getTokens(TaskParser.ValueInInstance)
            else:
                return self.getToken(TaskParser.ValueInInstance, i)

        def NLInInstance(self, i=None):
            if i is None:
                return self.getTokens(TaskParser.NLInInstance)
            else:
                return self.getToken(TaskParser.NLInInstance, i)

        def getRuleIndex(self):
            return TaskParser.RULE_innerInstance

        def enterRule(self, listener):
            if hasattr(listener, "enterInnerInstance"):
                listener.enterInnerInstance(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitInnerInstance"):
                listener.exitInnerInstance(self)




    def innerInstance(self):

        localctx = TaskParser.InnerInstanceContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_innerInstance)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 46 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 41
                self.match(TaskParser.IndentationInInstance)
                self.state = 42
                self.match(TaskParser.AttributeInInstance)
                self.state = 43
                self.match(TaskParser.Equal)
                self.state = 44
                self.match(TaskParser.ValueInInstance)
                self.state = 45
                self.match(TaskParser.NLInInstance)
                self.state = 48 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==TaskParser.IndentationInInstance):
                    break

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TaskContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(TaskParser.TaskContext, self).__init__(parent, invokingState)
            self.parser = parser

        def TaskStart(self):
            return self.getToken(TaskParser.TaskStart, 0)

        def NLInTask(self):
            return self.getToken(TaskParser.NLInTask, 0)

        def innerTask(self):
            return self.getTypedRuleContext(TaskParser.InnerTaskContext,0)


        def EndInTask(self):
            return self.getToken(TaskParser.EndInTask, 0)

        def getRuleIndex(self):
            return TaskParser.RULE_task

        def enterRule(self, listener):
            if hasattr(listener, "enterTask"):
                listener.enterTask(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitTask"):
                listener.exitTask(self)




    def task(self):

        localctx = TaskParser.TaskContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_task)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 50
            self.match(TaskParser.TaskStart)
            self.state = 51
            self.match(TaskParser.NLInTask)
            self.state = 52
            self.innerTask()
            self.state = 53
            self.match(TaskParser.EndInTask)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class InnerTaskContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(TaskParser.InnerTaskContext, self).__init__(parent, invokingState)
            self.parser = parser

        def transportOrder(self, i=None):
            if i is None:
                return self.getTypedRuleContexts(TaskParser.TransportOrderContext)
            else:
                return self.getTypedRuleContext(TaskParser.TransportOrderContext,i)


        def IndentationInTask(self, i=None):
            if i is None:
                return self.getTokens(TaskParser.IndentationInTask)
            else:
                return self.getToken(TaskParser.IndentationInTask, i)

        def TriggeredBy(self, i=None):
            if i is None:
                return self.getTokens(TaskParser.TriggeredBy)
            else:
                return self.getToken(TaskParser.TriggeredBy, i)

        def NewInstance(self, i=None):
            if i is None:
                return self.getTokens(TaskParser.NewInstance)
            else:
                return self.getToken(TaskParser.NewInstance, i)

        def NLInTask(self, i=None):
            if i is None:
                return self.getTokens(TaskParser.NLInTask)
            else:
                return self.getToken(TaskParser.NLInTask, i)

        def OnDone(self, i=None):
            if i is None:
                return self.getTokens(TaskParser.OnDone)
            else:
                return self.getToken(TaskParser.OnDone, i)

        def NewTask(self, i=None):
            if i is None:
                return self.getTokens(TaskParser.NewTask)
            else:
                return self.getToken(TaskParser.NewTask, i)

        def getRuleIndex(self):
            return TaskParser.RULE_innerTask

        def enterRule(self, listener):
            if hasattr(listener, "enterInnerTask"):
                listener.enterInnerTask(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitInnerTask"):
                listener.exitInnerTask(self)




    def innerTask(self):

        localctx = TaskParser.InnerTaskContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_innerTask)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 64 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 64
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,4,self._ctx)
                if la_ == 1:
                    self.state = 55
                    self.transportOrder()
                    pass

                elif la_ == 2:
                    self.state = 56
                    self.match(TaskParser.IndentationInTask)
                    self.state = 57
                    self.match(TaskParser.TriggeredBy)
                    self.state = 58
                    self.match(TaskParser.NewInstance)
                    self.state = 59
                    self.match(TaskParser.NLInTask)
                    pass

                elif la_ == 3:
                    self.state = 60
                    self.match(TaskParser.IndentationInTask)
                    self.state = 61
                    self.match(TaskParser.OnDone)
                    self.state = 62
                    self.match(TaskParser.NewTask)
                    self.state = 63
                    self.match(TaskParser.NLInTask)
                    pass


                self.state = 66 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==TaskParser.IndentationInTask):
                    break

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TransportOrderContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(TaskParser.TransportOrderContext, self).__init__(parent, invokingState)
            self.parser = parser

        def IndentationInTask(self, i=None):
            if i is None:
                return self.getTokens(TaskParser.IndentationInTask)
            else:
                return self.getToken(TaskParser.IndentationInTask, i)

        def Transport(self):
            return self.getToken(TaskParser.Transport, 0)

        def NLInTask(self, i=None):
            if i is None:
                return self.getTokens(TaskParser.NLInTask)
            else:
                return self.getToken(TaskParser.NLInTask, i)

        def From(self):
            return self.getToken(TaskParser.From, 0)

        def NewInstance(self, i=None):
            if i is None:
                return self.getTokens(TaskParser.NewInstance)
            else:
                return self.getToken(TaskParser.NewInstance, i)

        def To(self):
            return self.getToken(TaskParser.To, 0)

        def Comma(self, i=None):
            if i is None:
                return self.getTokens(TaskParser.Comma)
            else:
                return self.getToken(TaskParser.Comma, i)

        def getRuleIndex(self):
            return TaskParser.RULE_transportOrder

        def enterRule(self, listener):
            if hasattr(listener, "enterTransportOrder"):
                listener.enterTransportOrder(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitTransportOrder"):
                listener.exitTransportOrder(self)




    def transportOrder(self):

        localctx = TaskParser.TransportOrderContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_transportOrder)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 68
            self.match(TaskParser.IndentationInTask)
            self.state = 69
            self.match(TaskParser.Transport)
            self.state = 70
            self.match(TaskParser.NLInTask)
            self.state = 71
            self.match(TaskParser.IndentationInTask)
            self.state = 72
            self.match(TaskParser.From)
            self.state = 73
            self.match(TaskParser.NewInstance)
            self.state = 78
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==TaskParser.Comma:
                self.state = 74
                self.match(TaskParser.Comma)
                self.state = 75
                self.match(TaskParser.NewInstance)
                self.state = 80
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 81
            self.match(TaskParser.NLInTask)
            self.state = 82
            self.match(TaskParser.IndentationInTask)
            self.state = 83
            self.match(TaskParser.To)
            self.state = 84
            self.match(TaskParser.NewInstance)
            self.state = 85
            self.match(TaskParser.NLInTask)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





