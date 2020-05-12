__author__ = "Peter Detzner"  
__version__ = "0.0.1a"
__status__ = "Developement"

# import system libs
import threading
import time
import datetime
import uuid
import logging 
import Queue

# import 3rd partie libs

# import local packages
import globals 
from TaskSupervisor.transportOrder import TransportOrder
from helpers.utc import getUTCtime

logger = logging.getLogger(__name__)
ocbHandler = globals.ocbHandler


# this represents a set of tasks
class MaterialflowUpdate(threading.Thread):
    def __init__(self, ownerId, name, q):
        threading.Thread.__init__(self) 
        logger.info("taskManager init")
        
        self.id = str(uuid.uuid1())
        self.taskManagerName = name
        self.time = getUTCtime()
        self.transportOrderList = []
        self.refOwnerId = ownerId


        logger.info("taskMakanger name: " + self.taskManagerName + ", uuid: " + str(self.id))
        self._taskInfoList = []
        #self.runningTask= None
        self._queue = q
        self._start_task = None
        
        self._queuedTransportOrders = Queue.Queue()
        self._runningTransportOrders = list()
        self._finishedTransportOrders = Queue.Queue()
        self._repeat_forever = True
        logger.info("taskManager init_done")

    def setActive(self, _value):
        #self._repeat_forever = _value
        if(_value == False):
            self._queuedTransportOrders.put("_inactive")
        else:
            self._queuedTransportOrders.put("_active")    

    @classmethod
    def newMaterialflowUpdate(self, _object, _queue):
        tM = MaterialflowUpdate(_object.refOwnerId, _object.taskManagerName, _queue)
        tM.transportOrderList = _object.transportOrderList
        tM._taskInfoList = _object._taskInfoList
        return tM

    def __findTaskByName(self, task_name):
        for taskInfo in self._taskInfoList:
            if(str(task_name) == str(taskInfo.name)):
                return taskInfo
        return None

    def setStartTask(self, start_task):
        self._start_task = start_task
        self.addTask(start_task)

    def addTask(self, taskInfo):
        if(taskInfo not in self._taskInfoList):
            self._taskInfoList.append(taskInfo)
            self.transportOrderList.append(taskInfo.name)
    
    def publishEntity(self):
        global ocbHandler
        logger.info("TaskManager publishEntity " + self.taskManagerName)
        self.time = getUTCtime()
      #  ocbHandler.create_entity(self.taskState) 
        ocbHandler.create_entity(self)
        logger.info("TaskManager publishEntity_done")

    def deleteEntity(self):
        global ocbHandler
        logger.info("TaskManager deleteEntity " + self.taskManagerName)
        self.time =  getUTCtime()
        ocbHandler.delete_entity(self.id)
        logger.info("TaskManager deleteEntity_done") 
        
    def threadSpwanTransportOrdeers(self):
        set_inactive = False 
        while(self._repeat_forever):
            next_task = self._queuedTransportOrders.get()
            logger.info("ID: " + str(threading.currentThread().ident))
            if(next_task == "_inactive"):
                set_inactive = True
            elif(next_task == "_active"):
                set_inactive = False 
            elif(next_task.startswith("_DONE")): 
                splitted = next_task.split("|")
                if(len(splitted)==2): # there might be a follow up task which needs to be spawned
                    self._finishedTransportOrders.put(splitted[1])
                elif(len(splitted)==1):
                    break
            elif(next_task != "-"):
                if(set_inactive):
                    break
                else:
                    taskInfo = self.__findTaskByName(str(next_task))
                    if(taskInfo):
                        t = TransportOrder(taskInfo, self.id, self.refOwnerId, self._queuedTransportOrders)
                        t.start()
                        self._runningTransportOrders.append(t)
                        #self._finishedTransportOrders.put(t)


        self._finishedTransportOrders.put("END")
 
    def run(self):

        x = threading.Thread(name ="threadSpwanTransportOrdeers" ,target=self.threadSpwanTransportOrdeers, args=())
        x.start()
        if(self._start_task):
            # add to queue
            self._queuedTransportOrders.put(self._start_task.name)

         # wait here for the end of the threads 
        while self._repeat_forever:
            finished = self._finishedTransportOrders.get()
            
            # ensure, all tasks are proped joined/ended
            for thread in  self._runningTransportOrders:
                if(thread.id == finished):
                    logger.info("End of Thread:" + str(thread))
                    self._runningTransportOrders.remove(thread)
                    thread.join()
            if(finished == "END"):
                break
        x.join()
        self._queue.put(self.taskManagerName)
        

        #self.queue.task_done()
        #print str(datetime.datetime.now().time()) + ", TM_Finnished: " + self.taskManagerName +", start: " + taskInfo.name
        self.deleteEntity()


    def __cmp__(self, other):
        if(self.name == other):
            return 0
        return -1