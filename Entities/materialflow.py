# using enum34
from enum import IntEnum

from entity import FiwareEntity

import urllib

id = 0
idHistory = []

from FiwareObjectConverter.objectFiwareConverter import ObjectFiwareConverter

class Materialflow(FiwareEntity): 
    def __init__(self): 
        FiwareEntity.__init__(self)
        self.specification = ""
        self.ownerId = ""
        self.active = False

    @classmethod
    def CreateObjectFromJson(cls, myJson):
        ts = Materialflow()
        try:
            ObjectFiwareConverter.fiware2Obj(myJson, ts, setAttr=True)
            ts.specification = urllib.unquote_plus(ts.specification)
        except Exception as identifier:
            return None
        
        return ts