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
        self.taskList = []
        self.runningTask= None
        self.queue = q

    def addTask(self, task):
        if(task not in self.taskList):
            self.taskList.append(task)
    
    def run(self):
        
        for task in self.taskList:    
            print str(datetime.datetime.now().time()) + ", TM_Started: " + self.name +", start: " + task.name
            t = Task(task.name)
            t.start()
            t.join()
        self.queue.put(self.name)
        #self.queue.task_done()
        print str(datetime.datetime.now().time()) + ", TM_Finnished: " + self.name +", start: " + task.name
    

    def __cmp__(self, other):
        if(self.name == other):
            return 0
        return -1