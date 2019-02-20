import Queue
import datetime 
import copy

from antlr4 import *
import networkx as nx


from TaskLanguage.checkGrammar import PythonListener
from TaskLanguage.TaskLexer import TaskLexer
from TaskLanguage.TaskParserListener import TaskParserListener
from TaskLanguage.TaskParser import TaskParser

from TaskSupervisor import graphy
from TaskSupervisor.taskManager import taskManager
from TaskSupervisor.task import Task
def createPrinter(taskLanguage):
    try:
        lexer = TaskLexer(InputStream(taskLanguage))
        stream = CommonTokenStream(lexer)
        parser = TaskParser(stream)
        tree = parser.program() 
        printer = PythonListener()
        # printer = TaskParserListener()
        walker = ParseTreeWalker()
        walker.walk(printer, tree)
       
        for key,value in printer.taskInfoList.iteritems():
            print "NewTask: "
            print key
            print value.childs
        return printer
    except Exception as expression:
        print expression

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
        G = graphy.createGraph(printer.taskInfoList)
        graphy.printGraphInfo(G)
        graphy.displayGraph(G, True)
        self.taskGraph = G
        self.taskInfoList = printer.taskInfoList
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
            if(self.taskGraph.in_degree(node) == 0):
                successors = nx.dfs_successors(self.taskGraph, source = node).values()
                if(successors):
                    self.taskGraph.nodes()
                    tM = taskManager(node.name, self.queue)
                    tM.addTask(node)
                    print successors
                    print type(successors)
                    for successor in successors:
                        tM.addTask(successor[0])
                    self.taskManager.append(tM)
                else:
                    # no successor, single task, reocurrent
                    tM = taskManager(node.name, self.queue)
                    tM.addTask(node)
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
                    temp.taskList = tM.taskList
                    
                    self.runningTasks.append(temp)
                    print "RESPAWN "+ res
                    temp.start()
            
            
            
        
#     def start(self):
#         listOfStartTask = graphy.getStartTask(self.taskGraph)
# #        for task in listOfStartTask:
#         for x in listOfStartTask:
#             t = Task(x.name)
#             print "Start now:" + t.name
#             print "type: " + str(type(t))
#             self.runningTasks.append(t)
#             t.start()
#         while True:    
#             for i in self.runningTasks:
#                 print "wait for "+ i.name
#                 i.join()
#                 child = getSuccessors(self.taskGraph, i)
#                 self.runningTasks.remove(i)
#                 if( child == None): 
#                     print "no successors, start the ROOT task"
#                 else:
#                     print type(child)
#                     t = Task(child.name)
#                     self.runningTasks.append(t)
#                     t.start()
#                     print "Start now: " + child.name
#                     print "type: " + str(type(x))

#             print "reached"
#         pass


    def status(self):
        # return states
        pass