# class TaskInfo():
#     def __init__(self, name):
#         self.name = name 
#         self.triggeredBy = []
#         self.transportFrom = []
#         self.transportTo = []
#         self.childs = [] 

class TaskInfo(object):
    def __init__(self):
        self.name = None # String Name of Task
        self.triggers = [] # List of Triggers
        self.transportOrders = [] # List of Transport Order (from|to)
        self.onDone = [] # Reference to the next Tasks

    def addChild(self, _child):
        if(_child not in self.onDone):
            self.onDone.append(_child)


    def __str__(self):
        return self.name    
     
    def __repr__(self):
        return self.__str__()
