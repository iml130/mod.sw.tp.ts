""" Contains TransportOrderUpdate API class """

import uuid

from tasksupervisor.TaskSupervisor.user_action import UserAction

class TransportOrderUpdate():
    """
        Once, a Transportion by an AGV starts, the TaskPlanner will create a TransportOrderUpdate.
        It contains information about the TransportOrder for example the start time.    
    """
    def __init__(self, transport_order):
        self.id = uuid.uuid4() 
        self.name = transport_order.task_name
        self.start_time = transport_order.start_time
        self.update_time = transport_order.start_time
        self.broker_ref_id = ""

        if transport_order._to_info:
            self.pickup_from = transport_order._to_info.to_step_from.location.physical_name
        else:
            self.pickup_from = "Unknown"

        if transport_order._to_info:
            self.deliver_to = transport_order._to_info.to_step_to.location.physical_name
        else:
            self.deliver_to = "Unknown"

        self.ref_owner_id = transport_order.ref_owner_id
        self.ref_materialflow_update_id = str(transport_order.ref_materialflow_update_id)
        self.state = transport_order._to_state_machine.state
        self.task_info = UserAction.Idle
        if transport_order._robot_id:
            self.robot_id = transport_order._robotId
        else:
            self.robot_id = "-"
