__author__ = "Peter Detzner"  
__version__ = "0.0.1a"
__status__ = "Developement"

import Queue
import datetime 
import copy
import logging
import threading

from antlr4 import *
import networkx as nx

 
from TaskLanguage.checkGrammarTreeCreation import CreateTreeTaskParserVisitor
from TaskLanguage.TaskLexer import TaskLexer
from TaskLanguage.TaskParserListener import TaskParserListener
from TaskLanguage.TaskParser import TaskParser

from TaskSupervisor import graphy
from TaskSupervisor.materialflowupdate import MaterialflowUpdate 

from Entities.materialflow import Materialflow
logger = logging.getLogger(__name__)

def createLoTLan(_taskLanguage):
    try:
        lexer = TaskLexer(InputStream(_taskLanguage))
        stream = CommonTokenStream(lexer)
        parser = TaskParser(stream)
        tree = parser.program() 
        visitor = CreateTreeTaskParserVisitor() 
        t = visitor.visit(tree)
        for key,value in t.taskInfos.iteritems():
            print("NewTask: ",key)
            print("  OnDone: ", value.onDone)
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

INDEGREE_ZERO = 0
SUCCESS_TASK = 1
END_TASK = 2

class Schedular(threading.Thread):
    def __init__(self, _materialflow, ): # name, taskLanguage):
        threading.Thread.__init__(self) 
        logger.info("taskSchedular init")
        self.id = _materialflow.id
        self.tasklanguage = _materialflow.specification
        LoTLan = createLoTLan(self.tasklanguage)

# todo: check if it is parsable and create an own state

        taskGraph = graphy.createGraph(LoTLan.taskInfos)
        tmp = taskGraph.nodes_with_selfloops()
        print(tmp)
        print ("NumberOfSelfLoops:" + str(taskGraph.nodes_with_selfloops()))
        graphy.printGraphInfo(taskGraph)
        graphy.displayGraph(taskGraph, True)
        self.taskGraph = taskGraph
        self.taskInfos = LoTLan.taskInfos
        self.transportOrderStepInfos = LoTLan.transportOrderSteps

        for key, taskInfo in self.taskInfos.iteritems():
            taskInfo.instances = LoTLan.instances

        for key, taskInfo in self.taskInfos.iteritems():
            taskInfo.transportOrderStepInfos = LoTLan.transportOrderSteps    
        self.name = _materialflow.ownerId
        
        self.owner = _materialflow.ownerId

        self.runningTasks = []
        self.historyTasks = [] 
        self.taskManager = []
        self.queue = Queue.Queue()
        self.active = True
        logger.info("taskSchedular init_end")
    
    def setActive(self, _value):
        self.active = _value
        for tm in self.taskManager:
            tm.setActive(_value)

    def addTask(self, task):
        logger.info("taskSchedular addTask" + task.name)
        if(task not in self.runningTasks):
            self.runningTasks.append(task)        
        logger.info("taskSchedular addTask_end")

    def run(self):
        logger.info("taskSchedular start")
        for node in self.taskGraph.nodes:
            if(self.taskGraph.in_degree(node) == INDEGREE_ZERO): # get all starting points from the graph
                tmp_material_flow_update = MaterialflowUpdate(self.owner,node.name, self.queue)
                tmp_material_flow_update.setStartTask(node) # add the starting task
                tmp_material_flow_update.addTask(node) # add the starting task
                successors = nx.dfs_successors(self.taskGraph, source = node).values()
                if(successors):
                    #self.taskGraph.nodes() 
                    for successor in successors: # create linked list with child nodes
                        tmp_material_flow_update.addTask(successor[0])
                    self.taskManager.append(tmp_material_flow_update)
                else:
                    # no successor, single task, reocurrent                    
                    self.taskManager.append(tmp_material_flow_update)
            elif(self.taskGraph.in_degree(node) != INDEGREE_ZERO):
                if(node.position == 0):
                    # hello starting point for the materialflow :)
                    tmp_material_flow_update = MaterialflowUpdate(self.owner,node.name, self.queue)
                    tmp_material_flow_update.setStartTask(node) # add the starting task
                    #tmp_material_flow_update.addTask(node) # add the starting task
                    successors = nx.dfs_successors(self.taskGraph, source = node).values()
                    if(successors):
                        #self.taskGraph.nodes() 
                        for successor in successors: # create linked list with child nodes
                            tmp_material_flow_update.addTask(successor[0])
                        self.taskManager.append(tmp_material_flow_update)
                    else:
                        # no successor, single task, reocurrent                    
                        self.taskManager.append(tmp_material_flow_update)
        for tm in self.taskManager:
            logger.info("taskSchedular, MaterialflowUpdate spawn: " + tm.taskManagerName)
            self.runningTasks.append(tm)
            tm.publishEntity()
            tm.start()

        while (self.active):
            res = self.queue.get()
            logger.info("taskSchedular, taskSMaterialflowUpdateet finished: " + res)
            for tR in self.runningTasks:
                if(tR.taskManagerName == res):
                    tR.join()
                    #tR.deleteEntity()
                    self.runningTasks.remove(tR)                                           
                    tR = None
            if(len(self.runningTasks) == 0):
                self.active = False
                print("We are done; ")
                pass

        logger.info("taskSchedular start_end")
            
    def status(self):
        # return states
        pass