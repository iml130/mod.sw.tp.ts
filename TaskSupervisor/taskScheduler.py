import Queue
import datetime 
import copy
import logging

from antlr4 import *
import networkx as nx

 
from TaskLanguage.checkGrammarTreeCreation import CreateTreeTaskParserVisitor
from TaskLanguage.TaskLexer import TaskLexer
from TaskLanguage.TaskParserListener import TaskParserListener
from TaskLanguage.TaskParser import TaskParser

from TaskSupervisor import graphy
from TaskSupervisor.taskManager import taskManager
from TaskSupervisor.task import Task

logger = logging.getLogger(__name__)

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

# def getSuccessors(digraph, node):
#     child = None
#     print list(digraph.nodes)
#     for digraphnode in digraph.nodes:
#         if(node.name == digraphnode.name):
#             for x in digraph.successors(digraphnode):
#                 child = x
    
#     return child



class taskScheduler():
    def __init__(self, name, taskLanguage):
        logger.info("taskSchedular init")
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
        logger.info("taskSchedular init_end")
    
    def addTask(self, task):
        logger.info("taskSchedular addTask" + task.name)
        if(task not in self.runningTasks):
            self.runningTasks.append(task)        
        logger.info("taskSchedular addTask_end")

    def start(self):
        logger.info("taskSchedular start")
        for node in self.taskGraph.nodes:
            if(self.taskGraph.in_degree(node) == 0): # get all starting points from the graph
                tM = taskManager(node.name, self.queue)
                tM.addTask(node) # add the starting task
                successors = nx.dfs_successors(self.taskGraph, source = node).values()
                if(successors):
                    #self.taskGraph.nodes() 
                    for successor in successors: # create linked list with child nodes
                        tM.addTask(successor[0])
                    self.taskManager.append(tM)
                else:
                    # no successor, single task, reocurrent
                    
                    self.taskManager.append(tM)
                    
        for tm in self.taskManager:
            logger.info("taskSchedular, taskManager spawn: " + tm.taskManagerName)
            self.runningTasks.append(tm)
            tm.publishEntity()
            tm.start()

        # respawn finished taskManager 
        while (True):
            res = self.queue.get()
            logger.info("taskSchedular, TaskManager finished: " + res)
            for tR in self.runningTasks:
                if(tR.taskManagerName == res):
                    tR.join()
                    #tR.deleteEntity()
                    self.runningTasks.remove(tR)
                    tR = None
                    
            for tM in self.taskManager:
                if(tM.taskManagerName == res):
                    temp = taskManager(tM.taskManagerName, self.queue)
                    temp._taskInfoList = tM._taskInfoList
                    
                    self.runningTasks.append(temp)
                    logger.info("taskSchedular, taskManager respawn: " + res)
                    temp.publishEntity()
                    temp.start()
        logger.info("taskSchedular start_end")
            
    def status(self):
        # return states
        pass