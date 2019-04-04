from enum import IntEnum
from Entities.entity import FiwareEntity

class TaskState(FiwareEntity):

    def __init__(self, _task):
        if(not isinstance(_task, Task)):
            raise Exception("TypeMissmatch")
        FiwareEntity.__init__(self, id=_task.id)
        self.name = _task.taskName
        self.state = State.Idle
        self.taskId = _task.id
        self.taskManagerId = _task.taskManagerId
        # self.taskSpecUuid = None
        self.errorMessage = ""


class State():
    Idle = 0
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