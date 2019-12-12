import logging 


import rospy

from mars_agent_logical_srvs.srv import AddTransportOrder, AddTransportOrderRequest, ManualActionDone, ManualActionDoneRequest
from mars_agent_logical_msgs.msg import TransportOrder, TransportOrderStep, MoveOrder, OrderStatus
from mars_agent_physical_robot_msgs.msg import RobotAction
from mars_agent_physical_robot_msgs.msg._RobotAction import RobotAction as ROBOT_ACTION
from mars_topology_msgs.msg import TopologyEntity, TopologyEntityType

#mars_agent_physical_robot_msgs/RobotAction robot_action
from mars_common.Id import Id, IdType
from std_msgs.msg import Duration, Time

from ROS.OrderState import OrderState

from globals import parsedConfigFile

NAMESPACE = "/mars/agent/logical/" 
TOPIC_ADD_TRANSPORT_ORDER = "add_transport_order"
TOPIC_MANUAL_ACTION_DONE = "manual_action_done"
# Infinite reservation time for manual loading and unloading 
# INIFITE_RSERVATION_TIME = -1.0
# DST_RESERVATION_TIME = -INIFITE_RSERVATION_TIME
DST_RESERVATION_TIME = 5

logger = logging.getLogger(__name__)

def createTopic(_robotid, _topic):
    return (NAMESPACE + str(_robotid) + "/" + str(_topic))

class rTransportOrder():
    def __init__(self, _taskId, _fromId, _toId, _robotId):
        self.status = -1
        print "ROS service (TransportOrder)" 
        
        tmpService = createTopic(_robotId, TOPIC_ADD_TRANSPORT_ORDER)
        rospy.wait_for_service(tmpService)
        try:           
      
            # create the required UUIDs based on the input names
            self.task_id = Id(_taskId, IdType.ID_TYPE_STRING_UUID)
            self.from_id = Id(_fromId, IdType.ID_TYPE_STRING_NAME)
            self.to_id = Id(_toId, IdType.ID_TYPE_STRING_NAME)
            dura = Duration()
            # SIMPLY THE BEST
            dura.data.secs = DST_RESERVATION_TIME
            
            
            # FROM
            move_order_from = MoveOrder(move_order_id=self.task_id.to_msg(), destination_entity=TopologyEntity(
                id=self.from_id.to_msg(), entity_type=TopologyEntityType(10)), destination_reservation_time=dura.data)
            robot_action_load = RobotAction(category= ROBOT_ACTION.CATEGORY_MANUAL_LOAD, description = "load")

            self.transportOderStepFrom = TransportOrderStep(transport_order_step_id=self.task_id.to_msg(),  move_order=move_order_from, robot_action=robot_action_load)


            # TO
            move_order_to = MoveOrder(move_order_id=self.task_id.to_msg(), destination_entity=TopologyEntity(
                id=self.to_id.to_msg(), entity_type=TopologyEntityType(10)), destination_reservation_time=dura.data)
            robot_action_unload = RobotAction(category = ROBOT_ACTION.CATEGORY_MANUAL_UNLOAD, description = "_UNload")
            self.transportOderStepTo = TransportOrderStep(transport_order_step_id=self.task_id.to_msg(),  move_order=move_order_to, robot_action=robot_action_unload)
            


            self.TransportOrder = TransportOrder(transport_order_id=self.task_id.to_msg(), start_step=self.transportOderStepFrom, destination_step = self.transportOderStepTo )
      

            add_transport_order_srv_req = rospy.ServiceProxy(tmpService, AddTransportOrder)
            
            add_transport_order_req = AddTransportOrderRequest(transport_order=self.TransportOrder)

          
            result = add_transport_order_srv_req(self.TransportOrder)
            self.status = result.result.result
            logger.info("addTransportOrderResult" + str(self.status))
            

        except rospy.ServiceException, e:
            logger.info("ROS Service (AddTransportOrder) call failed: %s" % e)
     
        except Exception as ex:
            logger.info("ROS Exception: %s" % ex)

def rManualActionAck(_robotId):
 
    print "ROS service (rManualActionAck)" 
    #robotId = parsedConfigFile.robots[0]
    tmpService = createTopic(_robotId, TOPIC_MANUAL_ACTION_DONE)
    
    rospy.wait_for_service(tmpService)
    try:              

        add_transport_order_srv_req = rospy.ServiceProxy(tmpService, ManualActionDone)
        
        add_transport_order_req = ManualActionDoneRequest()

        
        result = add_transport_order_srv_req()
        result = result.result.result
        logger.info("rManualActionAck" + str(result))
        
        return result

    except rospy.ServiceException, e:
        print "ROS Service (rManualActionAck) call failed: %s" % e
    except Exception as ex:
        print ex