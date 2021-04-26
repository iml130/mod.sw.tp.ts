""" Contains TaskSupervisorInfo API class """

import uuid

class TaskSupervisorInfo():
    """
        Gets created at the start of the Supervisor and provides information
        about the total number of started materialflows.
    """
    def __init__(self):
        self.id = uuid.uuid4()
        self.used_materialflows = []
        self.number_of_materialflows = len(self.used_materialflows)
        self.message = ""

    def append_materialflow(self, id_):
        if id_ not in self.used_materialflows:
            self.used_materialflows.append(id_)
            self.number_of_materialflows = len(self.used_materialflows)

    def remove_materialflow(self,id_):
        if id_ in self.used_materialflows == True:
            self.used_materialflows.remove(id_)
            self.number_of_materialflows = len(self.used_materialflows)
