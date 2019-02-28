import threading
import time
import datetime
import uuid

from TaskSupervisor.task import Task
class taskManager(threading.Thread):
    def __init__(self, name, q):
        threading.Thread.__init__(self) 
        self.uuid = uuid.uuid1()
        self.name = name
        self.taskInfoList = []
        self.runningTask= None
        self.queue = q

    def addTask(self, taskInfo):
        if(taskInfo not in self.taskInfoList):
            self.taskInfoList.append(taskInfo)
    
    def run(self):
        
        for taskInfo in self.taskInfoList:
            print str(datetime.datetime.now().time()) + ", TM_Started: " + self.name +", start: " + taskInfo.name
            t = Task(taskInfo)
            t.start()
            t.join()
        self.queue.put(self.name)
        #self.queue.task_done()
        print str(datetime.datetime.now().time()) + ", TM_Finnished: " + self.name +", start: " + taskInfo.name
    

    def __cmp__(self, other):
        if(self.name == other):
            return 0
        return -1