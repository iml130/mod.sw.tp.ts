import threading

from tasksupervisor.control.agv import AGV
from tasksupervisor.control.agv_manager import AgvManager

from .interface import FormalOptimizationInterface


class RoundRobin(FormalOptimizationInterface):
    lock = threading.Lock()

    def __init__(self, _agv_manager):
        # self.agv_types = []
        # self.agv_current_index = []
        # self.agv_manager = _agv_manager
        self.update_agvs(_agv_manager)

    def get_next_agv_by_type(self, _type):
        with self.lock:
            temp_agvs = self.agv_manager.get_agvs_by_type(_type)
            if _type in self.agv_types:
                type_index = self.agv_types.index(_type)
            else:
                raise RuntimeError("Unknown AGV Type")

            if self.agv_current_index[type_index] >= len(temp_agvs):
                self.agv_current_index[type_index] = 0

            if temp_agvs:
                agv = temp_agvs[self.agv_current_index[type_index]]
                self.agv_current_index[type_index] += 1
                return agv
            return None

    def update_agvs(self, _agv_manager):
        with self.lock:
            if _agv_manager:
                self.agv_manager = _agv_manager
            else:
                raise Exception("Invalid agv_manager")

            if len(_agv_manager.get_agv_types()):
                self.agv_types = _agv_manager.get_agv_types()
                self.agv_current_index.clear()
                for x in range(0, len(self.agv_types)):
                    self.agv_current_index.append(0)
            else:
                raise Exception("Empty agv manager - it does not work")


if __name__ == "__main__":
    robot_ids = [1, 2, 3, 3]
    robot_names = ["agv1", "agv2", "agv3", "agv4"]
    robot_types = ["slc", "pallet", "slc", "peter"]
    agv_manager = AgvManager(robot_ids, robot_names, robot_types)
    agvs = agv_manager.get_agv_types()
    rounder = RoundRobin(agv_manager)
    a = rounder.get_next_agv_by_type("pallet")
    print(a.id)
    a = rounder.get_next_agv_by_type("pallet")
    print(a.id)
    a = rounder.get_next_agv_by_type("pallet")
    print(a.id)
