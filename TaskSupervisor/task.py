import threading
import time 
from random import randint
import uuid 
import Queue
import logging

from globals import sanDictQueue

from transportOrder import TransportOrder
from taskInfo import TaskInfo

logger =logging.getLogger(__name__)
class Task(threading.Thread):
    def __init__(self, _taskInfo):
        threading.Thread.__init__(self)
        logger.info("Task init")     
        self.uuid = uuid.uuid1()  
        self.name = _taskInfo.name
        logger.info("Task name: " + self.name + ", uuid:" + str(self.uuid))
        self.taskInfo = _taskInfo
        sanDictQueue.addThread(self.uuid)
        self.q = sanDictQueue.getQueue(self.uuid)
        #self.transportOrder = TransportOrder(self.name)
        logger.info("Task init_done")

    def __str__(self):
        return "Task name: " + self.name + ",uuid: " + str(self.uuid)    
     
    def __repr__(self):
        return self.__str__()

    def run(self):   
        tempVal = (randint(2,7))
        logger.info("Task running, " + str(self))
        print "\nrunning " + self.name + ", sleep " + str(tempVal)
        #time.sleep(tempVal)
        try:
            a = self.q.get(timeout = tempVal)
            if (a):
                print "Received:" +str(a)
        except Queue.Empty:
            pass
        sanDictQueue.removeThread(self.uuid)
        logger.info("Task finished, " + str(self))

