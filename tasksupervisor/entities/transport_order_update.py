

from tasksupervisor.entities.entity import FiwareEntity
from tasksupervisor.TaskSupervisor.user_action import UserAction


class TransportOrderUpdate(FiwareEntity):
    def __init__(self, _transport_order):
        FiwareEntity.__init__(self)

        self.name = _transport_order.task_name
        self.startTime = _transport_order.start_time
        # self.updateTime = _transportOrder.startTime
        if _transport_order._to_info:
            self.pickupFrom = _transport_order._to_info.to_step_from.location.physical_name
        else:
            self.pickupFrom = "Unknown"

        if _transport_order._to_info:
            self.deliverTo = _transport_order._to_info.to_step_to.location.physical_name
        else:
            self.deliverTo = "Unknown"

        self.refOwnerId = _transport_order.ref_owner_id
        self.refMaterialflowUpdateId = str(_transport_order.ref_materialflow_update_id)
        self.state = _transport_order._to_state_machine.state
        self.taskInfo = UserAction.Idle
        if _transport_order._robot_id:
            self.robotId = _transport_order._robotId
        else:
            self.robotId = "-"
