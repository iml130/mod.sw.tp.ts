
# import system libs
import threading
import uuid
import logging
import queue
# import multiprocessing

# import 3rd partie libs
from lotlan_scheduler.api.event import Event

# import local packages
from tasksupervisor.helpers.utc import get_utc_time
from tasksupervisor.entities.materialflow_update import MaterialflowUpdate
from tasksupervisor.TaskSupervisor.transport_order import TransportOrder

logger = logging.getLogger(__name__)

# this represents a set of tasks
class Materialflow(threading.Thread):
    def __init__(self, ownerId, _materialflow, _queue_to_scheduler, task_supervisor_knowledge):
        threading.Thread.__init__(self)
        logger.info("taskManager init")
        self.id = uuid.uuid4()
        self.task_supervisor_knowledge = task_supervisor_knowledge
        self.taskManagerName = _materialflow.name
        self.time = get_utc_time()
        self.transportOrderList = []
        self.refOwnerId = ownerId
        self._materialflow = _materialflow

        self._materialflow_update = None

        logger.info("taskMakanger name: %s, uuid: %s",
                    self.taskManagerName, str(self.id))

        #self.runningTask= None
        self._queue_to_scheduler = _queue_to_scheduler
        self._start_task = None

        self._queue_to_transport_order = queue.Queue()
        self._running_transport_orders = {}
        self._repeat_forever = True

        self._materialflow.register_callback_triggered_by(self.cb_triggered_by)
        self._materialflow.register_callback_next_to(self.cb_next_to)
        self._materialflow.register_callback_finished_by(self.cb_finished_by)
        self._materialflow.register_callback_task_finished(
            self.cb_task_finished)
        self._materialflow.register_callback_all_finished(self.cb_all_finished)
        self._materialflow.register_callback_pickup_finished(self.cb_pickup_finished)
        self._materialflow.register_callback_delivery_finished(self.cb_delivery_finished)

        logger.info("taskManager init_done")


    def cb_triggered_by(self, mf_uuid, _uuid, event_information):
        print("cb_triggered_by from mf: " + str(mf_uuid))
        print("UUID: " + str(_uuid), "Event_Info: " + str(event_information))
        temp_uuid = str(_uuid)
        if temp_uuid not in self._running_transport_orders: 
            self._running_transport_orders[temp_uuid] = TransportOrder(
                _uuid, self.id, self.refOwnerId, self._queue_to_transport_order, self.task_supervisor_knowledge) 
        self._running_transport_orders[temp_uuid].wait_for_triggered_by(event_information)
        if not self._running_transport_orders[temp_uuid].is_alive():
            self._running_transport_orders[temp_uuid].start()
        # foreach event in event_information

    def cb_next_to(self, mf_uuid, transport_orders):
        print("cb_next_to from mf: " + str(mf_uuid))
        if self._repeat_forever:
            for key, to in transport_orders.items():
                print("key: ", key, "-> TO: ", to)
                temp_uuid = str(to.uuid)
                if temp_uuid not in self._running_transport_orders:
                    self._running_transport_orders[temp_uuid] = TransportOrder(
                        to.uuid, self.id, self.refOwnerId, self._queue_to_transport_order, self.task_supervisor_knowledge)
                self._running_transport_orders[temp_uuid].set_transport_info(to)
                if not self._running_transport_orders[temp_uuid].is_alive():
                    self._running_transport_orders[temp_uuid].start()
            # print(str(transport_orders))

    def cb_pickup_finished(self, mf_uuid, _uuid):
        print("cb_pickup_finished from mf: " + str(mf_uuid))
        temp_uuid = str(_uuid)
        self._running_transport_orders[temp_uuid].load_agv()

    def cb_delivery_finished(self, mf_uuid, _uuid):
        print("cb_delivery_finished from mf: " + str(mf_uuid))
        temp_uuid = str(_uuid)
        self._running_transport_orders[temp_uuid].unload_agv()

    def cb_finished_by(self, mf_uuid, _uuid, event_information):
        print("cb_finished_by from mf: " + str(mf_uuid))
        print("UUID: " + str(_uuid), "Event_Info: " + str(event_information))
        temp_uuid = str(_uuid)
        if temp_uuid in self._running_transport_orders:
            self._running_transport_orders[temp_uuid].wait_for_finished_by(event_information)

    def cb_task_finished(self, mf_uuid, _uuid):
        print("cb_task_finished from mf: " + str(mf_uuid))
        temp_uuid = str(_uuid)
        if temp_uuid in self._running_transport_orders:
            self._running_transport_orders[temp_uuid].wait_for_finished_by(None)

        print("task with uuid " + str(_uuid) + " finished")
        self._running_transport_orders[temp_uuid].join()
        del self._running_transport_orders[temp_uuid]

    def cb_all_finished(self, mf_uuid):
        print("cb_all_finished from mf: " + str(mf_uuid))

    def set_active(self, is_active):
        self._repeat_forever = is_active

    # def setStartTask(self, start_task):
    #     self._start_task = start_task
    #     self.addTask(start_task)

    def run(self):
        self._materialflow_update = MaterialflowUpdate(self)
        self.task_supervisor_knowledge.orion_connector.create_entity(
            self._materialflow_update)

        self._materialflow.start()
        while self._materialflow.is_running() and self._repeat_forever:
            temp_uuid, temp_lotlan_event = self._queue_to_transport_order.get()

            if temp_lotlan_event is not None:
                if type(temp_lotlan_event) is Event:
                    self._materialflow.fire_event(temp_uuid, temp_lotlan_event)
            pass

        print("WAIT_FOR_END")
        if not self._repeat_forever:
            for key_uuid, _ in self._running_transport_orders.items():
                temp_uuid = str(key_uuid)
                self._running_transport_orders[temp_uuid].join()
                del self._running_transport_orders[temp_uuid]

        self.task_supervisor_knowledge.orion_connector.delete_entity(
            self._materialflow_update.getId())

        self._queue_to_scheduler.put(self.taskManagerName)

    def __cmp__(self, other):
        if self.name == other:
            return 0
        return -1
