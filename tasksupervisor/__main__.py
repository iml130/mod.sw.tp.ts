import json
import logging
import logging.config
import os
import signal
import sys
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
from tasksupervisor.flask_setup import create_flask_app
from tasksupervisor.task_supervisor_knowledge import TaskSupervisorKnowledge
from tasksupervisor.entities import materialflow
from tasksupervisor.entities.materialflow_specification_state import MaterialflowSpecificationState
from tasksupervisor.entities.task_supervisor_info import TaskSupervisorInfo
# from helpers.config import Config
from tasksupervisor.helpers import servercheck
from tasksupervisor.control.ros_order_state import OrderState, rosOrderStatus

# from tasksupervisor.optimization.round_robin import initRobot
from tasksupervisor.TaskSupervisor.scheduler import Scheduler

from tasksupervisor.control.agv_manager import AgvManager
from tasksupervisor.optimization.round_robin import RoundRobin


def setup_logging(
        default_path='./tasksupervisor/logging.json',
        default_level=logging.INFO,
        env_key='LOG_CFG'):
    """Setup logging configuration """
    path = default_path
    value = os.getenv(env_key, None)

    if value:
        path = value
    if os.path.exists("./tasksupervisor/logging.json"):
        with open(path, 'rt') as local_f:
            config = json.load(local_f)
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)


# reconnect logging calls which are children of this to the ros log system
setup_logging()
logger = logging.getLogger(__name__)


# initRobot(my_globals.parsed_config_file.robotTypes,
#           my_globals.parsed_config_file.robots, my_globals.parsed_config_file.robotNames)

# if my_globals.parsed_config_file.TASKPLANNER_HOST:
#     PORT = int(my_globals.parsed_config_file.TASKPLANNER_PORT)

ORION_CONNECTOR = my_globals.ORION_CONNECTOR

active_materialflow_specification_states = []
active_task_schedulers = []
# currentMaterialFlowSpecState = MaterialflowSpecificationState()
entity_task_supervisor_info = TaskSupervisorInfo()

# todos:
# updating the task id; actually HMI sets a task and the taskState represents a task
# taskLanguage
# stateMachine should be in charge of the states and dealing with the event; internal pub/sub mechanism
# shift method 'delete_subscription_by_id' to the context-broker; internal subscription_id_materialflow handler
# storage of subscriptions in a database, when starting the programm what to do with subscriptions (deleting? Adding a new name to it?);
# ending/exiting programm either by typing 'exit' or pushing ctrl-c


class GracefulKiller:
    """ A helper class to wait for a ctrl+c user input  """
    kill_now = False

    def __init__(self):
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    def exit_gracefully(self, signum, frame):
        self.kill_now = True


def callback_flask_server(task_supervisor):
    """ Callback method to create for the flask server """
    logger.info("Starting thread_flask_server")
    app = create_flask_app(task_supervisor)
    app.run(host=my_globals.parsed_config_file.FLASK_HOST,
            port=my_globals.parsed_config_file.TASKPLANNER_PORT, threaded=True, use_reloader=False, debug=True)


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

        entity_task_supervisor_info.appendMaterialflow(
            materialflow_specification.id)

        task_supervisor.orion_connector.update_entity(
            entity_task_supervisor_info)
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
        json_requests, entity_type = queue_materialflow_spec.get()
        with lock:
            if entity_type == "Materialflow":
                # it might be possible that there are multiple entities
                # iterate over each json request
                for temp_json_request in json_requests:
                    new_mf_specification_state = MaterialflowSpecificationState()

                    # create an entity from the json request
                    new_materialflow = materialflow.Materialflow.CreateObjectFromJson(
                        temp_json_request)

                    # check if the materialflow shall be processed - or not
                    if new_materialflow.active:
                        try:
                            lotlan_validator = LotlanScheduler(
                                new_materialflow.specification)
                            materialflow_is_valid = lotlan_validator.validate(
                                new_materialflow.specification)
                            if materialflow_is_valid:
                                new_materialflow._specStateId = new_mf_specification_state.getId()  # ????
                                logger.info("newTaskSpec:\n %s",
                                            str(new_materialflow.specification))
                                
                                new_mf_specification_state.message = "Valid"
                                new_mf_specification_state.state = materialflow_is_valid
                                new_mf_specification_state.refId = temp_json_request["id"]
                                my_globals.taskSchedulerQueue.put(new_materialflow)
                        except ValueError as p:
                            materialflow_is_valid = -1
                            logger.info("Materialflow specification error")
                            new_mf_specification_state.message = urllib.parse.quote_plus(str(p))
                            new_mf_specification_state.state = materialflow_is_valid
                            new_mf_specification_state.refId = temp_json_request["id"]


                        materialflow_is_valid = task_supervisor.orion_connector.create_entity(new_mf_specification_state)
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
        # ORION_CONNECTOR.update_entity(currentMaterialFlowSpecState)

    logger.info("callback_new_materialflow ended")


def callback_ros_order_state(data, ros_queue):
    """ Callback for ros order state
    """
    # rospy.loginfo(data.order_id)
    order_state = OrderState.CreateObjectRosMsg(data)
    # logger.info("uuid: " + str(os.uuid) + ", state: " + str(os.state) +", status:" +  str(os.status))
    if order_state:
        if order_state.status == rosOrderStatus.FINISHED:
            logger.info("Received callback_ros_order_state --> FIN")
        ros_queue.put_data(order_state.uuid, order_state)


if __name__ == '__main__':
    logger.info("Subscriptions to /order_status")
    logger.info("Setting up ROS")

    task_supervisor = TaskSupervisorKnowledge()
    task_supervisor.agv_manager = AgvManager(
        my_globals.parsed_config_file.robots, my_globals.parsed_config_file.robotNames, my_globals.parsed_config_file.robotTypes)
    task_supervisor.optimizer = RoundRobin(task_supervisor.agv_manager)
    task_supervisor.orion_connector = ORION_CONNECTOR
    task_supervisor.task_planner_address = my_globals.parsed_config_file.get_taskplanner_address()

    # initialize rospy
    rospy.init_node('task_supervisor')
    rospy.Subscriber("/order_status", OrderStatus,
                     callback_ros_order_state, task_supervisor.ros_message_dispatcher)

    setup_logging()

    logger.info("Starting TaskPlanner %i", 4)
    if os.path.isfile('./images/task.png'):
        os.remove('./images/task.png')

    logger.info("Setting up thread_check_if_server_is_up")
    thread_check_if_server_is_up = threading.Thread(name='checkServerRunning',
                                                    target=servercheck.webserver_is_running,
                                                    args=("localhost", my_globals.parsed_config_file.TASKPLANNER_PORT,))

    logger.info("Setting up checkForProgrammEnd")
    # checkForProgrammEnd = threading.Thread(name='waitForEnd',
    #                                             target=waitForEnd,
    #                                             args=())

    logger.info("Setting up thread_flask_server")
    thread_flask_server = threading.Thread(
        name='callback_flask_server', target=callback_flask_server, args=(task_supervisor,))

    thread_check_if_server_is_up.start()

    thread_flask_server.start()
    logger.info("Starting Flask and wait")
    thread_check_if_server_is_up.join()
    logger.info("Flask is running")
    # create an instance of the fiware ocb handler

    # few things commented due to the damn airplane mode
    # publish first the needed entities before subscribing ot it
    return_value = ORION_CONNECTOR.create_entity(entity_task_supervisor_info)
    if return_value == 0:
        logger.info(
            "Orion Connection is working - created TaskSpecState Entity")
        logger.info("Orion Address: " +
                    my_globals.parsed_config_file.get_fiware_server_address())
    else:
        logger.error("No Connection to Orion - please check configurations")
        sys.exit(0)

    logger.info("Setting up callback_new_materialflow and workTaskScheduler")
    thread_new_materialflow = Thread(target=callback_new_materialflow,
                                     args=(my_globals.taskQueue, task_supervisor))
    thread_new_materialflow_scheduler = Thread(
        target=callback_task_scheduler_creator, args=(my_globals.taskSchedulerQueue, task_supervisor))

    logger.info(
        "Starting callback_new_materialflow, sanDealer and workTaskScheduler")
    thread_new_materialflow.start()
    thread_new_materialflow_scheduler.start()

    materialflow_entity = materialflow.Materialflow()
    with my_globals.lock:
        subscription_id_materialflow = ORION_CONNECTOR.subscribe_to_entity(_description="Materialflow subscription",
                                                                           _entities=materialflow_entity.obj2JsonArray(),
                                                                           _notification=my_globals.parsed_config_file.get_taskplanner_address() + "/materialflow", _generic=True)
        task_supervisor.subscription_dict[subscription_id_materialflow] = "Materialflow"

    logger.info("Push Ctrl+C to exit()")

    wait_for_user_end = GracefulKiller()
    while not wait_for_user_end.kill_now:
        time.sleep(1)

    # clean up means, delete
    #   - all subscriptions
    #   - all created entities

    logger.info("Shutting down TaskPlanner")
    logger.info("Unsubscribing from Subscriptions")
    # TODO: error with threads, size of dict might change:
    # better: get keys and iterate overy keys
    for temp_subription_id in task_supervisor.subscription_dict:
        ORION_CONNECTOR.delete_subscription_by_id(temp_subription_id)

    logger.info("Unsubscribing from Subscriptions_done")

    logger.info("Deleting all created Entities")
    ORION_CONNECTOR.shutdown()
    logger.info("Deleting all created Entities_done")

    logger.info("EndOf TaskPlanner")
    os._exit(0)
