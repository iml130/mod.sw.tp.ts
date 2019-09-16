__author__ = "Peter Detzner"  
__version__ = "0.0.1a"
__status__ = "Developement"

import logging

logger= logging.getLogger(__name__)
class TaskInfo(object):
    def __init__(self):
        logger.info("TaskInfo init")
        self.name = None # String Name of Task
        self.triggers = [] # List of Triggers
        self.transportOrders = [] # List of Transport Order (pickupFrom|deliverTo)
        self.onDone = [] # Reference to the next Tasks
        self.instances = None
        logger.info("TaskInfo init_done")

    def addChild(self, _child):
        
        logger.info("TaskInfo addChild")
        if(_child not in self.onDone):
            self.onDone.append(_child)
        logger.info("TaskInfo addChild_done")


    def __str__(self):
        return "TaskInfo: " + self.name
     
    def __repr__(self):
        return self.__str__()

    def findPositionByName(self, positionName):
        if self.instances:
            if(positionName in self.instances):
                return self.instances[positionName].keyval["position"].replace('"',"")
    
    def findSensorById(self, sensorId):
        sensorId = sensorId.split(".")[0]
        if self.instances:
            for value in self.instances:
                if "sensorId" in self.instances[value].keyval:
                    print "Looking for : " + sensorId + ", found so far SensorId: "  + self.instances[value].keyval["sensorId"].replace('"', '')
                    if(self.instances[value].keyval["sensorId"].replace('"', '') == sensorId):
                        print "SENSOR MATCH"
                        return self.instances[value].keyval["type"].replace('"', '')
        return None
