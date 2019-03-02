from enum import IntEnum

  



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