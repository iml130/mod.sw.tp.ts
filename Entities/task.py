# using enum34
from enum import IntEnum

from entity import FiwareEntity

class Task(FiwareEntity): 
    def __init__(self): 
        self.taskOrder = 0 
        self.taskId = 0


#0= No-Task, 1 = Start, 2 = Pause, 3 = Cancel, 4 = EmergencyStop, 5 = Reset"
class TaskOrder():
    New = 0 
    Start = 1
    Pause = 2
    Cancel = 3
    EmergencyStop = 4
    Reset = 5
