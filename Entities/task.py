from enum import IntEnum



class Task(object): 
    def __init__(self): 
        self.taskOrder = 0
        self.id = ""
        self.type = ""
        self.taskId = 0

    @classmethod
    def getEntity(cls):
        return { "id" : Task.getId() , "type" : Task.getType() }
    
    @classmethod
    def getId(cls):
        return cls.__name__+"1"

        
    @classmethod
    def getType(cls):
        return cls.__name__


    
#0= No-Task, 1 = Start, 2 = Pause, 3 = Cancel, 4 = EmergencyStop, 5 = Reset"
class TaskOrder(IntEnum):
    New = 0 
    Start = 1
    Pause = 2
    Cancel = 3
    EmergencyStop = 4
    Reset = 5
