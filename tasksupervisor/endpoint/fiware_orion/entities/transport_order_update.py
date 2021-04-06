from tasksupervisor.entities.entity import FiwareEntity
from tasksupervisor.TaskSupervisor.user_action import UserAction

class TransportOrderUpdate(FiwareEntity):
    def __init__(self, _transport_order=None):
        FiwareEntity.__init__(self)

        if _transport_order:
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
        else:
            self.name = ""
            self.startTime = ""
            self.pickupFrom = ""
            self.deliverTo = ""
            self.refOwnerId = ""
            self.refMaterialflowUpdateId = ""
            self.state = None
            self.taskInfo = "" 
            self.robotId = ""


    @classmethod
    def from_api_object(cls, api_transport_order_update):
        transport_order_update = TransportOrderUpdate()

        transport_order_update.id = str(api_transport_order_update.id)
        transport_order_update.name = api_transport_order_update.name
        transport_order_update.startTime = api_transport_order_update.start_time
        transport_order_update.pickupFrom = api_transport_order_update.pickup_from
        transport_order_update.deliverTo = api_transport_order_update.deliver_to
        transport_order_update.refOwnerId = api_transport_order_update.ref_owner_id
        transport_order_update.refMaterialflowUpdateId = api_transport_order_update.ref_materialflow_update_id
        transport_order_update.state = api_transport_order_update.state
        transport_order_update.taskInfo = api_transport_order_update.task_info
        transport_order_update.robotId = api_transport_order_update.robot_id

        return transport_order_update

