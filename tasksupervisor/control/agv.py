import threading
from tasksupervisor.control.interface import FormalControlInterface

class Location():
    def __init__(self):
        self.coord_x = 0
        self.coord_y = 0
        self.theta = 0

class WorkingQueue():
    def __init__(self):
        self.tasks_upcoming = 0
        self.tasks_done = 0
        self.busy_time = 0


class AGV():
    lock = threading.Lock()
    def __init__(self, _id, _name, _type):
        self.id = _id
        self.name = _name
        self.type = _type
        self.location = Location()
        self.working_queue = WorkingQueue()
        self.control = None
        
    
    def set_control(self, control):
        self.control = control
