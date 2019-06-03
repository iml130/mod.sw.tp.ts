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


# IMPORT LOCAL libs
from globals import sanDictQueue, rosMessageDispatcher
import globals


from FiwareObjectConverter.objectFiwareConverter import ObjectFiwareConverter
from Entities.entity import FiwareEntity
from Entities.san import SensorAgent, SensorData

from ROS.moveOrder import rMoveOrder
from ROS.OrderState import OrderState, rosOrderStatus

from TaskSupervisor.transportOrder import TransportOrder
from TaskSupervisor.taskInfo import TaskInfo
from TaskSupervisor.taskState import State, TaskState
from TaskSupervisor.triggerValidator import validateTrigger

ocbHandler = globals.ocbHandler

logger = logging.getLogger(__name__)


# defines
ROS_CALL_ERROR = -1
ROS_CALL_SUCCESS = 0
WAITING_AT_DESTINATION_IN_SECONDS = 5


def obj2JsonArray(_obj):
    tempArray = []
    tempArray.append(_obj)
    print json.dumps(tempArray)
    return (tempArray)
 
class Task():
    def __init__(self, _taskInfo, _taskManagerUuid):
        # threading.Thread.__init__(self)
        logger.info("Task init")

        # only these attribues will be published
        self.id = str(uuid.uuid4())
        self.taskManagerId = _taskManagerUuid
        self.taskName = str(_taskInfo.name)
        self.state = State.Idle
        self.time = str(datetime.datetime.now())

        # setting up the thread
        self._threadRunner = threading.Thread(target=self.run)
        self._threadRunner.setDaemon(True)
        # self._t.start()

        logger.info("Task name: " + self.taskName + ", uuid:" + str(self.id))
        self._taskInfo = _taskInfo
        # 
        sanDictQueue.addThread(self.id)
        rosMessageDispatcher.addThread(self.id)

        self._q = sanDictQueue.getQueue(self.id)
        self._rosQ = rosMessageDispatcher.getQueue(self.id)
        self._subscriptionId = None
        self._transportOrder = TransportOrder(self.taskName)
        logger.info("Task init_done")

    def subscriptionDescription(self):
        return self.taskName + "_" + self.id

# thread imitation
    def start(self):
        logger.info("Task start")
        self.publishEntity()
        self._threadRunner.start()
        logger.info("Task start_done")

    def join(self):
        logger.info("Task join")
        self._threadRunner.join()
        self.deleteEntity()
        logger.info("Task join_done")

# updates orion (publish, update and delete)
    def publishEntity(self):
        global ocbHandler
        logger.info("Task publishEntity " + self.taskName)
      #  ocbHandler.create_entity(self.taskState)

        self.time = str(datetime.datetime.now())
        ocbHandler.create_entity(self)
        logger.info("Task publishEntity_done")


    def updateEntity(self):
        global ocbHandler
        logger.info("Task updateEntity " + self.taskName)
        self.time = str(datetime.datetime.now())
        ocbHandler.update_entity(self)
        logger.info("Task updateEntity")

    def deleteEntity(self):
        global ocbHandler
        logger.info("Task deleteEntity " + self.taskName)
        self.time = str(datetime.datetime.now())
        ocbHandler.delete_entity(self.id)
        logger.info("Task deleteEntity_done")


    def __str__(self):
        return "Task name: " + self.taskName + ",uuid: " + str(self.id)

    def __repr__(self):
        return self.__str__()

    def run(self):
        self.state = State.Running
        self.updateEntity()
        bResendOrder = True
        oldValue = 0
        while(self._transportOrder.state != "finished" and self._transportOrder.state != "error"):
            
            state = self._transportOrder.state
            #print state
            if(state == "init"):
                print state
                # subscribe to trigger events
                if(self._taskInfo.triggers):
                    ts = SensorAgent()
                    self._subscriptionId = ocbHandler.subscribe2Entity(_description=self.subscriptionDescription(), _entities=obj2JsonArray(ts.getEntity()), _notification=globals.parsedConfigFile.getTaskPlannerAddress() + "/san/" + self.id, _generic=True)
                    globals.subscriptionDict[self._subscriptionId] = "SAN"
                self._transportOrder.Initialized()
            elif(state == "waitForTrigger"):
                print state
                if(self._taskInfo.triggers):
                    sensorEntityData = self._q.get()
                    if (sensorEntityData):
                        dd = SensorAgent.CreateObjectFromJson(sensorEntityData["data"][0])
                        sensorData =  dd.findSensorById(self._taskInfo.triggers[0]["left"])
                        if(sensorData):
                            #checkForType() 
                            excpectedType = self._taskInfo.findSensorById(self._taskInfo.triggers[0]["left"])
                            if(validateTrigger(excpectedType, sensorData,self._taskInfo.triggers[0])):
                                self._transportOrder.TriggerReceived()
                else:
                    # no trigger :-) 
                    self._transportOrder.TriggerReceived()
                        

                print "recv trigger"
            elif(state == "moveOrderStart"):
                print state
                
                destinationName =  self._taskInfo.findPositionByName(self._taskInfo.transportOrders[0].pickupFrom[0])
                if(destinationName):
                    try:
                        if(bResendOrder):
                            rMo = rMoveOrder(self.id, destinationName)
                            if(rMo.status == ROS_CALL_SUCCESS): # no need to resend it...
                                bResendOrder = False   
                        rosPacketOrderState = self._rosQ.get(WAITING_AT_DESTINATION_IN_SECONDS)
                        if(rosPacketOrderState):
                            tempUuid = rosPacketOrderState.uuid              
                            if((rosPacketOrderState.status == rosOrderStatus.STARTED or rosPacketOrderState.status==rosOrderStatus.ONGOING) and tempUuid==self.id and bResendOrder == False):
                                print "Robot is moving" + str(rosPacketOrderState.status)
                                self._transportOrder.OrderStart()                    
 
                    except Exception:
                        pass
            elif(state == "moveOrder"): 
                #print state
                try: 
                        ##self.sendMoveOrder(destinationName)
                    rosPacketOrderState = self._rosQ.get()
                    tempUuid = rosPacketOrderState.uuid
                    if(rosPacketOrderState.status == rosOrderStatus.FINISHED and tempUuid ==self.id):
                        self._transportOrder.OrderFinished()
                        bResendOrder = True
                        print "finished"
                    elif(rosPacketOrderState.status == rosOrderStatus.ERROR or rosPacketOrderState.status == rosOrderStatus.WAITING or rosPacketOrderState.status == rosOrderStatus.UNKNOWN):
                        print rosPacketOrderState.status
                except Queue.Empty:
                    pass
            elif(state == "moveOrderFinished"):
                print state
                self._transportOrder.DestinationReached()

            #print state
 
        logger.info("Task running, " + str(self))

        rosMessageDispatcher.removeThread(self.id)
        sanDictQueue.removeThread(self.id)

        try:
            if(self._subscriptionId):
                ocbHandler.deleteSubscriptionById(self._subscriptionId)
        except Exception as ex:
            pass
        
        self.state = State.Finished
        self.updateEntity()
        logger.info("Task finished, " + str(self))


# TASK
# 0= No-Task, 1 = Start, 2 = Pause, 3 = Cancel, 4 = EmergencyStop, 5 = Reset"
# TASK_STATE
# Idle : 0, Running : 1, Waiting : 2, Active : 3, Finished : 4, Aborted : 5, Error : 6


