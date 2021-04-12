""" Contains Task and TaskState Fiware class """

from tasksupervisor.endpoint.fiware_orion.entities.entity import FiwareEntity

class Task(FiwareEntity):
    def __init__(self): 
        self.state = TaskState.NoTask
        self.taskId = 1


#0= No-Task, 1 = Start, 2 = Pause, 3 = Cancel, 4 = EmergencyStop, 5 = Reset"
class TaskState():
    NoTask = 0
    Start = 1
    Pause = 2
    Cancel = 3
    EmergencyStop = 4
    Reset = 5
