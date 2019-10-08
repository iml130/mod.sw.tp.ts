# using enum34
from enum import IntEnum

from entity import FiwareEntity

id = 0
idHistory = []


class MaterialflowSpecificationState(FiwareEntity): 
    def __init__(self): 
        FiwareEntity.__init__(self)
        self.refId = ""
        self.state = SpecState.Idle
        self.message = ""

# TASK
#0= No-Task, 1 = Start, 2 = Pause, 3 = Cancel, 4 = EmergencyStop, 5 = Reset"
# TASK_STATE
# Idle : 0, Running : 1, Waiting : 2, Active : 3, Finished : 4, Aborted : 5, Error : 6
class SpecState():
    Idle = 0
    Ok = 1
    Error = -1

