import uuid

from tasksupervisor.entities.entity import FiwareEntity

class TaskSupervisorInfo(FiwareEntity):
    def __init__(self):
        FiwareEntity.__init__(self)
        self.usedMaterialFlows = []
        self.numberOfMatarielFlows = len(self.usedMaterialFlows)
        self.message = ""

    def appendMaterialflow(self, _id):
        if _id not in self.usedMaterialFlows:
            self.usedMaterialFlows.append(_id)
            self.numberOfMatarielFlows = len(self.usedMaterialFlows)

    def removeMaterialFlow(self, _id):
        if _id in self.usedMaterialFlows == True:
            self.usedMaterialFlows.remove(_id)
            self.numberOfMatarielFlows = len(self.usedMaterialFlows)