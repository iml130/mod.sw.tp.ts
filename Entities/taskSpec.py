# using enum34
from enum import IntEnum

from entity import FiwareEntity

import urllib

id = 0
idHistory = []

from FiwareObjectConverter.objectFiwareConverter import ObjectFiwareConverter

class TaskSpec(FiwareEntity): 
    def __init__(self): 
        FiwareEntity.__init__(self)
        self.TaskSpec = ""

    @classmethod
    def CreateObjectFromJson(cls, myJson):
        ts = TaskSpec()
        try:
            ObjectFiwareConverter.fiware2Obj(myJson, ts, setAttr=True)
            ts.TaskSpec = urllib.unquote_plus(ts.TaskSpec)
        except Exception as identifier:
            return None
        
        return ts