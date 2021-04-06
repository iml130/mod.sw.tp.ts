import uuid

from tasksupervisor.helpers.utc import get_utc_time

class MaterialflowUpdate():
    """ Representation of a materialflow update """
    def __init__(self, materialflow):
        self.id = uuid.uuid4() 
        self.task_manager_name = materialflow.task_manager_name
        self.transport_order_list = materialflow.transport_order_list
        self.ref_owner_id = materialflow.ref_owner_id
        self.time = get_utc_time()
        self.broker_ref_id = materialflow.broker_ref_id
