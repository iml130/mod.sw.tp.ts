""" Contains RoundRobin class """

import threading

from .interface import FormalOptimizationInterface


class RoundRobin(FormalOptimizationInterface):
    """ Round Robin implementation of the FormalOptimizationInterface """
    lock = threading.Lock()

    def __init__(self, agv_manager):
        self.update_agvs(agv_manager)

    def get_next_agv_by_type(self, type_):
        with self.lock:
            temp_agvs = self.agv_manager.get_agvs_by_type(type_)
            if type_ in self.agv_types:
                type_index = self.agv_types.index(type_)
            else:
                raise RuntimeError("Unknown AGV Type")

            if self.agv_current_index[type_index] >= len(temp_agvs):
                self.agv_current_index[type_index] = 0

            if temp_agvs:
                agv = temp_agvs[self.agv_current_index[type_index]]
                self.agv_current_index[type_index] += 1
                return agv
            return None

    def update_agvs(self, agv_manager):
        with self.lock:
            if agv_manager:
                self.agv_manager = agv_manager
            else:
                raise Exception("Invalid agv_manager")

            if agv_manager.get_agv_types():
                self.agv_types = agv_manager.get_agv_types()
                self.agv_current_index.clear()
                for x in range(0, len(self.agv_types)):
                    self.agv_current_index.append(0)
            else:
                raise Exception("Empty agv manager - it does not work")
