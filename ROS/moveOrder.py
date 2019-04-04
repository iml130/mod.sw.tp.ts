
import rospy

from mars_agent_logical_srvs.srv import AddMoveOrder, AddMoveOrderRequest
from mars_agent_logical_msgs.msg import MoveOrder, OrderStatus
from mars_topology_msgs.msg import TopologyEntity, TopologyEntityType
from mars_common.Id import Id, IdType
from std_msgs.msg import Duration, Time

from ROS.OrderState import OrderState

class rMoveOrder():
    def __init__(self, _id, _destinationName):
        rospy.wait_for_service('/mars_agent_logical_robot_0/add_move_order')
        try:
                             
            if(_destinationName):
                id_str = _destinationName
                # uuid.uuid3(uuid.NAMESPACE_DNS, destinationName)
            else: 
                return  

            self.task_id = Id(_id, IdType.ID_TYPE_UUID)
            self.dest_id = Id(_destinationName, IdType.ID_TYPE_STRING_NAME)
            
            dura = Duration()
            # SIMPLY THE BEST
            dura.data.secs = 5 

            add_move_order_srv_req = rospy.ServiceProxy(
                '/mars_agent_logical_robot_0/add_move_order', AddMoveOrder)
            move_order = MoveOrder(move_order_id=self.task_id.to_msg(), destination_entity=TopologyEntity(
                id=self.dest_id.to_msg(), entity_type=TopologyEntityType(10)), destination_reservation_time=dura.data)
            add_move_order_req = AddMoveOrderRequest(move_order=move_order)

          
            result = add_move_order_srv_req(move_order)

            print result

        except rospy.ServiceException, e:
            print "Service call failed: %s" % e
        except Exception as ex:
            print ex

 