import threading
import time
import datetime
import uuid
import logging 

from TaskSupervisor.task import Task

logger = logging.getLogger(__name__)

class taskManager(threading.Thread):
    def __init__(self, name, q):
        threading.Thread.__init__(self) 
        logger.info("taskManager init")
        self.uuid = uuid.uuid1()
        self.name = name
        logger.info("taskMakanger name: " + self.name + ", uuid: " + str(self.uuid))
        self.taskInfoList = []
        self.runningTask= None
        self.queue = q
        logger.info("taskManager init_done")

    def addTask(self, taskInfo):
        if(taskInfo not in self.taskInfoList):
            self.taskInfoList.append(taskInfo)
    
    def run(self):
        
        for taskInfo in self.taskInfoList:
            logger.info("tM " + self.name  + " starting Task" + str(taskInfo))
            t = Task(taskInfo)
            t.start()
            t.join()            
            logger.info("tM " + self.name  + " finished Task" + str(taskInfo))
        self.queue.put(self.name)
        #self.queue.task_done()
        print str(datetime.datetime.now().time()) + ", TM_Finnished: " + self.name +", start: " + taskInfo.name
    

    def __cmp__(self, other):
        if(self.name == other):
            return 0
        return -1