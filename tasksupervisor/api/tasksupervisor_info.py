import uuid

class TaskSupervisorInfo():
    def __init__(self):
        self.id = uuid.uuid4()
        self.used_materialflows = []
        self.number_of_materialflows = len(self.used_materialflows)
        self.message = ""

    def appendMaterialflow(self, _id):
        if _id not in self.used_materialflows:
            self.used_materialflows.append(_id)
            self.number_of_materialflows = len(self.used_materialflows)

    def removeMaterialFlow(self, _id):
        if _id in self.used_materialflows == True:
            self.used_materialflows.remove(_id)
            self.number_of_materialflows = len(self.used_materialflows)
