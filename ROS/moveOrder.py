
import rospy

from mars_agent_logical_srvs.srv import AddMoveOrder, AddMoveOrderRequest
from mars_agent_logical_msgs.msg import MoveOrder, OrderStatus
from mars_topology_msgs.msg import TopologyEntity, TopologyEntityType
from mars_common.Id import Id, IdType
from std_msgs.msg import Duration, Time

from ROS.OrderState import OrderState

class rMoveOrder():
    def __init__(self, _id, _destinationName):
        self.status = -1
        print "ROS service (MoveOder)" 
        rospy.wait_for_service('/mars/agent/logical/robot_00000000000000000000000000000100/add_move_order')
        try:           
            if(_destinationName):
                id_str = _destinationName
                # uuid.uuid3(uuid.NAMESPACE_DNS, destinationName)
            else: 
                return  

            self.task_id = Id(_id, IdType.ID_TYPE_STRING_UUID)
            
            self.dest_id = Id(_destinationName, IdType.ID_TYPE_STRING_NAME)
            print("Converting Name: " +  str(_destinationName) + " to UUID: ")
            print (self.dest_id)
            dura = Duration()
            # SIMPLY THE BEST
            dura.data.secs = 5 

            add_move_order_srv_req = rospy.ServiceProxy(
                '/mars/agent/logical/robot_00000000000000000000000000000100/add_move_order', AddMoveOrder)
            move_order = MoveOrder(move_order_id=self.task_id.to_msg(), destination_entity=TopologyEntity(
                id=self.dest_id.to_msg(), entity_type=TopologyEntityType(10)), destination_reservation_time=dura.data)
            add_move_order_req = AddMoveOrderRequest(move_order=move_order)

          
            result = add_move_order_srv_req(move_order)
            self.status = result.result.result
            print "addMoveOrderResult"
            print self.status

        except rospy.ServiceException, e:
            print "ROS Service (MoveOrder) call failed: %s" % e
        except Exception as ex:
            print ex

 