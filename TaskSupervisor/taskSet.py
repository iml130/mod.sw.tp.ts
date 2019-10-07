__author__ = "Peter Detzner"  
__version__ = "0.0.1a"
__status__ = "Developement"


import threading
import time
import datetime
import uuid
import logging 
import globals 
from TaskSupervisor.task import Task

logger = logging.getLogger(__name__)
ocbHandler = globals.ocbHandler

# this represents a set of tasks
class taskSet(threading.Thread):
    def __init__(self, name, q):
        threading.Thread.__init__(self) 
        logger.info("taskManager init")
        
        self.id = str(uuid.uuid1())
        self.taskManagerName = name
        self.time = str(datetime.datetime.now())
        self.taskList = []

        

        logger.info("taskMakanger name: " + self.taskManagerName + ", uuid: " + str(self.id))
        self._taskInfoList = []
        #self.runningTask= None
        self._queue = q
        logger.info("taskManager init_done")

    @classmethod
    def newTaskSet(self, _object, _queue):
        tM = taskSet(_object.taskManagerName, _queue)
        tM.taskList = _object.taskList
        tM._taskInfoList = _object._taskInfoList
        return tM

    def addTask(self, taskInfo):
        if(taskInfo not in self._taskInfoList):
            self._taskInfoList.append(taskInfo)
            self.taskList.append(taskInfo.name)
    
    def publishEntity(self):
        global ocbHandler
        logger.info("TaskManager publishEntity " + self.taskManagerName)
        self.time = str(datetime.datetime.now())
      #  ocbHandler.create_entity(self.taskState) 
        ocbHandler.create_entity(self)
        logger.info("TaskManager publishEntity_done")

    def deleteEntity(self):
        global ocbHandler
        logger.info("TaskManager deleteEntity " + self.taskManagerName)
        self.time = str(datetime.datetime.now())
        ocbHandler.delete_entity(self.id)
        logger.info("TaskManager deleteEntity_done") 
        
    def run(self):
        
        for taskInfo in self._taskInfoList:
            logger.info("tM " + self.taskManagerName  + " starting Task" + str(taskInfo))
            t = Task(taskInfo, self.id)
            #t.publishEntity()
            t.start()
            t.join()            
            #t.deleteEntity()
            logger.info("tM " + self.taskManagerName  + " finished Task" + str(taskInfo))
        self._queue.put(self.taskManagerName)
        #self.queue.task_done()
        print str(datetime.datetime.now().time()) + ", TM_Finnished: " + self.taskManagerName +", start: " + taskInfo.name
        self.deleteEntity()

    def __cmp__(self, other):
        if(self.name == other):
            return 0
        return -1