# using enum34
from enum import IntEnum

from entity import FiwareEntity

class San(FiwareEntity): 
    def __init__(self): 
        self.taskOrder = 0 
        self.taskId = 0

    @classmethod
    def getEntity(cls):
        print cls.Type()
        print cls.Id()
        return { "id" : "SAN_demo" , "type" : "SensorAgent" }