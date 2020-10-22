import threading

from tasksupervisor.control.agv import AGV


class AgvManager():
    lock = threading.Lock()

    def __init__(self, _robot_ids, _robot_names, _robot_types): 
        self.available_agvs = {}
        if len(_robot_types) != len(_robot_ids) != len(_robot_names):
            raise ValueError("Invalid length of parameter")
        index = 0
        for robot_id in _robot_ids:
            self.add_agv(_robot_ids[index],
                        _robot_names[index], _robot_types[index])
            index += 1

    def add_agv(self, _robot_id, _robot_name, _robot_type):
        with self.lock:
            if not _robot_id in self.available_agvs:
                self.available_agvs[_robot_id] = AGV(
                    _robot_id, _robot_name, _robot_type)

    def get_agv_by_id(self, _robot_id):
        with self.lock:
            if _robot_id in self.available_agvs:
                return self.available_agvs[_robot_id]
            return None

    def get_agvs_by_type(self, _robot_type):
        with self.lock:
            list_of_agvs = []
            for key, item in self.available_agvs.items():
                if(item.type == _robot_type):
                    list_of_agvs.append(item)
            return list_of_agvs

    def get_agv_types(self):
        agv_types = []
        with self.lock:
            for key, item in self.available_agvs.items():
                if not item.type in agv_types:
                    agv_types.append(item.type)
            return agv_types


if __name__ == "__main__":
    robot_ids = [1, 2, 3, 3]
    robot_names = ["agv1", "agv2", "agv3", "agv4"]
    robot_types = ["slc", "pallet", "slc", "peter"]
    agv_manager = AgvManager(robot_ids, robot_names, robot_types)
    agvs = agv_manager.get_agv_types()
 