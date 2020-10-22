# import system libs
import logging

# import 3rd party libs
import rospy

from mars_agent_logical_srvs.srv import AddTransportOrder, AddTransportOrderRequest, ManualActionDone, ManualActionDoneRequest
from mars_agent_logical_msgs.msg import TransportOrder, TransportOrderStep, MoveOrder
from mars_agent_physical_robot_msgs.msg import RobotAction
from mars_agent_physical_robot_msgs.msg._RobotAction import RobotAction as ROBOT_ACTION
from mars_topology_msgs.msg import TopologyEntity, TopologyEntityType

from mars_common.Id import Id, IdType
from std_msgs.msg import Duration


# import local libs
from .interface import FormalControlInterface


logger = logging.getLogger(__name__)

DST_RESERVATION_TIME = 5
NAMESPACE = "/mars/agent/logical/"
TOPIC_ADD_TRANSPORT_ORDER = "add_transport_order"
TOPIC_MANUAL_ACTION_DONE = "manual_action_done"


class RosControl(FormalControlInterface):
    """Extract text from a PDF."""

    def __init__(self):
        self.status = 0

    def create_transport_order(self, _task_id: str, _from_id: str, _to_id: str, _robot_id: str) -> str:
        """Overrides FormalParserInterface.create_transport_order()"""

        logger.info("ROS create_transport_order")
        service_topic_add_transport_order = self._create_topic(
            _robot_id, TOPIC_ADD_TRANSPORT_ORDER)
        rospy.wait_for_service(service_topic_add_transport_order)
        try:
            ros_task_id = Id(_task_id, IdType.ID_TYPE_STRING_UUID)
            ros_from_id = Id(_from_id, IdType.ID_TYPE_STRING_NAME)
            ros_to_id = Id(_to_id, IdType.ID_TYPE_STRING_NAME)
            duration = Duration()
            duration.data.secs = DST_RESERVATION_TIME

            # FROM
            move_order_from = MoveOrder(move_order_id=ros_task_id.to_msg(), destination_entity=TopologyEntity(
                id=ros_from_id.to_msg(), entity_type=TopologyEntityType(10)), destination_reservation_time=duration.data)
            robot_action_load = RobotAction(
                category=ROBOT_ACTION.CATEGORY_MANUAL_LOAD, description="load")

            transport_order_step_from = TransportOrderStep(transport_order_step_id=ros_task_id.to_msg(
            ), move_order=move_order_from, robot_action=robot_action_load)

            # TO
            ros_move_order_to = MoveOrder(move_order_id=ros_task_id.to_msg(), destination_entity=TopologyEntity(
                id=ros_to_id.to_msg(), entity_type=TopologyEntityType(10)), destination_reservation_time=duration.data)

            ros_robot_action_unload = RobotAction(
                category=ROBOT_ACTION.CATEGORY_MANUAL_UNLOAD, description="_UNload")
            ros_transport_order_step_to = TransportOrderStep(transport_order_step_id=ros_task_id.to_msg(
            ), move_order=ros_move_order_to, robot_action=ros_robot_action_unload)

            ros_transport_order = TransportOrder(transport_order_id=ros_task_id.to_msg(
            ), start_step=transport_order_step_from, destination_step=ros_transport_order_step_to)

            add_transport_order_srv_req = rospy.ServiceProxy(
                service_topic_add_transport_order, AddTransportOrder)
            add_transport_order_req = AddTransportOrderRequest(
                transport_order=ros_transport_order)

            ros_service_call_result = add_transport_order_srv_req(
                ros_transport_order)
            self.status = ros_service_call_result.result.result
            logger.info("addTransportOrderResult: %s", str(self.status))

        except rospy.ServiceException as err:
            logger.error(
                "ROS Service (AddTransportOrder) call failed: %s", err)

        except Exception as ex:
            logger.info("ROS Exception: %s", ex)

    def manual_action_acknowledge(self, _robot_id):
        logger.info("ROS manual_action_acknowledge")
        service_topic_manual_action_done = self._create_topic(
            _robot_id, TOPIC_MANUAL_ACTION_DONE)

        rospy.wait_for_service(service_topic_manual_action_done)
        try:

            ros_manual_action_done = rospy.ServiceProxy(
                service_topic_manual_action_done, ManualActionDone)

            ros_manual_action_done_req = ManualActionDoneRequest()

            result = ros_manual_action_done()
            result = result.result.result
            logger.info("rManualActionAck %s", str(result))

            return result

        except rospy.ServiceException as err:
            logger.error("ROS Service (rManualActionAck) call failed: %s", err)
        except Exception as ex:
            logger.error(ex)
            logger.info("ROS manual_action_acknowledge done")

    def _create_topic(self, _robot_id, _topic):
        return NAMESPACE + str(_robot_id) + "/" + str(_topic)


if __name__ == "__main__":
    temp_ros_control = RosControl()
    temp_ros_control.create_transport_order("1", "2", "3", "4")
