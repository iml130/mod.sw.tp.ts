import uuid

class OrderState(object):
    def __init__(self):
        self.uuid = ""
        self.type = 0
        self.status = 0
        self.state = 0
    
    @classmethod
    def CreateObjectRosMsg(cls, msg):
        os = OrderState() 
        try: 
            os.uuid = str(uuid.UUID(bytes= msg.order_id.uuid))
            #print(os.uuid)
            os.status = msg.order_status
            os.type = msg.order_type
            os.state = msg.order_state
            
        except:
            return None
        return os

class rosOrderStatus():
    UNKNOWN = 0
    STARTED = 10
    ONGOING = 20
    FINISHED = 30
    WAITING = 40
    ERROR = 255

class rosOrderType():
    UNKNOWN = 0
    MOVE_ORDER = 10
    TRANSPORT_ORDER_STEP = 20
    TRANSPORT_ORDER  = 30

class rosMoveOrderStates():
    MOVE_ORDER_UNAVAILABLE=10
    MOVE_ORDER_START=11
    MOVE_ORDER_ONGOING=12
    MOVE_ORDER_FINISHED=13
    MOVE_ORDER_ERROR=14


class rosTransportOrderStepStates():
    TOS_MOVE_ORDER_START=20
    TOS_MOVE_ORDER_ONGOING=21
    TOS_MOVE_ORDER_FINISHED=22
    TOS_MOVE_ORDER_ERROR=23
    TOS_ACTION_START=24
    TOS_ACTION_ONGOING=25
    TOS_ACTION_FINISHED=26
    TOS_ACTION_ERROR=27

class rosTransportOrderStates():
## Transport order
    TO_LOAD_MOVE_ORDER_START=40
    TO_LOAD_MOVE_ORDER_ONGOING=41
    TO_LOAD_MOVE_ORDER_FINISHED=42
    TO_LOAD_MOVE_ORDER_ERROR=43
    TO_LOAD_ACTION_START=44
    TO_LOAD_ACTION_ONGOING=45
    TO_LOAD_ACTION_FINISHED=46
    TO_LOAD_ACTION_ERROR=47
    TO_UNLOAD_MOVE_ORDER_START=48
    TO_UNLOAD_MOVE_ORDER_ONGOING=49
    TO_UNLOAD_MOVE_ORDER_FINISHED=50
    TO_UNLOAD_MOVE_ORDER_ERROR=51
    TO_UNLOAD_ACTION_START=52
    TO_UNLOAD_ACTION_ONGOING=53
    TO_UNLOAD_ACTION_FINISHED=54
    TO_UNLOAD_ACTION_ERROR=55
 