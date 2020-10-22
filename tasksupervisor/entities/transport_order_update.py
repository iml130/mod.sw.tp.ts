

from tasksupervisor.entities.entity import FiwareEntity
from tasksupervisor.TaskSupervisor.user_action import UserAction


class TransportOrderUpdate(FiwareEntity): 
    def __init__(self, _transportOrder):
        FiwareEntity.__init__(self)

        self.name = _transportOrder.taskName
        self.startTime = _transportOrder.startTime
        # self.updateTime = _transportOrder.startTime
        self.pickupFrom = _transportOrder.fromId
        self.deliverTo = _transportOrder.toId
        self.refOwnerId = _transportOrder.refOwnerId
        self.refMaterialflowUpdateId = _transportOrder.refMaterialflowUpdateId
        self.state = _transportOrder._transportOrderStateMachine.state
        self.taskInfo = UserAction.Idle
        self.robotId = _transportOrder._robotId
        if (self.robotId is None):
            self.robotId = "-" 
