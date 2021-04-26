""" Contains TaskSupervisorKnowledge class """

import threading

from tasksupervisor.helpers.dict_queue import DictQueue

class TaskSupervisorKnowledge():
    """ Data class which holds important objects for classes in the Supervisor """
    lock = threading.Lock()
    def __init__(self):
        self.agv_manager = None
        self.optimizer = None
        self.broker_connector = None
        self.task_planner_address = None

        self.sensor_dispatcher = DictQueue()
        self.ros_message_dispatcher = DictQueue()
