# using enum34
from enum import IntEnum

from entity import FiwareEntity
from FiwareObjectConverter.objectFiwareConverter import ObjectFiwareConverter

class SensorData(object):
   def __init__(self, **entries):
      self.manufacturer = ""
      self.measurementType = ""
      self.readings = []
      self.sensorId = ""
      self.sensorType = ""
      self.__dict__.update(entries)  # Insert values from given dict

class SensorAgent(FiwareEntity):
    def __init__(self):
        FiwareEntity.__init__(self)
        self.sensorData = [] # List of SensorData
        self.type = "SAN_demo"
        self.modifiedTime = "" # ISO8601

    @classmethod
    def CreateObjectFromJson(cls, myJson):
        sa = SensorAgent()
        try:
            ObjectFiwareConverter.fiware2Obj(myJson, sa, setAttr=True)
            for i in range(len(sa.sensorData)):
                print sa.sensorData[i] 
                sa.sensorData[i] = SensorData(**sa.sensorData[i])
        except Exception as identifier:
            return None
        
        return sa
    
    def findSensorById(self, _triggerName):
        _triggerName = _triggerName.split(".")[0]
        for sdata in self.sensorData:
            if(sdata.sensorId == _triggerName):
                return sdata
        return None

# class San(FiwareEntity): 
#     def __init__(self):  
#         pass
    
#     @classmethod
#     def getEntity(cls):
#         print cls.Type()
#         print cls.Id()
#         return { "id" : "SAN_demo" , "type" : "SensorAgent" }