# using enum34
from enum import IntEnum

from entity import FiwareEntity

id = 0
idHistory = []


class TaskSpec(FiwareEntity): 
    def __init__(self): 
        FiwareEntity.__init__(self)
        self.TaskSpec = ""