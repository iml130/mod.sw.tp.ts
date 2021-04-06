from tasksupervisor.entities.entity import FiwareEntity
from tasksupervisor.helpers.utc import get_utc_time

class MaterialflowUpdate(FiwareEntity):
    """ representation of a materialflow update """
    def __init__(self, _materialflow=None):
        FiwareEntity.__init__(self)
        if _materialflow:
            self.taskManagerName = _materialflow.taskManagerName
            self.transportOrderList = _materialflow.transportOrderList
            self.refOwnerId = _materialflow.refOwnerId
            self.time = get_utc_time()
        else:
            self.taskManagerName = ""
            self.transportOrderList = []
            self.refOwnerId = ""
            self.time = ""

    @classmethod
    def from_api_object(cls, api_mf_update):
        mf_update = MaterialflowUpdate()

        mf_update.id = str(api_mf_update.id)
        mf_update.taskManagerName = api_mf_update.task_manager_name
        mf_update.transportOrderList = api_mf_update.transport_order_list
        mf_update.refOwnerId = api_mf_update.ref_owner_id
        mf_update.time = api_mf_update.time

        return mf_update
