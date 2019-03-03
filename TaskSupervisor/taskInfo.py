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
        self.transportOrders = [] # List of Transport Order (from|to)
        self.onDone = [] # Reference to the next Tasks
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
