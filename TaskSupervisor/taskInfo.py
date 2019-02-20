class TaskInfo():
    def __init__(self, name):
        self.name = name 
        self.triggeredBy = []
        self.transportFrom = []
        self.transportTo = []
        self.childs = [] 
    
    def addChild(self, _child):
        if(_child not in self.childs):
            self.childs.append(_child)

    

    def __str__(self):
        return self.name    
     
    def __repr__(self):
        return self.__str__()
