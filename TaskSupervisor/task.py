__author__ = "Peter Detzner"
__version__ = "0.0.1a"
__status__ = "Developement"

# IMPORT SYSTEM LIBS
import threading
import time
from random import randint
import uuid
import Queue
import logging
import datetime
import json
import sys


# IMPORT 3rd party libs

import rospy
from mars_agent_logical_srvs.srv import AddMoveOrder, AddMoveOrderRequest
from mars_agent_logical_msgs.msg import MoveOrder, OrderStatus
from mars_topology_msgs.msg import TopologyEntity, TopologyEntityType
from mars_common.Id import Id, IdType
from std_msgs.msg import Duration, Time

# IMPORT LOCAL libs
from globals import sanDictQueue, rosMessageDispatcher
import globals
from transportOrder import TransportOrder
from taskInfo import TaskInfo

from FiwareObjectConverter.objectFiwareConverter import ObjectFiwareConverter
from Entities.entity import FiwareEntity
from Entities.san import SensorAgent, SensorData


from ROS.OrderState import OrderState

ocbHandler = globals.ocbHandler

logger = logging.getLogger(__name__)


def obj2JsonArray(_obj):
    tempArray = []
    tempArray.append(_obj)
    print json.dumps(tempArray)
    return (tempArray)


toggle = True


class Task():
    def __init__(self, _taskInfo, _taskManagerUuid):
        # threading.Thread.__init__(self)
        logger.info("Task init")

        # only these attribues will be published
 

        self.id = str(uuid.uuid4())
        self.taskManagerId = _taskManagerUuid
        self.taskName = str(_taskInfo.name)
        self.state = State.Idle
        self.time = str(datetime.datetime.now())

        # setting up the thread
        self._threadRunner = threading.Thread(target=self.run)
        self._threadRunner.setDaemon(True)
        # self._t.start()

        logger.info("Task name: " + self.taskName + ", uuid:" + str(self.id))
        self._taskInfo = _taskInfo
        sanDictQueue.addThread(self.id)
        rosMessageDispatcher.addThread(self.id)

        self._q = sanDictQueue.getQueue(self.id)
        self._rosQ = rosMessageDispatcher.getQueue(self.id)

        # self.transportOrder = TransportOrder(self.name)
        logger.info("Task init_done")

# thread imitation
    def start(self):
        logger.info("Task start")
        self.publishEntity()
        self._threadRunner.start()
        logger.info("Task start_done")

    def join(self):
        logger.info("Task join")
        self._threadRunner.join()
        self.deleteEntity()
        logger.info("Task join_done")

# updates orion (publish, update and delete)
    def publishEntity(self):
        global ocbHandler
        logger.info("Task publishEntity " + self.taskName)
      #  ocbHandler.create_entity(self.taskState)

        self.time = str(datetime.datetime.now())
        ocbHandler.create_entity(self)
        logger.info("Task publishEntity_done")

    def deleteEntity(self):
        global ocbHandler
        logger.info("Task deleteEntity " + self.taskName)
        self.time = str(datetime.datetime.now())
        ocbHandler.delete_entity(self.id)
        logger.info("Task deleteEntity_done")

    def updateEntity(self):
        global ocbHandler
        logger.info("Task updateEntity " + self.taskName)
        self.time = str(datetime.datetime.now())
        ocbHandler.update_entity(self)
        logger.info("Task updateEntity")

    def __str__(self):
        return "Task name: " + self.taskName + ",uuid: " + str(self.id)

    def __repr__(self):
        return self.__str__()

    def sendMoveOrder(self, destination = None):
        rospy.wait_for_service('/mars_agent_logical_robot_0/add_move_order')
        try:
                            
            global toggle
            if(destination):
                newId = uuid.uuid3(uuid.NAMESPACE_DNS, destination)
            
            if(toggle):
               # id_str = "00000000000000000000000000000003"
                id_str = "moldingArea_palletPlace"
                
            else:
                id_str = str('00000000000000000000000000000010')
                #toggle = True

            task_id = Id(self.id, IdType.ID_TYPE_UUID)
            dest_id = Id(id_str, IdType.ID_TYPE_STRING_NAME)
            
            dura = Duration()
            # SIMPLY THE BEST
            dura.data.secs = 5 

            add_move_order_srv_req = rospy.ServiceProxy(
                '/mars_agent_logical_robot_0/add_move_order', AddMoveOrder)
            move_order = MoveOrder(move_order_id=task_id.to_msg(), destination_entity=TopologyEntity(
                id=dest_id.to_msg(), entity_type=TopologyEntityType(10)), destination_reservation_time=dura.data)
            add_move_order_req = AddMoveOrderRequest(move_order=move_order)

            if(toggle):
                toggle = False
                result = add_move_order_srv_req(move_order)

                print result

        except rospy.ServiceException, e:
            print "Service call failed: %s" % e
        except Exception as ex:
            print ex

        
    def run(self):
        self.state = State.Running
        self.updateEntity()
        ts = SensorAgent()
        subscriptionId = ocbHandler.subscribe2Entity(_description="Individual blabla",
                                                     _entities=obj2JsonArray(
                                                         ts.getEntity()),
                                                     _notification=globals.parsedConfigFile.getTaskPlannerAddress() + "/san/" + self.id, _generic=True)
        globals.subscriptionDict[subscriptionId] = "SAN"

        tempVal = 15  # (randint(2,7))
        logger.info("Task running, " + str(self))
        print "\nrunning " + self.taskName + ", sleep " + str(tempVal)
        # time.sleep(tempVal)
        try:
            
            # TODO / ROS / Disabling while ROS implementation
            self.sendMoveOrder()
            bb = self._rosQ.get()

            a = self._q.get(timeout=tempVal)
            if (a):
                dd = SensorAgent.CreateObjectFromJson(a["data"][0])
                logger.info("Just a small timeout of 10secs")
               # dd.findSensorById(self._taskInfo.triggers[0].left)
                time.sleep(10)

        except Queue.Empty:
            pass
        rosMessageDispatcher.removeThread(self.id)
        sanDictQueue.removeThread(self.id)
        ocbHandler.deleteSubscriptionById(subscriptionId)
        self.state = State.Finished
        self.updateEntity()
        logger.info("Task finished, " + str(self))


class TaskState(FiwareEntity):

    def __init__(self, _task):
        if(not isinstance(_task, Task)):
            raise Exception("TypeMissmatch")
        FiwareEntity.__init__(self, id=_task.id)
        self.name = _task.taskName
        self.state = State.Idle
        self.taskId = _task.id
        self.taskManagerId = _task.taskManagerId
        # self.taskSpecUuid = None
        self.errorMessage = ""

# TASK
# 0= No-Task, 1 = Start, 2 = Pause, 3 = Cancel, 4 = EmergencyStop, 5 = Reset"
# TASK_STATE
# Idle : 0, Running : 1, Waiting : 2, Active : 3, Finished : 4, Aborted : 5, Error : 6


class State():
    Idle = 0
    Running = 1
    Waiting = 2
    Active = 3
    Finished = 4
    Aborted = 5
    Error = 6
