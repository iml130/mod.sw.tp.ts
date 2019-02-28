import Queue
import datetime 
import copy

from antlr4 import *
import networkx as nx

 
from TaskLanguage.checkGrammarTreeCreation import CreateTreeTaskParserVisitor
from TaskLanguage.TaskLexer import TaskLexer
from TaskLanguage.TaskParserListener import TaskParserListener
from TaskLanguage.TaskParser import TaskParser

from TaskSupervisor import graphy
from TaskSupervisor.taskManager import taskManager
from TaskSupervisor.task import Task


def createPrinter(_taskLanguage):
    try:
        lexer = TaskLexer(InputStream(_taskLanguage))
        stream = CommonTokenStream(lexer)
        parser = TaskParser(stream)
        tree = parser.program() 
        visitor = CreateTreeTaskParserVisitor() 
        t = visitor.visit(tree)
        for key,value in t.taskInfos.iteritems():
            print "NewTask: "
            print key
            print value.onDone
        return t
    except Exception as expression:
        print expression
        return -1, expression.message
    return 0, "Success"


# def createPrinter(taskLanguage):
#     try:
#         lexer = TaskLexer(InputStream(taskLanguage))
#         stream = CommonTokenStream(lexer)
#         parser = TaskParser(stream)
#         tree = parser.program() 
#         printer = PythonListener()
#         # printer = TaskParserListener()
#         walker = ParseTreeWalker()
#         walker.walk(printer, tree)
       
#         for key,value in printer.taskInfos.iteritems():
#             print "NewTask: "
#             print key
#             print value.childs
#         return printer
#     except Exception as expression:
#         print expression

def getSuccessors(digraph, node):
    child = None
    print list(digraph.nodes)
    for digraphnode in digraph.nodes:
        if(node.name == digraphnode.name):
            for x in digraph.successors(digraphnode):
                child = x
    
    
    return child



class taskScheduler():
    def __init__(self, name, taskLanguage):
        self.tasklanguage = taskLanguage
        printer = createPrinter(taskLanguage)
        G = graphy.createGraph(printer.taskInfos)
        graphy.printGraphInfo(G)
        graphy.displayGraph(G, True)
        self.taskGraph = G
        self.taskInfos = printer.taskInfos
        self.name = name
        self.runningTasks = []
        self.historyTasks = [] 
        self.taskManager = []
        self.queue = Queue.Queue()
    
    def addTask(self, task):
        if(task not in self.runningTasks):
            self.runningTasks.append(task)

    def start(self):
        for node in self.taskGraph.nodes:
            if(self.taskGraph.in_degree(node) == 0): # get all starting points from the graph
                tM = taskManager(node.name, self.queue)
                tM.addTask(node) # add the starting task
                successors = nx.dfs_successors(self.taskGraph, source = node).values()
                if(successors):
                    #self.taskGraph.nodes()
                    print successors
                    print type(successors)
                    for successor in successors: # create linked list with child nodes
                        tM.addTask(successor[0])
                    self.taskManager.append(tM)
                else:
                    # no successor, single task, reocurrent
                    
                    self.taskManager.append(tM)
                    
        for tm in self.taskManager:
            print str(datetime.datetime.now().time()) + ", Spawn_TM" + tm.name
            self.runningTasks.append(tm)
            tm.start()

        while (True):
            res = self.queue.get()
            print "FINISHED " + res
            for tR in self.runningTasks:
                if(tR.name == res):
                    tR.join()
                    self.runningTasks.remove(tR)

            for tM in self.taskManager:
                if(tM.name == res):
                    temp = taskManager(tM.name, self.queue)
                    temp.taskInfoList = tM.taskInfoList
                    
                    self.runningTasks.append(temp)
                    print "RESPAWN "+ res
                    temp.start()
            
    def status(self):
        # return states
        pass