""" Contains TaskState class """

from tasksupervisor.endpoint.fiware_orion.entities.entity import FiwareEntity
from tasksupervisor.endpoint.fiware_orion.entities.task import Task

class TaskState(FiwareEntity):
    """ Represents the current state of the Task """
    def __init__(self, _task):
        if not isinstance(_task, Task):
            raise Exception("TypeMissmatch")
        FiwareEntity.__init__(self, id=_task.id)
        self.name = _task.taskName
        self.state = State.Idle
        self.task_id = _task.id
        self.task_manager_id = _task.taskManagerId
        self.error_message = ""


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
