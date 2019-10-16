__author__ = "Peter Detzner"
__version__ = "0.0.1a"
__status__ = "Developement"

# IMPORT SYSTEM LIBS
import threading
import time
from random import randint
import uuid
import Queue
import logging
import datetime
import json
import sys
import ast
import uuid

# IMPORT LOCAL libs
from globals import sanDictQueue, rosMessageDispatcher
import globals
 

ocbHandler = globals.ocbHandler

logger = logging.getLogger(__name__)


class TransportOrderUpdate():
    def __init__(self, _transportOrder):
        self.id = str(uuid.uuid4())
        self.name = _transportOrder.taskName
        #self.owner = 
        self.startTime = _transportOrder.startTime
        self.updateTime = _transportOrder.startTime
        self.pickupFrom = _transportOrder.fromId
        self.deliverTo = _transportOrder.toId
        self.refOwnerId = _transportOrder.refOwnerId
        self.refMaterialflowUpdateId = _transportOrder.refMaterialflowUpdateId
        self.state = _transportOrder._transportOrderStateMachine.state
        self.taskInfo = UserAction.Idle


# updates orion (publish, update and delete)        
    def publishEntity(self):
        global ocbHandler
        logger.info("TransportOrderUpdate publishEntity " + self.name)
      #  ocbHandler.create_entity(self.taskState)

        self.updateTime = str(datetime.datetime.now())
        ocbHandler.create_entity(self)
        logger.info("TransportOrderUpdate publishEntity_done")

    def updateEntity(self):
        global ocbHandler
        logger.info("Task updateEntity " + self.name)
        self.updateTime = str(datetime.datetime.now())
        ocbHandler.update_entity(self)
        logger.info("Task updateEntity")

    def deleteEntity(self):
        global ocbHandler
        logger.info("Task deleteEntity " + self.name)
        self.updateTime = str(datetime.datetime.now())
        ocbHandler.delete_entity(self.id)
        logger.info("Task deleteEntity_done")


class UserAction():
    Idle = 0
    WaitForStartTrigger = 1
    MovingToPickupDestination = 2
    WaitForLoading = 3
    MovingToDeliveryDestination = 4
    WaitForUnloading = 5
    
