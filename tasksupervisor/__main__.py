""" Contains the main module of the TaskSupervisor """

import json
import logging
import logging.config
import os
import signal
import threading
import time
import urllib
from threading import Thread

# external third party imports
import rospy
from mars_agent_logical_msgs.msg import OrderStatus
from lotlan_scheduler.scheduler import LotlanScheduler

# local imports
from tasksupervisor import my_globals
from tasksupervisor.task_supervisor_knowledge import TaskSupervisorKnowledge

from tasksupervisor.api.materialflow import Materialflow
from tasksupervisor.api.materialflow_specification_state import MaterialflowSpecificationState
from tasksupervisor.api.tasksupervisor_info import TaskSupervisorInfo
# from helpers.config import Config
from tasksupervisor.control.ros_order_state import OrderState, rosOrderStatus

# from tasksupervisor.optimization.round_robin import initRobot
from tasksupervisor.TaskSupervisor.scheduler import Scheduler

from tasksupervisor.control.agv_manager import AgvManager
from tasksupervisor.optimization.round_robin import RoundRobin

from tasksupervisor.endpoint.broker_connector import BrokerConnector
from tasksupervisor.endpoint.fiware_orion.orion_interface import OrionInterface

def setup_logging(default_path="./tasksupervisor/logging.json", default_level=logging.INFO, env_key="LOG_CFG"):
    """Setup logging configuration """
    path = default_path
    value = os.getenv(env_key, None)

    if value:
        path = value
    if os.path.exists("./tasksupervisor/logging.json"):
        with open(path, "rt") as local_f:
            config = json.load(local_f)
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)


# reconnect logging calls which are children of this to the ros log system
setup_logging()
logger = logging.getLogger(__name__)

active_materialflow_specification_states = []
active_task_schedulers = []

entity_task_supervisor_info = TaskSupervisorInfo()

class GracefulKiller:
    """ A helper class to wait for a ctrl+c user input  """
    kill_now = False

    def __init__(self):
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    def exit_gracefully(self, signum, frame):
        self.kill_now = True

def callback_task_scheduler_creator(queue_task_scheduler, task_supervisor):
    """ Callback method for creating a new task scheduler

    Keyword arguments:
        queue_task_scheduler -- a queue which gets a valid materialflow description
    """
    global entity_task_supervisor_info
    global active_task_schedulers
    logger.info("SchedulerDealer started")

    while True:
        task_scheduler = None
        # wait for a new materialflow
        materialflow_specification = queue_task_scheduler.get()

        # create new task shedular
        task_scheduler = Scheduler(materialflow_specification, task_supervisor)

        active_task_schedulers.append(task_scheduler)
        task_scheduler.start()

        entity_task_supervisor_info.append_materialflow(materialflow_specification.id)

        task_supervisor.broker_connector.update(entity_task_supervisor_info)
        logger.info("New TaskScheduler added")

    logger.info("SchedulerDealer ended")


def callback_new_materialflow(queue_materialflow_spec, task_supervisor):
    """ Callback method for validating a new materialflow description

    Keyword arguments:
        queue_materialflow_spec -- a queue which gets a new materialflow description
    """
    lock = threading.Lock()

    global active_materialflow_specification_states
    global active_task_schedulers

    logger.info("callback_new_materialflow started")
    while True:
        new_materialflow, entity_type = queue_materialflow_spec.get()
        with lock:
            if entity_type == "Materialflow":
                new_mf_specification_state = MaterialflowSpecificationState()

                # check if the materialflow shall be processed - or not
                if new_materialflow.active:
                    try:
                        lotlan_validator = LotlanScheduler(
                            new_materialflow.specification)
                        materialflow_is_valid = lotlan_validator.validate(
                            new_materialflow.specification)
                        if materialflow_is_valid:
                            logger.info("newTaskSpec:\n %s",
                                        str(new_materialflow.specification))

                            new_mf_specification_state.message = "Valid"
                            new_mf_specification_state.state = materialflow_is_valid
                            new_mf_specification_state.refId = new_materialflow.id
                            new_mf_specification_state.broker_ref_id = new_materialflow.broker_ref_id
                            my_globals.taskSchedulerQueue.put(new_materialflow)
                    except ValueError as p:
                        materialflow_is_valid = -1
                        logger.info("Materialflow specification error")
                        new_mf_specification_state.message = urllib.parse.quote_plus(str(p))
                        new_mf_specification_state.state = materialflow_is_valid
                        new_mf_specification_state.refId = new_materialflow.id


                    materialflow_is_valid = task_supervisor.broker_connector.create(new_mf_specification_state)
                    if materialflow_is_valid == 0:
                        active_materialflow_specification_states.append(
                            new_mf_specification_state)
                else:
                    # materialflow has been set passive
                    # disable the inactive ones
                    for scheduler in active_task_schedulers:
                        if scheduler.id == new_materialflow.id:
                            print("SET INACTIVE: " + scheduler.id)
                            scheduler.set_active(False)
                    print(
                        "TODO: Disable the Materialflow or ignore it...but first... lets make it easy")

    logger.info("callback_new_materialflow ended")


def callback_ros_order_state(data, ros_queue):
    """ Callback for ros order state """
    order_state = OrderState.CreateObjectRosMsg(data)

    if order_state:
        if order_state.status == rosOrderStatus.FINISHED:
            logger.info("Received callback_ros_order_state --> FIN")
        ros_queue.put_data(order_state.uuid, order_state)


if __name__ == "__main__":
    logger.info("Subscriptions to /order_status")
    logger.info("Setting up ROS")

    task_supervisor = TaskSupervisorKnowledge()
    task_supervisor.agv_manager = AgvManager(my_globals.parsed_config_file.robots,
                                             my_globals.parsed_config_file.robot_names,
                                             my_globals.parsed_config_file.robot_types)
    task_supervisor.optimizer = RoundRobin(task_supervisor.agv_manager)
    task_supervisor.task_planner_address = my_globals.parsed_config_file.get_taskplanner_address()

    # initialize rospy
    rospy.init_node("task_supervisor")
    rospy.Subscriber("/order_status", OrderStatus,
                     callback_ros_order_state, task_supervisor.ros_message_dispatcher)

    setup_logging()

    logger.info("Starting TaskPlanner %i", 4)
    if os.path.isfile("./images/task.png"):
        os.remove("./images/task.png")

    broker_connector = BrokerConnector(task_supervisor)
    task_supervisor.broker_connector = broker_connector

    # create and register interface instances here
    orion_interface = OrionInterface(broker_connector, "Orion Context Broker Instance_1")
    broker_connector.register_interface(orion_interface)

    orion_interface.start_interface()

    broker_connector.create(entity_task_supervisor_info)

    logger.info("Setting up callback_new_materialflow and workTaskScheduler")
    thread_new_materialflow = Thread(target=callback_new_materialflow,
                                     args=(my_globals.taskQueue, task_supervisor))
    thread_new_materialflow_scheduler = Thread(target=callback_task_scheduler_creator,
                                               args=(my_globals.taskSchedulerQueue, task_supervisor))

    logger.info("Starting callback_new_materialflow, sanDealer and workTaskScheduler")
    thread_new_materialflow.start()
    thread_new_materialflow_scheduler.start()

    new_materialflow = Materialflow()
    task_supervisor.broker_connector.subscribe_to_specific(new_materialflow, orion_interface.broker_id, generic=True)

    logger.info("Push Ctrl+C to exit()")

    wait_for_user_end = GracefulKiller()
    while not wait_for_user_end.kill_now:
        time.sleep(1)

    # clean up means, delete
    #   - all subscriptions
    #   - all created entities

    logger.info("Shutting down TaskPlanner")
    logger.info("Unsubscribing from Subscriptions and deleting all created Entities")

    broker_connector.shutdown()

    logger.info("Unsubscribing from Subscriptions and deleting all created Entities done")
    logger.info("EndOf TaskPlanner")
    os._exit(0)
