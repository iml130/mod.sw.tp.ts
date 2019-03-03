# using enum34
from enum import IntEnum

from entity import FiwareEntity

id = 0
idHistory = []
from TaskSupervisor.task import Task

class TaskState(FiwareEntity): 
    
    def __init__(self, _task): 
        if(not isinstance(_task, Task)):
            raise Exception("TypeMissmatch")
        FiwareEntity.__init__(self,id = _task.id)
        self.name = _task.name
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

class UserAction():
    Idle = 0
    WaitForLoading = 1
    WaitForUnloading = 2

def getCurrentTaskId():
    global id
    return id

def getNewTaskId():
    global id
    id = id+1    
    if (id not in idHistory):
        idHistory.append(id)
    return id