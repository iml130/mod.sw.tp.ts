# using enum34
from enum import IntEnum

from entity import FiwareEntity

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

# class San(FiwareEntity): 
#     def __init__(self):  
#         pass
    
#     @classmethod
#     def getEntity(cls):
#         print cls.Type()
#         print cls.Id()
#         return { "id" : "SAN_demo" , "type" : "SensorAgent" }