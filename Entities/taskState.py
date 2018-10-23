# using enum34
from enum import IntEnum

from entity import FiwareEntity

id = 0
idHistory = []


class TaskState(FiwareEntity): 
    def __init__(self): 
        self.state = State.Idle
        self.taskId = 0
        self.userAction = UserAction.Idle


#0= No-Task, 1 = Start, 2 = Pause, 3 = Cancel, 4 = EmergencyStop, 5 = Reset"
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


def getNewTaskId():
    global id
    id = id+1    
    if (id not in idHistory):
        idHistory.append(id)
    return id