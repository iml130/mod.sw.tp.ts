""" Contains AgvManager class """

import threading

from tasksupervisor.control.agv import AGV
from tasksupervisor.control.ros_interface import RosControl

class AgvManager():
    """
        Provides methods for managing AGVs:
            - add agv
            - get agv by different conditions
    """
    lock = threading.Lock()

    def __init__(self, robot_ids, robot_names, robot_types):
        self.available_agvs = {}
        if len(robot_types) != len(robot_ids) != len(robot_names):
            raise ValueError("Invalid length of parameter")

        for index in range(len(robot_ids)):
            self.add_agv(robot_ids[index], robot_names[index], robot_types[index])

    def add_agv(self, robot_id, robot_name, robot_type):
        with self.lock:
            if not robot_id in self.available_agvs:
                self.available_agvs[robot_id] = AGV(robot_id, robot_name, robot_type)
                self.available_agvs[robot_id].set_control(RosControl(robot_id))

    def get_agv_by_id(self, robot_id):
        with self.lock:
            if robot_id in self.available_agvs:
                return self.available_agvs[robot_id]
            return None

    def get_agvs_by_type(self, robot_type):
        with self.lock:
            list_of_agvs = []
            for item in self.available_agvs.values():
                if item.type == robot_type:
                    list_of_agvs.append(item)
            return list_of_agvs

    def get_agv_types(self):
        agv_types = []
        with self.lock:
            for item in self.available_agvs.values():
                if not item.type in agv_types:
                    agv_types.append(item.type)
            return agv_types
