from tasksupervisor.entities.entity import FiwareEntity
from tasksupervisor.helpers.utc import get_utc_time

class MaterialflowUpdate(FiwareEntity):
    """ representation of a materialflow update """
    def __init__(self, _materialflow):
        FiwareEntity.__init__(self)
        self.taskManagerName = _materialflow.taskManagerName
        self.transportOrderList = _materialflow.transportOrderList
        self.refOwnerId = _materialflow.refOwnerId
        self.time = get_utc_time()