__author__ = "Peter Detzner"  
__version__ = "0.0.1a"
__status__ = "Developement"

import logging

logger= logging.getLogger(__name__)

class TaskInfo(object):
    def __init__(self):
        logger.info("TaskInfo init")
        self.name = None # String Name of Task
        self.triggeredBy = [] # List of Triggers
        self.transportOrders = [] # List of Transport Order (from|to)
        self.onDone = [] # Reference to the next Tasks
        self.repeat = -1 # uninitialized
        self.finishedBy = []
        self.instances = {}
        self.transportOrderStepInfos = {}
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

    def findLocationByTransportOrderStep(self, _toStep):
        if(self.transportOrderStepInfos):
            if(_toStep in self.transportOrderStepInfos):
                for key, value in self.transportOrderStepInfos.iteritems():
                    if(key == _toStep):                       
                        if(value.location != ""):
                            tempName = self.transportOrderStepInfos[_toStep].location
                            return self.findPositionByName(tempName)
                    #rint(key, value)
                
                    
    def findSensorIdByName(self, eventName):
        if self.instances:
            if(eventName in self.instances):
                return self.instances[eventName].keyval["name"].replace('"',"")

    def findPositionByName(self, positionName):
   
        if self.instances:
            if(positionName in self.instances):
                return self.instances[positionName].keyval["name"].replace('"',"")
    
    def matchEventNameBySensorId(self, sensorId, eventName):
        sensorId = sensorId.split(".")[0]
        if self.instances:
            for value in self.instances:
                if(value == eventName):
                    if "name" in self.instances[value].keyval:
                        logger.info("Looking for SensorId: " + sensorId + ", found so far SensorId: "  + self.instances[value].keyval["name"].replace('"', ''))
                        if(self.instances[value].keyval["name"].replace('"', '') == sensorId):
                            logger.info("Sensor Match for the Event, need to check also the expected value/type against the received value/type")
                            return self.instances[value].keyval["type"].replace('"', '')
        return None
