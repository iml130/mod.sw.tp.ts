import uuid

from tasksupervisor.entities.entity import FiwareEntity

class TaskSupervisorInfo(FiwareEntity):
    def __init__(self):
        FiwareEntity.__init__(self)
        self.usedMaterialFlows = []
        self.numberOfMaterialFlows = len(self.usedMaterialFlows)
        self.message = ""

    def appendMaterialflow(self, _id):
        if _id not in self.usedMaterialFlows:
            self.usedMaterialFlows.append(_id)
            self.numberOfMaterialFlows = len(self.usedMaterialFlows)

    def removeMaterialFlow(self, _id):
        if _id in self.usedMaterialFlows == True:
            self.usedMaterialFlows.remove(_id)
            self.numberOfMaterialFlows = len(self.usedMaterialFlows)
    
    @classmethod
    def from_api_object(cls, api_task_supervisor_info):
        task_supervisor_info = TaskSupervisorInfo()

        task_supervisor_info.id = str(api_task_supervisor_info.id)
        task_supervisor_info.usedMaterialFlows = api_task_supervisor_info.used_materialflows
        task_supervisor_info.numberOfMaterialFlows = api_task_supervisor_info.number_of_materialflows
        task_supervisor_info.message = api_task_supervisor_info.message

        return task_supervisor_info
