# # IMPORT SYSTEM LIBS
# import threading
# import uuid
# import queue
# import logging
# import sys
# import ast
# import json


# # IMPORT LOCAL libs
# #from my_globals import sanDictQueue, rosMessageDispatcher
# #import my_globals
# from tasksupervisor import my_globals
# from tasksupervisor.my_globals import sanDictQueue, rosMessageDispatcher

 
# from tasksupervisor.entities.sensor_agent_node import SensorAgent

# # from tasksupervisor.ROS.transportOrder import rTransportOrder, rManualActionAck
# # from tasksupervisor.ROS.moveOrder import rMoveOrder
# from tasksupervisor.control.ros_order_state import rosOrderStatus, rosTransportOrderStates

# from tasksupervisor.control.ros_interface import RosControl

# from tasksupervisor.TaskSupervisor.transport_order_state_machine import TransportOrderStateMachine, TRANSPORT_ORDER_STATES
# #from tasksupervisor.TaskSupervisor.transportOrderUpdate import TransportOrderUpdate
# from tasksupervisor.entities.transport_order_update import TransportOrderUpdate
# from tasksupervisor.TaskSupervisor.user_action import UserAction
# from tasksupervisor.lotlan.task_info import TaskInfo
# from tasksupervisor.TaskSupervisor.taskState import State, TaskState
# from tasksupervisor.TaskSupervisor.triggerValidator import validate_event
 
# from tasksupervisor.helpers.utc import get_utc_time

# ORION_CONNECTOR = my_globals.ORION_CONNECTOR

# logger = logging.getLogger(__name__)


# defines
# ROS_CALL_ERROR = -1
# CREATE_TRANSPORT_ORDER_SUCCESS = 0
# QUEUE_WAIT_TIME_IN_SECONDS = 5
# TRANSPORT_ODER_DONE = "_DONE"


# def object_to_json_array(_obj):
#     tempArray = []
#     tempArray.append(_obj)
#     logger.info(json.dumps(tempArray))
#     return (tempArray)


# class TransportOrder():
#     def __init__(self, _task_info, _refMaterialflowUpdateId, _refOwnerId, queueTransportOrders, task_supervisor_knowledge):
#         # threading.Thread.__init__(self)
#         logger.info("Task init")

#         # only these attribues will be published
#         self.id = str(uuid.uuid4())
#         self.refMaterialflowUpdateId = _refMaterialflowUpdateId
#         self.refOwnerId = _refOwnerId
#         self.taskName = str(_task_info.name)
#         self.state = State.Idle
#         self.startTime = get_utc_time()

#         # setting up the thread
#         self._threadRunner = threading.Thread(target=self.run)
#         self._threadRunner.setDaemon(True)
#         self._threadRunner.name = str(self.id)
#         # self._t.start()

#         logger.info("Task name: %s, uuid: %s", self.taskName, str(self.id))
#         self._task_info = _task_info

#         # store the names:
#         self.fromId = self._task_info.findLocationByTransportOrderStep(
#             self._task_info.transportOrders[0].pickupFrom)
#         self.toId = self._task_info.findLocationByTransportOrderStep(
#             self._task_info.transportOrders[0].deliverTo)

#         # temporary uids for the moveOrders
#         self._fromUuid = str(uuid.uuid4())
#         self._toUuid = str(uuid.uuid4())

#         self._task_supervisor_knowledge = task_supervisor_knowledge
#         #
#         sanDictQueue.addThread(self.id)

#         rosMessageDispatcher.addThread(self.id)
#         # rosMessageDispatcher.addThread(self._fromUuid)
#         # rosMessageDispatcher.addThread(self._toUuid)
#         self._queuedTransportOrders = queueTransportOrders

#         self._sanQueue = sanDictQueue.getQueue(self.id)
#         self._rosQueueTO = rosMessageDispatcher.getQueue(self.id)
#         # self._rosQueueTO_From = rosMessageDispatcher.getQueue(self._fromUuid)
#         # self._rosQueueTO_To = rosMessageDispatcher.getQueue(self._toUuid)

#         self._subscriptionId = None
#         self._transportOrderStateMachine = TransportOrderStateMachine(
#             self.taskName)
#         self._robotId = None
#         self._transportOrderUpdate = TransportOrderUpdate(self)
#         self._robot = None
#         logger.info("Task init_done")

#     def subscriptionDescription(self):
#         return self.taskName + "_" + self.id + "_"

# # thread imitation
#     def start(self):
#         logger.info("Task start")
#         # self.publishEntity()
#         self._threadRunner.start()
#         logger.info("Task start_done")

#     def join(self):
#         logger.info("Task join")
#         self._threadRunner.join()
#         # self.deleteEntity()
#         logger.info("Task join_done")

# # updates orion (publish, update and delete)
#     def publishEntity(self):
#         global ORION_CONNECTOR
#         logger.info("Task publishEntity " + self.taskName)
#       #  ORION_CONNECTOR.create_entity(self.taskState)

#         self.updateTime = get_utc_time()
#         ORION_CONNECTOR.create_entity(self)
#         logger.info("Task publishEntity_done")

#     def updateEntity(self):
#         global ORION_CONNECTOR
#         logger.info("Task updateEntity " + self.taskName)
#         self.updateTime = get_utc_time()
#         ORION_CONNECTOR.update_entity(self)
#         logger.info("Task updateEntity")

#     def deleteEntity(self):
#         global ORION_CONNECTOR
#         logger.info("Task deleteEntity " + self.taskName)
#         self.updateTime = get_utc_time()
#         ORION_CONNECTOR.delete_entity(self.id)
#         logger.info("Task deleteEntity_done")

#     def __str__(self):
#         return "Task name: " + self.taskName + ",uuid: " + str(self.id)

#     def __repr__(self):
#         return self.__str__()

#     def deleteSubscription(self):
#         try:
#             if(self._subscriptionId):
#                 ORION_CONNECTOR.delete_subscription_by_id(self._subscriptionId)
#                 if(self._subscriptionId in my_globals.subscriptionDict):
#                     del my_globals.subscriptionDict[self._subscriptionId]
#         except Exception as ex:
#             logger.info("Error in deleteSubscription: %s", str(ex))

#     def registerForSensor(self):
#         pass

#     def is_current_state(self, _state):
#         return self._transportOrderStateMachine.current_state_is(_state)

#     def run(self):
#         self.state = State.Running
#         # self.updateEntity()
#         hasOnDone = False
#         # self._transportOrderUpdate.publishEntity()
#         self._task_supervisor_knowledge.orion_connector.create_entity(
#             self._transportOrderUpdate)

#         bResendOrder = True

#         # this is a huge state machine, quite ugly coded...
#         #
#         while(self._transportOrderStateMachine.get_state() != "finished" and self._transportOrderStateMachine.get_state() != "error"):

#             current_state = self._transportOrderStateMachine.state
#             # print state
#             if self.is_current_state(TRANSPORT_ORDER_STATES.INIT):
#                 logger.info(current_state + ", id: " + self.id +
#                             ", Task: " + self.taskName)
#                 # subscribe to trigger events
#                 if(self._task_info.triggeredBy):
#                     ts = SensorAgent(self._task_info.findSensorIdByName(
#                         self._task_info.triggeredBy[0]['left']))
#                     self._transportOrderUpdate.taskInfo = UserAction.WaitForStartTrigger
#                     self._transportOrderUpdate.update_time()
#                     self._task_supervisor_knowledge.orion_connector.update_entity(
#                         self._transportOrderUpdate)
#                     # self._transportOrderUpdate.updateEntity()
#                     self._subscriptionId = ORION_CONNECTOR.subscribe_to_entity(_description=self.subscriptionDescription(
#                     ) + "WaitForTrigger", _entities=object_to_json_array(ts.getEntity()), _notification=my_globals.parsed_config_file.getTaskPlannerAddress() + "/san/" + self.id)
#                     my_globals.subscriptionDict[self._subscriptionId] = self.id
#                 self._transportOrderStateMachine.Initialized()
#             elif self.is_current_state(TRANSPORT_ORDER_STATES.WAIT_FOR_TRIGGER):
#                 logger.info(current_state + ", id: " + self.id +
#                             ", Task: " + self.taskName)

#                 # check if a trigger even exists or not
#                 if(self._task_info.triggeredBy):
#                     sensorEntityData = self._sanQueue.get()
#                     taskTrigger = self._task_info.triggeredBy[0]
#                     retVal = checkIfSensorEventTriggersNextTransportUpdate(
#                         sensorEntityData, self._subscriptionId, taskTrigger, self._task_info)

#                     if(retVal == True):
#                         self.deleteSubscription()
#                         self._transportOrderStateMachine.TriggerReceived()
#                         self._transportOrderUpdate.taskInfo = UserAction.MovingToPickupDestination
#                         self._transportOrderUpdate.update_time()
#                         self._task_supervisor_knowledge.orion_connector.update_entity(
#                             self._transportOrderUpdate)
#                         # self._transportOrderUpdate.updateEntity()
#                 else:
#                     # no trigger :-)
#                     self._transportOrderUpdate.taskInfo = UserAction.MovingToPickupDestination
#                     self._transportOrderUpdate.update_time()
#                     self._task_supervisor_knowledge.orion_connector.update_entity(
#                         self._transportOrderUpdate)
#                     # self._transportOrderUpdate.updateEntity()
#                     self._transportOrderStateMachine.TriggerReceived()
#             elif self.is_current_state(TRANSPORT_ORDER_STATES.START_PICKUP):

#                 logger.info(current_state + ", id: " + self.id +
#                             ", Task: " + self.taskName)
#                 if(self.fromId):
#                     try:
#                         if(bResendOrder):  # check if we have to resend it,
#                             # working MO
#                             #rMo = rMoveOrder(self._fromUuid, self.fromId)
#                             pickupType = self._task_info.findLocationTypeByTransportOrderStep(
#                                 self._task_info.transportOrders[0].pickupFrom)
#                             dropoffType = self._task_info.findLocationTypeByTransportOrderStep(
#                                 self._task_info.transportOrders[0].deliverTo)
#                             # self._robot = round_robin.getNextRobotByType(pickupType)
#                             self._robot = self._task_supervisor_knowledge.optimizer.get_next_agv_by_type(
#                                 pickupType)
#                             if(self._robot is None):
#                                 # okay, lets break out
#                                 self._transportOrderStateMachine.TransportOrderError()
#                                 self._transportOrderUpdate.robotId = 0
#                                 self._transportOrderUpdate.state = self._transportOrderStateMachine.get_state()
#                                 self._transportOrderUpdate.update_time()
#                                 self._task_supervisor_knowledge.orion_connector.update_entity(
#                                     self._transportOrderUpdate)
#                                 # self._transportOrderUpdate.updateEntity()
#                                 logger.error(
#                                     "No valid robot selection; Please check TS configuration and Materialflow Description")
#                                 break

#                             self._robotId = self._robot.id
#                             self._transportOrderUpdate.robotId = self._robotId
#                             self._transportOrderUpdate.update_time()
#                             self._task_supervisor_knowledge.orion_connector.update_entity(
#                                 self._transportOrderUpdate)
#                             # self._transportOrderUpdate.updateEntity()

# #                            rTo = rTransportOrder(self.id, self.fromId, self.toId, self._robotId)
#                             rTo = RosControl()
#                             rTo.create_transport_order(
#                                 self.id, self.fromId, self.toId, self._robotId)

#                             # no need to resend it...
#                             if(rTo.status == CREATE_TRANSPORT_ORDER_SUCCESS):
#                                 bResendOrder = False
#                         rosPacketOrderState = self._rosQueueTO.get(
#                             QUEUE_WAIT_TIME_IN_SECONDS)

#                         if(rosPacketOrderState):
#                             tempUuid = rosPacketOrderState.uuid
#                             tempState = rosPacketOrderState.state
#                             if((tempState == rosTransportOrderStates.TO_LOAD_MOVE_ORDER_START or tempState == rosTransportOrderStates.TO_LOAD_MOVE_ORDER_ONGOING) and tempUuid == self.id and bResendOrder == 0):
#                                 logger.info("TransportOrder - Robot SHOULD moving" + str(
#                                     rosPacketOrderState.status) + ", Task " + self.taskName + ", id: " + self.id)
#                                 self._transportOrderStateMachine.GotoPickupDestination()

#                     except Exception:
#                         logger.info("startPickup, didnt work")
#             elif self.is_current_state(TRANSPORT_ORDER_STATES.MOVING_TO_PICKUP):

#                 logger.info(current_state + ", id: " + self.id +
#                             ", Task: " + self.taskName)
#                 try:
#                     # self.sendMoveOrder(destinationName)
#                     rosPacketOrderState = self._rosQueueTO.get()

#                     tempUuid = rosPacketOrderState.uuid
#                     tempState = rosPacketOrderState.state

#                     if(tempState == rosTransportOrderStates.TO_LOAD_MOVE_ORDER_FINISHED and tempUuid == self.id):

#                         bResendOrder = True
#                         tmpToPickUp = self._task_info.transport_order_step_infos[
#                             self._task_info.transportOrders[0].pickupFrom]
#                         if(tmpToPickUp.finishedBy):
#                             ts = SensorAgent(self._task_info.findSensorIdByName(
#                                 tmpToPickUp.finishedBy[0]['left']))
#                             self._subscriptionId = ORION_CONNECTOR.subscribe_to_entity(_description=self.subscriptionDescription(
#                             ) + "WaitForManualLoading", _entities=object_to_json_array(ts.getEntity()), _notification=my_globals.parsed_config_file.getTaskPlannerAddress() + "/san/" + self.id)
#                             my_globals.subscriptionDict[self._subscriptionId] = self.id

#                     elif((tempState == rosTransportOrderStates.TO_LOAD_ACTION_START or tempState == rosTransportOrderStates.TO_LOAD_ACTION_ONGOING) and tempUuid == self.id):
#                         self._transportOrderUpdate.taskInfo = UserAction.WaitForLoading
#                         self._transportOrderUpdate.update_time()
#                         self._task_supervisor_knowledge.orion_connector.update_entity(
#                             self._transportOrderUpdate)
#                         # self._transportOrderUpdate.updateEntity()
#                         self._transportOrderStateMachine.ArrivedAtPickupDestination()

#                     elif(rosPacketOrderState.status == rosOrderStatus.ERROR or rosPacketOrderState.status == rosOrderStatus.WAITING or rosPacketOrderState.status == rosOrderStatus.UNKNOWN):
#                         logger.info(rosPacketOrderState.status)
#                 except Queue.Empty:
#                     pass
#             elif self.is_current_state(TRANSPORT_ORDER_STATES.WAITING_FOR_LOADING):

#                 logger.info(current_state + ", id: " + self.id + ", Task: " +
#                             self.taskName + " - Waiting for _Loading_ Ack")

#                 tmpToPickUp = self._task_info.transport_order_step_infos[
#                     self._task_info.transportOrders[0].pickupFrom]

#                 if(tmpToPickUp.finishedBy):
#                     sensorEntityData = self._sanQueue.get()
#                     taskTrigger = tmpToPickUp.finishedBy[0]
#                     retVal = checkIfSensorEventTriggersNextTransportUpdate(
#                         sensorEntityData, self._subscriptionId, taskTrigger, self._task_info)
#                     if(retVal == True):
#                         self.deleteSubscription()
#                         # status = rManualActionAck(self._robotId)
#                         rTo = RosControl()
#                         status = rTo.manual_action_acknowledge(self._robotId)
#                         # no need to resend it...
#                         if(status == CREATE_TRANSPORT_ORDER_SUCCESS):
#                             self._transportOrderStateMachine.AgvIsLoaded()
#                             self._transportOrderUpdate.update_time()
#                             self._task_supervisor_knowledge.orion_connector.update_entity(
#                                 self._transportOrderUpdate)
#                             # self._transportOrderUpdate.updateEntity()

#                 else:
#                     self._transportOrderStateMachine.AgvIsLoaded()

#                 # check if there is a follow up task after picking up at transportorderstep
#                 if(tmpToPickUp.onDone):
#                     hasOnDone = True
#                     for onDone in tmpToPickUp.onDone:
#                         self._queuedTransportOrders.put(onDone)

#             elif self.is_current_state(TRANSPORT_ORDER_STATES.START_DELIVERY):

#                 logger.info("Robot SHOULD moving" + str(rosPacketOrderState.status) +
#                             ", Task " + self.taskName + ", id: " + self.id)
#                 if(self.toId):
#                     try:
#                         rosPacketOrderState = self._rosQueueTO.get()
#                         # if(bResendOrder): #check if we have to resend it,
#                         #     rMo = rMoveOrder(self._toUuid, self.toId)

#                         if(rosPacketOrderState):
#                             tempUuid = rosPacketOrderState.uuid
#                             tempState = rosPacketOrderState.state
#                             if((tempState == rosTransportOrderStates.TO_UNLOAD_MOVE_ORDER_START or tempState == rosTransportOrderStates.TO_UNLOAD_MOVE_ORDER_ONGOING) and tempUuid == self.id):
#                                 logger.info("TransportOrder - Robot SHOULD moving" + str(
#                                     rosPacketOrderState.status) + ", Task " + self.taskName + ", id: " + self.id)
#                                 self._transportOrderUpdate.taskInfo = UserAction.MovingToDeliveryDestination
#                                 self._transportOrderUpdate.update_time()
#                                 self._task_supervisor_knowledge.orion_connector.update_entity(
#                                     self._transportOrderUpdate)
#                                 # self._transportOrderUpdate.updateEntity()
#                                 self._transportOrderStateMachine.GotoDeliveryDestination()

#                     except Exception:
#                         pass

#             elif self.is_current_state(TRANSPORT_ORDER_STATES.MOVING_TO_DELIVERY):
#                 logger.info(current_state + ", id: " + self.id +
#                             ", Task: " + self.taskName)
#                 try:
#                     # self.sendMoveOrder(destinationName)
#                     rosPacketOrderState = self._rosQueueTO.get()
#                     tempUuid = rosPacketOrderState.uuid
#                     tempState = rosPacketOrderState.state
#                     if(tempState == rosTransportOrderStates.TO_UNLOAD_MOVE_ORDER_FINISHED and tempUuid == self.id):
#                         bResendOrder = True
#                         tmpToPickUp = self._task_info.transport_order_step_infos[
#                             self._task_info.transportOrders[0].deliverTo]
#                         if(tmpToPickUp.finishedBy):
#                             ts = SensorAgent(self._task_info.findSensorIdByName(
#                                 tmpToPickUp.finishedBy[0]['left']))
#                             self._subscriptionId = ORION_CONNECTOR.subscribe_to_entity(_description=self.subscriptionDescription(
#                             ) + "WaitForManualUnLoading", _entities=object_to_json_array(ts.getEntity()), _notification=my_globals.parsed_config_file.getTaskPlannerAddress() + "/san/" + self.id)
#                             my_globals.subscriptionDict[self._subscriptionId] = self.id

#                     elif((tempState == rosTransportOrderStates.TO_UNLOAD_ACTION_START or tempState == rosTransportOrderStates.TO_UNLOAD_ACTION_ONGOING) and tempUuid == self.id):
#                         self._transportOrderUpdate.taskInfo = UserAction.WaitForUnloading
#                         self._transportOrderUpdate.update_time()
#                         self._task_supervisor_knowledge.orion_connector.update_entity(
#                             self._transportOrderUpdate)
#                         # self._transportOrderUpdate.updateEntity()
#                         self._transportOrderStateMachine.ArrivedAtDeliveryDestination()

#                     elif(rosPacketOrderState.status == rosOrderStatus.ERROR or rosPacketOrderState.status == rosOrderStatus.WAITING or rosPacketOrderState.status == rosOrderStatus.UNKNOWN):
#                         print(rosPacketOrderState.status)
#                 except Queue.Empty:
#                     pass
#             elif self.is_current_state(TRANSPORT_ORDER_STATES.WAITING_FOR_UNLOADING):

#                 logger.info(current_state + ", id: " + self.id + ", Task: " +
#                             self.taskName + " - Waiting for _UNLoading_ Ack")
#                 tmpToDelivery = self._task_info.transport_order_step_infos[
#                     self._task_info.transportOrders[0].deliverTo]
#                 if(tmpToDelivery.finishedBy):
#                     sensorEntityData = self._sanQueue.get()

#                     taskTrigger = tmpToDelivery.finishedBy[0]
#                     retVal = checkIfSensorEventTriggersNextTransportUpdate(
#                         sensorEntityData, self._subscriptionId, taskTrigger, self._task_info)
#                     if(retVal == True):
#                         self.deleteSubscription()
#                         self._transportOrderUpdate.taskInfo = UserAction.Idle
#                         # status = rManualActionAck(self._robotId)
#                         rTo = RosControl()
#                         status = rTo.manual_action_acknowledge(self._robotId)

#                         if(status == CREATE_TRANSPORT_ORDER_SUCCESS):
#                             self._transportOrderStateMachine.AgvIsUnloaded()
#                             self._transportOrderUpdate.update_time()
#                             self._task_supervisor_knowledge.orion_connector.update_entity(
#                                 self._transportOrderUpdate)
#                             # self._transportOrderUpdate.updateEntity()
#                 else:
#                     self._transportOrderStateMachine.AgvIsUnloaded()

#                     # check if there is a follow up task after dropping at transportorderstep
#                 if(tmpToDelivery.onDone):
#                     hasOnDone = True
#                     for onDone in tmpToDelivery.onDone:
#                         self._queuedTransportOrders.put(onDone)
#             elif self.is_current_state(TRANSPORT_ORDER_STATES.MOVE_ORDER_FINISHED):

#                 logger.info(current_state + ", id: " + self.id +
#                             ", Task: " + self.taskName)
#                 self._transportOrderStateMachine.DestinationReached()

#             # print state

#         logger.info("Task ist ending, " + self.taskName + ", id: " + self.id)

#         # clean up the all not needed queus
#         sanDictQueue.removeThread(self.id)
#         rosMessageDispatcher.removeThread(self.id)
#         # rosMessageDispatcher.removeThread(self._fromUuid)
#         # rosMessageDispatcher.removeThread(self._toUuid)

#         try:
#             if(self._subscriptionId):
#                 # ORION_CONNECTOR.delete_subscription_by_id(self._subscriptionId)
#                 self.deleteSubscription()
#         except Exception as ex:
#             logger.error("another error in transportOrder %s", str(ex))

#         self.state = State.Finished
#         # self.updateEntity()
#         self._task_supervisor_knowledge.orion_connector.delete_entity(
#             self._transportOrderUpdate.getId())
#         # self._transportOrderUpdate.deleteEntity()
#         logger.info("TransportOrder finished: %s", str(self))
#         # check if there is a follow up task after the delivery
#         if(self._task_info.onDone):
#             for onDone in self._task_info.onDone:
#                 self._queuedTransportOrders.put(onDone)
#         else:
#             if(not hasOnDone):  # here is no follow up task... lets close everything
#                 self._queuedTransportOrders.put(TRANSPORT_ODER_DONE)
#             else:
#                 self._queuedTransportOrders.put(
#                     TRANSPORT_ODER_DONE + self._threadRunner.name)


# def checkIfSensorEventTriggersNextTransportUpdate(sensorEntityData, subscriptionId, taskTrigger, taskInfo):
#     if (sensorEntityData):
#         if("subscriptionId" in sensorEntityData):

#             if(sensorEntityData["subscriptionId"] == subscriptionId):
#                 for sensorData in sensorEntityData["data"]:
#                     dd = SensorAgent.CreateObjectFromJson(sensorData)
#                     if(taskTrigger):
#                         if(dd.readings):
#                             excpectedType = taskInfo.matchEventNameBySensorId(
#                                 dd.sensorID, taskTrigger["left"])
#                             if excpectedType:
#                                 if(validate_event(excpectedType, dd.readings, taskTrigger)):
#                                     return True
#     return False
# # TASK
# # 0= No-Task, 1 = Start, 2 = Pause, 3 = Cancel, 4 = EmergencyStop, 5 = Reset"
# # TASK_STATE
# # Idle : 0, Running : 1, Waiting : 2, Active : 3, Finished : 4, Aborted : 5, Error : 6
