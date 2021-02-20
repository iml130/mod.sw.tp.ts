class Location():
    def __init__(self):
        self.coord_x = 0
        self.coord_y = 0
        self.theta = 0

    def set_location(self, location):
        # assert to check if location is current location
        self.coord_x = location.coord_x
        self.coord_y = location.coord_y
        self.theta = location.theta

    def update_location(self, x, y, theta):
        self.coord_x = x
        self.coord_y = y
        self.theta = theta


class WorkingQueue():
    def __init__(self):
        self.tasks_upcoming = 0
        self.tasks_done = 0
        self.busy_time = 0


class AGV():
    def __init__(self, _id, _name, _type):
        self.id = _id
        self.name = _name
        self.type = _type
        self.location = Location()
        self.working_queue = WorkingQueue()
        self.control = None
        
    
    def set_control(self, control):
        self.control = control
