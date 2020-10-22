"""
    This class is a beast. Within this class, a TransportOrder (TO) is assigned to an AGV (for now ;)).
    But the selection of an AGV is done once it is needed.
"""
import threading
import logging
import json
import queue

from lotlan_schedular.api.event import Event


from tasksupervisor.entities.sensor_agent_node import SensorAgent

from tasksupervisor.control.ros_order_state import rosOrderStatus, rosTransportOrderStates
from tasksupervisor.control.ros_interface import RosControl

from tasksupervisor.entities.transport_order_update import TransportOrderUpdate

from tasksupervisor.TaskSupervisor.transport_order_state_machine import TransportOrderStateMachine
from tasksupervisor.TaskSupervisor.transport_order_state_machine import TRANSPORT_ORDER_STATES

from tasksupervisor.TaskSupervisor.taskState import State
from tasksupervisor.helpers.utc import get_utc_time
from tasksupervisor.TaskSupervisor.trigger_validator import checkIfSensorEventTriggersNextTransportUpdate
from tasksupervisor.TaskSupervisor.trigger_validator import get_sensor_value
from tasksupervisor.TaskSupervisor.trigger_validator import get_sensor_physical_sensor_name


from tasksupervisor.TaskSupervisor.multiq import multi_queue
from tasksupervisor.TaskSupervisor.user_action import UserAction


# defines
ROS_CALL_ERROR = -1
CREATE_TRANSPORT_ORDER_SUCCESS = 0
QUEUE_WAIT_TIME_IN_SECONDS = 5
TRANSPORT_ODER_DONE = "_DONE"
NEW_TRANSPORT_ORDER = "NEW_TO"
SUBSCRIBE_TO_FINISHED_BY = "SUB_FB"

logger = logging.getLogger(__name__)


def object_to_json_array(object_to_convert):
    temp_array = []
    temp_array.append(object_to_convert)
    logger.info(json.dumps(temp_array))
    return temp_array


class TransportOrder(threading.Thread):
    def __init__(self, _uuid, _refMaterialflowUpdateId, _refOwnerId, queueTransportOrders, task_supervisor_knowledge):
        threading.Thread.__init__(self)

        # these attributes representing the materialflow
        self._to_info = None
        self._event_info_triggered_by = None
        self._event_info_finished_by = None
        self._wait_for_trigger = False
        self._wait_for_finished_by = False

        # internal attributes
        self.id = str(_uuid)
        self.ref_materialflow_update_id = _refMaterialflowUpdateId
        self.ref_owner_id = _refOwnerId
        self.start_time = get_utc_time()
        self.task_name = str(_uuid)
        self.state = State.Idle
        self._task_supervisor_knowledge = task_supervisor_knowledge
        self._to_state_machine = TransportOrderStateMachine(
            self.task_name)

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


        self._task_supervisor_knowledge.orion_connector.create_entity(
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
            self._task_supervisor_knowledge.orion_connector.delete_subscription_by_id(
                sub_id)
            self._subscription_ids.remove(sub_id)
            del self._task_supervisor_knowledge.subscription_dict[sub_id]

    def run(self):
        self.state = State.Running
        send_transport_order = True

        select_on_queues = multi_queue(
            [self._sensor_queue, self._internal_queue])

        while(self._to_state_machine.get_state() != "finished" and self._to_state_machine.get_state() != "error"):
            current_state = self._to_state_machine.state
            if self.is_current_state(TRANSPORT_ORDER_STATES.INIT):
                if self._wait_for_trigger:                    
                    # register for wait for trigger events
                    for wait_for_tb in self._event_info_triggered_by:
                        sensor_agent = SensorAgent(
                            wait_for_tb.physical_name)
                        temp_subscription_id = self._task_supervisor_knowledge.orion_connector.subscribe_to_entity(_description=self.get_subscription_desc(
                        ) + "WaitForTrigger",  _entities=object_to_json_array(sensor_agent.getEntity()), _notification=self._task_supervisor_knowledge.task_planner_address + "/san/" + self.id)
                        self._task_supervisor_knowledge.subscription_dict[temp_subscription_id] = self.id
                        self._subscription_ids.append(temp_subscription_id)
                        self._transport_order_update.state = self._to_state_machine.get_state()
                        self._transport_order_update.taskInfo = UserAction.WaitForStartTrigger
                        self._transport_order_update.update_time()
                        self._task_supervisor_knowledge.orion_connector.update_entity(
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
                                self._transport_order_update.taskInfo = UserAction.MovingToPickupDestination
                                self._transport_order_update.update_time()
                                self._task_supervisor_knowledge.orion_connector.update_entity(
                                    self._transport_order_update)
                                continue
                        sensor_entity_data = queue_data
                        sensor_value = get_sensor_value(
                            sensor_entity_data, self._subscription_ids)
                        sensor_physical_name = get_sensor_physical_sensor_name(
                            sensor_entity_data, self._subscription_ids)

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
                    self._transport_order_update.taskInfo = UserAction.MovingToPickupDestination
                    self._transport_order_update.update_time()
                    self._task_supervisor_knowledge.orion_connector.update_entity(
                        self._transport_order_update)
            elif self.is_current_state(TRANSPORT_ORDER_STATES.START_PICKUP):
                logger.info("current_state: %s, id: %s, TaskName: %s",
                            current_state, self.id, self.task_name)
                try:
                    if send_transport_order:
                        pickup_type = self._to_info.to_step_from.location.location_type
                        try:
                            self._robot = self._task_supervisor_knowledge.optimizer.get_next_agv_by_type(
                                pickup_type)

                        except RuntimeError:
                            # we had no valid robot, so we have to kill the transport :(
                            self._to_state_machine.TransportOrderError()
                            self._transport_order_update.state = self._to_state_machine.get_state()
                            self._transport_order_update.robotId = 0
                            self._transport_order_update.update_time()
                            self._task_supervisor_knowledge.orion_connector.update_entity(
                                self._transport_order_update)

                            logger.error(
                                "No valid robot selection; Please check TS configuration and Materialflow Description")
                            break

                        self._robot_id = self._robot.id

                        ros_transport = RosControl()

                        # create the real transport order
                        ros_transport.create_transport_order(
                            str(self._to_info.uuid),
                            self._to_info.to_step_from.location.physical_name,
                            self._to_info.to_step_to.location.physical_name,
                            self._robot_id)

                        if ros_transport.status == CREATE_TRANSPORT_ORDER_SUCCESS:
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
                            self._transport_order_update.taskInfo = UserAction.MovingToPickupDestination
                            self._transport_order_update.state = self._to_state_machine.get_state()
                            self._transport_order_update.robotId = self._robot_id
                            self._transport_order_update.pickupFrom = self._to_info.to_step_from.location.physical_name
                            self._transport_order_update.deliverTo = self._to_info.to_step_to.location.physical_name
                            self._transport_order_update.update_time()
                            self._task_supervisor_knowledge.orion_connector.update_entity(
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
                        if self._to_info.to_step_from.finished_by:
                            # subscribe to events

                            sensor_agent = SensorAgent(
                                self._to_info.to_step_from.finished_by[0].physical_name)
                            temp_subscription_id = self._task_supervisor_knowledge.orion_connector.subscribe_to_entity(_description=self.get_subscription_desc(
                            ) + "WaitForManualLoading", _entities=object_to_json_array(sensor_agent.getEntity()), _notification=self._task_supervisor_knowledge.task_planner_address + "/san/" + self.id)
                            self._task_supervisor_knowledge.subscription_dict[
                                temp_subscription_id] = self.id
                            self._subscription_ids.append(temp_subscription_id)

                    elif (temp_state == rosTransportOrderStates.TO_LOAD_ACTION_START or temp_state == rosTransportOrderStates.TO_LOAD_ACTION_ONGOING) and temp_uuid == self.id:
                        self._to_state_machine.ArrivedAtPickupDestination()
                        self._transport_order_update.taskInfo = UserAction.WaitForLoading
                        self._transport_order_update.state = self._to_state_machine.get_state()
                        self._transport_order_update.update_time()
                        self._task_supervisor_knowledge.orion_connector.update_entity(
                            self._transport_order_update)

            elif self.is_current_state(TRANSPORT_ORDER_STATES.WAITING_FOR_LOADING):
                logger.info("current_state: %s, id: %s, TaskName: %s",
                            current_state, self.id, self.task_name)
                if self._to_info.to_step_from.finished_by:
                    queue_data = select_on_queues.get()[1]
                    if queue_data:
                        if queue_data == NEW_TRANSPORT_ORDER:
                            self._clear_subsriptions()
                            continue
                    sensor_entity_data = queue_data

                    if sensor_entity_data["subscriptionId"] not in self._subscription_ids:
                        continue
                    expected_value = self._to_info.to_step_from.finished_by[0].value
                    expected_type = self._to_info.to_step_from.finished_by[0].event_type
                    expected_comperator = self._to_info.to_step_from.finished_by[0].comparator
                    agv_is_loaded = checkIfSensorEventTriggersNextTransportUpdate(
                        sensor_entity_data, self._subscription_ids, expected_value, expected_type, expected_comperator)
                    if agv_is_loaded:
                        # unsubscribe from events:
                        self._clear_subsriptions()
                        ros_control = RosControl()
                        status = ros_control.manual_action_acknowledge(
                            self._robot_id)
                        # no need to resend it...
                        if status == CREATE_TRANSPORT_ORDER_SUCCESS:

                            self._to_state_machine.AgvIsLoaded()
                            self._transport_order_update.update_time()
                            self._transport_order_update.state = self._to_state_machine.get_state()
                            self._task_supervisor_knowledge.orion_connector.update_entity(
                                self._transport_order_update)

                else:  # automatic loaded is now simulated ;)
                    self._to_state_machine.AgvIsLoaded()
                    self._transport_order_update.update_time()
                    self._transport_order_update.state = self._to_state_machine.get_state()
                    self._task_supervisor_knowledge.orion_connector.update_entity(
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
                        self._transport_order_update.taskInfo = UserAction.MovingToDeliveryDestination
                        self._transport_order_update.update_time()
                        self._transport_order_update.state = self._to_state_machine.get_state()
                        self._task_supervisor_knowledge.orion_connector.update_entity(
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
                        if self._to_info.to_step_to.finished_by:
                            # subscribe to events
                            sensor_agent = SensorAgent(
                                self._to_info.to_step_to.finished_by[0].physical_name)
                            temp_subscription_id = self._task_supervisor_knowledge.orion_connector.subscribe_to_entity(_description=self.get_subscription_desc(
                            ) + "WaitForManualUNLoading", _entities=object_to_json_array(sensor_agent.getEntity()), _notification=self._task_supervisor_knowledge.task_planner_address + "/san/" + self.id)
                            self._task_supervisor_knowledge.subscription_dict[
                                temp_subscription_id] = self.id
                            self._subscription_ids.append(temp_subscription_id)
                    elif (temp_state == rosTransportOrderStates.TO_UNLOAD_ACTION_START or temp_state == rosTransportOrderStates.TO_UNLOAD_ACTION_ONGOING) and temp_uuid == self.id:

                        self._to_state_machine.ArrivedAtDeliveryDestination()
                        self._transport_order_update.taskInfo = UserAction.WaitForUnloading
                        self._transport_order_update.update_time()
                        self._transport_order_update.state = self._to_state_machine.get_state()
                        self._task_supervisor_knowledge.orion_connector.update_entity(
                            self._transport_order_update)
                    elif(ros_packet_order_state.status == rosOrderStatus.ERROR or ros_packet_order_state.status == rosOrderStatus.WAITING or ros_packet_order_state.status == rosOrderStatus.UNKNOWN):
                        print(ros_packet_order_state.status)

            elif self.is_current_state(TRANSPORT_ORDER_STATES.WAITING_FOR_UNLOADING):
                logger.info("current_state: %s, id: %s, TaskName: %s",
                            current_state, self.id, self.task_name)
                if self._to_info.to_step_to.finished_by:
                    queue_data = select_on_queues.get()[1]
                    if queue_data:
                        if queue_data == NEW_TRANSPORT_ORDER:
                            continue
                    sensor_entity_data = queue_data
                    # sensor_entity_data = self._sensor_queue.get()
                    if sensor_entity_data["subscriptionId"] not in self._subscription_ids:
                        continue
                    expected_value = self._to_info.to_step_to.finished_by[0].value
                    expected_type = self._to_info.to_step_to.finished_by[0].event_type
                    expected_comperator = self._to_info.to_step_to.finished_by[0].comparator
                    agv_is_unloaded = checkIfSensorEventTriggersNextTransportUpdate(
                        sensor_entity_data, self._subscription_ids, expected_value, expected_type, expected_comperator)
                    if agv_is_unloaded:
                        self._clear_subsriptions()

                        ros_control = RosControl()
                        status = ros_control.manual_action_acknowledge(
                            self._robot_id)

                        if status == CREATE_TRANSPORT_ORDER_SUCCESS:
                            # no need to resend it...
                            self._to_state_machine.AgvIsUnloaded()
                            self._transport_order_update.taskInfo = UserAction.Idle
                            self._transport_order_update.update_time()
                            self._transport_order_update.state = self._to_state_machine.get_state()

                            self._task_supervisor_knowledge.orion_connector.update_entity(
                                self._transport_order_update)

                            self._queue_to_materialflow.put(
                                (self.task_name, None))
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
                        temp_subscription_id = self._task_supervisor_knowledge.orion_connector.subscribe_to_entity(_description=self.get_subscription_desc(
                        ) + "WaitForFinishedBy", _entities=object_to_json_array(sensor_agent.getEntity()), _notification=self._task_supervisor_knowledge.task_planner_address + "/san/" + self.id)
                        self._task_supervisor_knowledge.subscription_dict[temp_subscription_id] = self.id
                        self._subscription_ids.append(temp_subscription_id)
                    self._to_state_machine.SubscribedToFinishedEvents()
                    self._transport_order_update.taskInfo = UserAction.WaitForFinishTrigger
                    self._transport_order_update.update_time()
                    self._transport_order_update.state = self._to_state_machine.get_state()

                    self._task_supervisor_knowledge.orion_connector.update_entity(
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
                    sensor_value = get_sensor_value(
                        sensor_entity_data, self._subscription_ids)
                    sensor_physical_name = get_sensor_physical_sensor_name(
                        sensor_entity_data, self._subscription_ids)

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

        self._task_supervisor_knowledge.orion_connector.delete_entity(
            self._transport_order_update.getId())

        self._task_supervisor_knowledge.ros_message_dispatcher.remove_thread(
            self.id)
        self._task_supervisor_knowledge.sensor_dispatcher.remove_thread(self.id)
