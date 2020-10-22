import threading


from tasksupervisor.helpers.dict_queue import DictQueue

class TaskSupervisorKnowledge():
    lock = threading.Lock()
    def __init__(self): 
        self.agv_manager = None
        self.optimizer = None
        self.orion_connector = None
        self.task_planner_address = None

        self.sensor_dispatcher = DictQueue()
        self.ros_message_dispatcher = DictQueue()

        
        self.subscription_dict = {}