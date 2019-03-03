import threading
import time 
from random import randint
import uuid 
import Queue
import logging
import datetime

from globals import sanDictQueue
import globals
from transportOrder import TransportOrder
from taskInfo import TaskInfo
 

from Entities.entity import FiwareEntity

ocbHandler = globals.ocbHandler

logger =logging.getLogger(__name__)
class Task():
    def __init__(self, _taskInfo, _taskManagerUuid):
        #threading.Thread.__init__(self)
        logger.info("Task init")     

        # only these attribues will be published
        self.id = str(uuid.uuid4())  
        self.taskManagerId = _taskManagerUuid
        self.taskName = str(_taskInfo.name)
        self.state = State.Idle
        self.time = str(datetime.datetime.now())

        # setting up the thread 
        self._threadRunner = threading.Thread(target=self.run)
        self._threadRunner.setDaemon(True)
        # self._t.start()

        logger.info("Task name: " + self.taskName + ", uuid:" + str(self.id))
        self._taskInfo = _taskInfo
        sanDictQueue.addThread(self.id)
        self._q = sanDictQueue.getQueue(self.id)
        #self.transportOrder = TransportOrder(self.name)
        logger.info("Task init_done")

# thread imitation
    def start(self):
        logger.info("Task start")     
        self.publishEntity()
        self._threadRunner.start()
        logger.info("Task start_done")

    def join(self):
        logger.info("Task join")     
        self._threadRunner.join()
        self.deleteEntity()
        logger.info("Task join_done")     

# updates orion (publish, update and delete)
    def publishEntity(self):
        global ocbHandler
        logger.info("Task publishEntity " + self.taskName)
      #  ocbHandler.create_entity(self.taskState) 
      
        self.time = str(datetime.datetime.now())
        ocbHandler.create_entity(self)
        logger.info("Task publishEntity_done")

    def deleteEntity(self):
        global ocbHandler
        logger.info("Task deleteEntity " + self.taskName)
        self.time = str(datetime.datetime.now())
        ocbHandler.delete_entity(self.id)
        logger.info("Task deleteEntity_done") 

    def updateEntity(self):        
        global ocbHandler
        logger.info("Task updateEntity " + self.taskName)
        self.time = str(datetime.datetime.now())
        ocbHandler.update_entity(self)
        logger.info("Task updateEntity") 
        
    def __str__(self):
        return "Task name: " + self.taskName + ",uuid: " + str(self.id)    
     
    def __repr__(self):
        return self.__str__()

    def run(self):   
        self.state = State.Running
        self.updateEntity()
         
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
        
        self.state = State.Finished
        self.updateEntity()
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