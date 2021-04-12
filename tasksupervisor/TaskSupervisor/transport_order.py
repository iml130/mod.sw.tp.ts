"""
    This class is a beast. Within this class, a TransportOrder (TO) is assigned to an AGV (for now ;)).
    But the selection of an AGV is done once it is needed.
"""
import threading
import logging
import json
import queue

# import local libs
from lotlan_scheduler.api.event import Event

from tasksupervisor.endpoint.fiware_orion.entities.sensor_agent_node import SensorAgent

from tasksupervisor.control.ros_order_state import rosOrderStatus, rosTransportOrderStates

from tasksupervisor.api.transport_order_update import TransportOrderUpdate

from tasksupervisor.TaskSupervisor.transport_order_state_machine import TransportOrderStateMachine
from tasksupervisor.TaskSupervisor.transport_order_state_machine import TRANSPORT_ORDER_STATES

from tasksupervisor.TaskSupervisor.taskState import State
from tasksupervisor.helpers.utc import get_utc_time

from tasksupervisor.TaskSupervisor.multiq import MultiQueue
from tasksupervisor.TaskSupervisor.user_action import UserAction


# defines
ROS_CALL_ERROR = -1
CREATE_TRANSPORT_ORDER_SUCCESS = 0
QUEUE_WAIT_TIME_IN_SECONDS = 5
TRANSPORT_ODER_DONE = "_DONE"
NEW_TRANSPORT_ORDER = "NEW_TO"
SUBSCRIBE_TO_FINISHED_BY = "SUB_FB"
AGV_LOADED = "AGV_LD"
AGV_UNLOADED = "AGV_UD"

logger = logging.getLogger(__name__)


def object_to_json_array(object_to_convert):
    temp_array = []
    temp_array.append(object_to_convert)
    logger.info(json.dumps(temp_array))
    return temp_array

class OptData(object):
    def __init__(self, description, to_id):
        self.description = description
        self.to_id = to_id

class TransportOrder(threading.Thread):
    """ Manages the different states of a TransportOrder and controls the AGVs """
    def __init__(self, uuid_, _refMaterialflowUpdateId, _refOwnerId,
                 queueTransportOrders, task_supervisor_knowledge, broker_ref_id):
        threading.Thread.__init__(self)

        # these attributes representing the materialflow
        self._to_info = None
        self._event_info_triggered_by = None # triggered_by of the task
        self._event_info_finished_by = None # finished_by of the task
        self._wait_for_trigger = False
        self._wait_for_finished_by = False

        # internal attributes
        self.id = str(uuid_)
        self.ref_materialflow_update_id = _refMaterialflowUpdateId
        self.ref_owner_id = _refOwnerId
        self.broker_ref_id = broker_ref_id
        self.start_time = get_utc_time()
        self.task_name = str(uuid_)
        self.state = State.Idle
        self._task_supervisor_knowledge = task_supervisor_knowledge
        self._to_state_machine = TransportOrderStateMachine(
            self.task_name)
        self.agv_is_loaded = False
        self.agv_is_unloaded = False

        # setting up the thread
        self._queue_to_materialflow = queueTransportOrders

        self._task_supervisor_knowledge.ros_message_dispatcher.add_thread(
            self.id)
        self._ros_queue_to = self._task_supervisor_knowledge.ros_message_dispatcher.get_queue(
            self.id)
        self._task_supervisor_knowledge.sensor_dispatcher.add_thread(self.id)
        self._sensor_queue = self._task_supervisor_knowledge.sensor_dispatcher.get_queue(
            self.id)
        self._internal_queue = queue.Queue()

        self._robot = None
        self._robot_id = None
        self._subscription_ids = []

        self._transport_order_update = TransportOrderUpdate(self)
        self._transport_order_update.broker_ref_id = self.broker_ref_id

        self._task_supervisor_knowledge.broker_connector.create(
            self._transport_order_update)

    def wait_for_triggered_by(self, event_information):
        self._wait_for_trigger = True
        self._event_info_triggered_by = event_information
        pass

    def wait_for_finished_by(self, event_information):
        if event_information is None:
            self._wait_for_finished_by = False
            self._event_info_finished_by = None
            self._internal_queue.put(None)
        else:
            self._wait_for_finished_by = True
            self._event_info_finished_by = event_information
            self._internal_queue.put(SUBSCRIBE_TO_FINISHED_BY)

    def load_agv(self):
        self._internal_queue.put(AGV_LOADED)

    def unload_agv(self):
        self._internal_queue.put(AGV_UNLOADED)

    def set_transport_info(self, transport_order):
        self._to_info = transport_order
        if self.is_current_state(TRANSPORT_ORDER_STATES.WAIT_FOR_TRIGGER):
            self._to_state_machine.TriggerReceived()
            self._internal_queue.put(NEW_TRANSPORT_ORDER)

    def is_current_state(self, current_state):
        return self._to_state_machine.current_state_is(current_state)

    def get_subscription_desc(self):
        return self.task_name + "_" + self.id + "_"

    def _clear_subsriptions(self):
        temp_list = list(self._subscription_ids)

        for sub_id in temp_list:
            self._task_supervisor_knowledge.broker_connector.delete(sub_id, self.broker_ref_id, delete_entity=False)
            self._subscription_ids.remove(sub_id)

    def run(self):
        self.state = State.Running
        send_transport_order = True

        select_on_queues = MultiQueue(
            [self._sensor_queue, self._internal_queue])

        while(self._to_state_machine.get_state() != "finished" and self._to_state_machine.get_state() != "error"):
            current_state = self._to_state_machine.state
            if self.is_current_state(TRANSPORT_ORDER_STATES.INIT):
                if self._wait_for_trigger:                    
                    # register for wait for trigger events
                    for wait_for_tb in self._event_info_triggered_by:
                        sensor_agent = SensorAgent(
                            wait_for_tb.physical_name)

                        opt_data = OptData(self.get_subscription_desc() + "WaitForTrigger", self.id)
                        temp_subscription_id = self._task_supervisor_knowledge.broker_connector.subscribe_to_specific(sensor_agent, self.broker_ref_id, opt_data=opt_data)

                        self._subscription_ids.append(temp_subscription_id)
                        self._transport_order_update.state = self._to_state_machine.get_state()
                        self._transport_order_update.task_info = UserAction.WaitForStartTrigger

                        self._task_supervisor_knowledge.broker_connector.update(
                            self._transport_order_update)

                self._to_state_machine.Initialized()

            elif self.is_current_state(TRANSPORT_ORDER_STATES.WAIT_FOR_TRIGGER):
                logger.info("current_state: %s, id: %s, TaskName: %s",
                            current_state, self.id, self.task_name)
                if self._wait_for_trigger:
                    print("WAIT FOR TRIGGER")
                    try:
                        queue_data = select_on_queues.get()[1]
                        if queue_data:
                            if queue_data == NEW_TRANSPORT_ORDER:
                                self._clear_subsriptions()
                                self._transport_order_update.state = self._to_state_machine.get_state()
                                self._transport_order_update.task_info = UserAction.MovingToPickupDestination
                                self._task_supervisor_knowledge.broker_connector.update(
                                    self._transport_order_update)
                                continue
                        sensor_entity_data = queue_data
                        sensor_value = sensor_entity_data.readings[0]["reading"]
                        sensor_physical_name = sensor_entity_data.sensor_id

                        for event_info in self._event_info_triggered_by:
                            if event_info.physical_name == sensor_physical_name:
                                self._queue_to_materialflow.put((self.task_name, Event(
                                    event_info.logical_name, sensor_physical_name, "", "", sensor_value)))
                        print("SEND TO MF")
                    except queue.Empty as arr:
                        logger.error(arr)

                elif not self._wait_for_trigger:
                    self._to_state_machine.TriggerReceived()
                    self._transport_order_update.state = self._to_state_machine.get_state()
                    self._transport_order_update.task_info = UserAction.MovingToPickupDestination
                    self._task_supervisor_knowledge.broker_connector.update(
                        self._transport_order_update)
            elif self.is_current_state(TRANSPORT_ORDER_STATES.START_PICKUP):
                logger.info("current_state: %s, id: %s, TaskName: %s",
                            current_state, self.id, self.task_name)
                try:
                    if send_transport_order:
                        pickup_type = self._to_info.pickup_tos.location.location_type
                        try:
                            self._robot = self._task_supervisor_knowledge.optimizer.get_next_agv_by_type(
                                pickup_type)

                        except RuntimeError:
                            # we had no valid robot, so we have to kill the transport :(
                            self._to_state_machine.TransportOrderError()
                            self._transport_order_update.state = self._to_state_machine.get_state()
                            self._transport_order_update.robot_id = 0
                            self._task_supervisor_knowledge.broker_connector.update(
                                self._transport_order_update)

                            logger.error(
                                "No valid robot selection; Please check TS configuration and Materialflow Description")
                            break

                        self._robot_id = self._robot.id

                        self._robot.control.create_transport_order(str(self._to_info.uuid),
                            self._to_info.pickup_tos.location.physical_name,
                            self._to_info.delivery_tos.location.physical_name)

                        if self._robot.control.status == CREATE_TRANSPORT_ORDER_SUCCESS:
                            # transport order has been send, now we can move on
                            send_transport_order = False

                    ros_packet_order_state = self._ros_queue_to.get(
                        QUEUE_WAIT_TIME_IN_SECONDS)

                    if ros_packet_order_state:
                        #  first lets check if we are really moving
                        temp_uuid = ros_packet_order_state.uuid
                        temp_state = ros_packet_order_state.state
                        if ((temp_state == rosTransportOrderStates.TO_LOAD_MOVE_ORDER_START or temp_state == rosTransportOrderStates.TO_LOAD_MOVE_ORDER_ONGOING) and temp_uuid == self.id and not send_transport_order):
                            logger.info("NewTransportOrder - Robot SHOULD moving" + str(
                                        ros_packet_order_state.status) + ", id: " + self.id)

                            self._to_state_machine.GotoPickupDestination()
                            self._transport_order_update.task_info = UserAction.MovingToPickupDestination
                            self._transport_order_update.state = self._to_state_machine.get_state()
                            self._transport_order_update.robot_id = self._robot_id
                            self._transport_order_update.pickup_from = self._to_info.pickup_tos.location.physical_name
                            self._transport_order_update.deliver_to = self._to_info.delivery_tos.location.physical_name
                            self._task_supervisor_knowledge.broker_connector.update(
                                self._transport_order_update)
                        pass
                except Exception as p:
                    logger.info("startPickup, didnt work")

            elif self.is_current_state(TRANSPORT_ORDER_STATES.MOVING_TO_PICKUP):
                logger.info(current_state + ", id: " +
                            self.id + ", Task: " + self.task_name)
                ros_packet_order_state = self._ros_queue_to.get()

                if ros_packet_order_state:
                    temp_uuid = ros_packet_order_state.uuid 
                    temp_state = ros_packet_order_state.state

                    if temp_state == rosTransportOrderStates.TO_LOAD_MOVE_ORDER_FINISHED and temp_uuid == self.id:
                        # lets check if there is a wait for trigger event
                        if self._to_info.pickup_tos.finished_by: # should be triggered_by not finished_by
                            # subscribe to events

                            sensor_agent = SensorAgent(
                                self._to_info.pickup_tos.finished_by[0].physical_name)

                            opt_data = OptData(self.get_subscription_desc() + "WaitForManualLoading", self.id)
                            temp_subscription_id = self._task_supervisor_knowledge.broker_connector.subscribe_to_specific(sensor_agent, self.broker_ref_id, opt_data=opt_data)

                            self._subscription_ids.append(temp_subscription_id)

                    # agv arrived at the pickup destination
                    elif (temp_state == rosTransportOrderStates.TO_LOAD_ACTION_START or temp_state == rosTransportOrderStates.TO_LOAD_ACTION_ONGOING) and temp_uuid == self.id:
                        self._to_state_machine.ArrivedAtPickupDestination()
                        self._transport_order_update.task_info = UserAction.WaitForLoading
                        self._transport_order_update.state = self._to_state_machine.get_state()

                        self._task_supervisor_knowledge.broker_connector.update(
                            self._transport_order_update)

                        # send info to scheduler
                        self._queue_to_materialflow.put((self.task_name, Event("moved_to_location", "",
                         "Boolean", value=True)))

            elif self.is_current_state(TRANSPORT_ORDER_STATES.WAITING_FOR_LOADING):
                logger.info("current_state: %s, id: %s, TaskName: %s",
                            current_state, self.id, self.task_name)
                if self._to_info.pickup_tos.finished_by:
                    queue_data = select_on_queues.get()[1]
                    if queue_data:
                        if queue_data == NEW_TRANSPORT_ORDER:
                            self._clear_subsriptions()
                            continue
                        elif queue_data == AGV_LOADED:
                             # unsubscribe from events:
                            self._clear_subsriptions() 
                            self._robot.control.manual_action_acknowledge()
                            status = self._robot.control.status
                            # no need to resend it...
                            if status == CREATE_TRANSPORT_ORDER_SUCCESS:
                                self._to_state_machine.AgvIsLoaded()

                                self._transport_order_update.state = self._to_state_machine.get_state()
                                self._task_supervisor_knowledge.broker_connector.update(self._transport_order_update)
                            continue
                    sensor_entity_data = queue_data

                    if not sensor_entity_data.readings:
                        raise ValueError("Given Sensor data contains no reading")

                    sensor_value = sensor_entity_data.readings[0]["reading"]
                    sensor_physical_name = sensor_entity_data.sensor_id
                    for event_info in self._to_info.pickup_tos.finished_by:
                        if event_info.physical_name == sensor_physical_name:
                            self._queue_to_materialflow.put((self.task_name,
                                                             Event(event_info.logical_name, sensor_physical_name,
                                                                   event_info.event_type, "", sensor_value)))
                else:  # automatic loaded is now simulated ;)
                    self._to_state_machine.AgvIsLoaded()

                    self._transport_order_update.state = self._to_state_machine.get_state()
                    self._task_supervisor_knowledge.broker_connector.update(
                        self._transport_order_update)

            elif self.is_current_state(TRANSPORT_ORDER_STATES.START_DELIVERY):
                logger.info("current_state: %s, id: %s, TaskName: %s",
                            current_state, self.id, self.task_name)

                ros_packet_order_state = self._ros_queue_to.get()
                if ros_packet_order_state:
                    #  first lets check if we are really moving
                    temp_uuid = ros_packet_order_state.uuid
                    temp_state = ros_packet_order_state.state

                    if temp_state == rosTransportOrderStates.TO_UNLOAD_MOVE_ORDER_START and temp_uuid == self.id:

                        self._to_state_machine.GotoDeliveryDestination()
                        self._transport_order_update.task_info = UserAction.MovingToDeliveryDestination

                        self._transport_order_update.state = self._to_state_machine.get_state()
                        self._task_supervisor_knowledge.broker_connector.update(
                            self._transport_order_update)

            elif self.is_current_state(TRANSPORT_ORDER_STATES.MOVING_TO_DELIVERY):
                logger.info("current_state: %s, id: %s, TaskName: %s",
                            current_state, self.id, self.task_name)
                ros_packet_order_state = self._ros_queue_to.get()

                if ros_packet_order_state:
                    #  first lets check if we are really moving
                    temp_uuid = ros_packet_order_state.uuid
                    temp_state = ros_packet_order_state.state

                    if temp_state == rosTransportOrderStates.TO_UNLOAD_MOVE_ORDER_FINISHED and temp_uuid == self.id:
                        if self._to_info.delivery_tos.finished_by:
                            # subscribe to events
                            sensor_agent = SensorAgent(
                                self._to_info.delivery_tos.finished_by[0].physical_name)

                            opt_data = OptData(self.get_subscription_desc() + "WaitForManualUNLoading", self.id)
                            temp_subscription_id = self._task_supervisor_knowledge.broker_connector.subscribe_to_specific(sensor_agent, self.broker_ref_id, opt_data=opt_data)

                            self._subscription_ids.append(temp_subscription_id)
                    # agv arrived at the delivery destination
                    elif (temp_state == rosTransportOrderStates.TO_UNLOAD_ACTION_START or temp_state == rosTransportOrderStates.TO_UNLOAD_ACTION_ONGOING) and temp_uuid == self.id:

                        self._to_state_machine.ArrivedAtDeliveryDestination()
                        self._transport_order_update.task_info = UserAction.WaitForUnloading

                        self._transport_order_update.state = self._to_state_machine.get_state()
                        self._task_supervisor_knowledge.broker_connector.update(
                            self._transport_order_update)

                        # send info to scheduler
                        self._queue_to_materialflow.put((self.task_name, Event("moved_to_location", "", "Boolean", value=True)))
                    elif(ros_packet_order_state.status == rosOrderStatus.ERROR or ros_packet_order_state.status == rosOrderStatus.WAITING or ros_packet_order_state.status == rosOrderStatus.UNKNOWN):
                        print(ros_packet_order_state.status)

            elif self.is_current_state(TRANSPORT_ORDER_STATES.WAITING_FOR_UNLOADING):
                logger.info("current_state: %s, id: %s, TaskName: %s",
                            current_state, self.id, self.task_name)
                if self._to_info.delivery_tos.finished_by:
                    queue_data = select_on_queues.get()[1]
                    if queue_data:
                        if queue_data == NEW_TRANSPORT_ORDER:
                            continue
                        elif queue_data == AGV_UNLOADED:
                            self._clear_subsriptions()

                            self._robot.control.manual_action_acknowledge()
                            status = self._robot.control.status

                            if status == CREATE_TRANSPORT_ORDER_SUCCESS:
                                # no need to resend it...
                                self._to_state_machine.AgvIsUnloaded()
                                self._transport_order_update.task_info = UserAction.Idle

                                self._transport_order_update.state = self._to_state_machine.get_state()

                                self._task_supervisor_knowledge.broker_connector.update(
                                    self._transport_order_update)
                            continue

                    sensor_entity_data = queue_data

                    sensor_value = sensor_entity_data.readings[0]["reading"]
                    sensor_physical_name = sensor_entity_data.sensor_id

                    for event_info in self._to_info.delivery_tos.finished_by:
                        if event_info.physical_name == sensor_physical_name:
                            self._queue_to_materialflow.put((self.task_name, Event(event_info.logical_name,
                                                                                   sensor_physical_name,
                                                                                   event_info.event_type,
                                                                                   "", sensor_value)))
                else:
                    self._to_state_machine.AgvIsUnloaded()
                pass
            elif self.is_current_state(TRANSPORT_ORDER_STATES.WAIT_FOR_FINISHED):
                logger.info("current_state: %s, id: %s, TaskName: %s",
                            current_state, self.id, self.task_name)
                queue_data = select_on_queues.get()[1]
                if queue_data is None:
                    self._to_state_machine.FinishedReceived()
                elif queue_data == SUBSCRIBE_TO_FINISHED_BY:
                    queue_data = None
                    logger.info("subscribe to events")
                    for wait_for_fb in self._event_info_finished_by:
                        sensor_agent = SensorAgent(
                            wait_for_fb.physical_name)

                        opt_data = OptData(self.get_subscription_desc() + "WaitForFinishedBy", self.id)
                        temp_subscription_id = self._task_supervisor_knowledge.broker_connector.subscribe_to_specific(sensor_agent, self.broker_ref_id, opt_data=opt_data)

                        self._subscription_ids.append(temp_subscription_id)
                    self._to_state_machine.SubscribedToFinishedEvents()
                    self._transport_order_update.task_info = UserAction.WaitForFinishTrigger

                    self._transport_order_update.state = self._to_state_machine.get_state()

                    self._task_supervisor_knowledge.broker_connector.update(
                        self._transport_order_update)

            elif self.is_current_state(TRANSPORT_ORDER_STATES.WAIT_FOR_FINISHED_EVENTS):
                logger.info("current_state: %s, id: %s, TaskName: %s",
                            current_state, self.id, self.task_name)
                if self._event_info_finished_by:
                    queue_data = select_on_queues.get()[1]
                    if queue_data is None:
                        self._to_state_machine.FinishedTriggerReceived()
                        break
                    sensor_entity_data = queue_data
                    sensor_value = sensor_entity_data.readings[0]["reading"]
                    sensor_physical_name = sensor_entity_data.sensor_id

                    for event_info in self._event_info_finished_by:
                        if event_info.physical_name == sensor_physical_name:
                            self._queue_to_materialflow.put((self.task_name, Event(
                                event_info.logical_name, sensor_physical_name, "", "", sensor_value)))
                    print("SEND TO MF")
                else:
                    self._to_state_machine.FinishedTriggerReceived()

            elif self.is_current_state(TRANSPORT_ORDER_STATES.FINISHED):
                logger.info("current_state: %s, id: %s, TaskName: %s",
                            current_state, self.id, self.task_name)
                break

        # its time to clean up
        logger.info("END_OF_TransportOrder: %s", self.id)
        select_on_queues.finish()
        self._clear_subsriptions()

        self._task_supervisor_knowledge.broker_connector.delete(self._transport_order_update.id, self.broker_ref_id)

        self._task_supervisor_knowledge.ros_message_dispatcher.remove_thread(
            self.id)
        self._task_supervisor_knowledge.sensor_dispatcher.remove_thread(self.id)
