# using enum34
import uuid
 
from Entities.entity import FiwareEntity

id = 0
idHistory = []


class TasksuperVisorInfo(FiwareEntity): 
    def __init__(self): 
        FiwareEntity.__init__(self)
        self.uuid = ""
        self.usedMaterialFlows = []
        self.numberOfMatarielFlows = len(self.usedMaterialFlows)
        self.message = ""

    def appendMaterielflow(self, id):
        if(id not in self.usedMaterialFlows):
            self.usedMaterialFlows.append(id)
            self.numberOfMatarielFlows = len(self.usedMaterialFlows)

    def removeMaterialFlow(self, id):
        if(id in self.usedMaterialFlows == True):
            self.usedMaterialFlows.remove(id)
            self.numberOfMatarielFlows = len(self.usedMaterialFlows)
