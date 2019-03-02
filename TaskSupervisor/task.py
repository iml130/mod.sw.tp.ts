import threading
import time 
from random import randint
import uuid 
import Queue
import logging

from globals import sanDictQueue
import globals
from transportOrder import TransportOrder
from taskInfo import TaskInfo
 

from Entities.entity import FiwareEntity

ocbHandler = globals.ocbHandler

logger =logging.getLogger(__name__)
class Task(threading.Thread):
    def __init__(self, _taskInfo, _taskManagerUuid):
        threading.Thread.__init__(self)
        logger.info("Task init")     
        self.id = str(uuid.uuid1())  
        self.taskManagerId = _taskManagerUuid
        self.taskName = str(_taskInfo.name)
        self._taskState = TaskState(self)
        logger.info("Task name: " + self.taskName + ", uuid:" + str(self.id))
        self._taskInfo = _taskInfo
        sanDictQueue.addThread(self.id)
        self._q = sanDictQueue.getQueue(self.id)
        #self.transportOrder = TransportOrder(self.name)
        logger.info("Task init_done")

    def publishEntity(self):
        global ocbHandler
        logger.info("Task publishEntity " + self.taskName)
      #  ocbHandler.create_entity(self.taskState) 
        ocbHandler.create_entity(self)
        logger.info("Task publishEntity_done")

    def deleteEntity(self):
        global ocbHandler
        logger.info("Task deleteEntity " + self.taskName)
        ocbHandler.delete_entity(self.id)
        logger.info("Task deleteEntity_done") 
        
    def __str__(self):
        return "Task name: " + self.taskName + ",uuid: " + str(self.id)    
     
    def __repr__(self):
        return self.__str__()

    def run(self):   
        tempVal = (randint(2,7))
        logger.info("Task running, " + str(self))
        print "\nrunning " + self.taskName + ", sleep " + str(tempVal)
        #time.sleep(tempVal)
        try:
            a = self._q.get(timeout = tempVal)
            if (a):
                print "Received:" +str(a)
        except Queue.Empty:
            pass
        sanDictQueue.removeThread(self.id)
        logger.info("Task finished, " + str(self))

class TaskState(FiwareEntity): 
    
    def __init__(self, _task): 
        if(not isinstance(_task, Task)):
            raise Exception("TypeMissmatch")
        FiwareEntity.__init__(self,id = _task.id)
        self.name = _task.taskName
        self.state = State.Idle
        self.taskId = _task.id
        self.taskManagerId = _task.taskManagerId
        #self.taskSpecUuid = None 
        self.errorMessage = ""

# TASK
#0= No-Task, 1 = Start, 2 = Pause, 3 = Cancel, 4 = EmergencyStop, 5 = Reset"
# TASK_STATE
# Idle : 0, Running : 1, Waiting : 2, Active : 3, Finished : 4, Aborted : 5, Error : 6
class State():
    Idle  = 0 
    Running = 1
    Waiting = 2
    Active = 3
    Finished = 4
    Aborted = 5
    Error = 6