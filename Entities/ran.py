# using enum34
from enum import IntEnum

from entity import FiwareEntity

class Ran(FiwareEntity): 
    def __init__(self):
        self.dummy =0
        
    @classmethod
    def getEntity(cls):
        print cls.Type()
        print cls.Id()
        return { "id" : "robot_opil_v1" , "type" : "ROBOT" }