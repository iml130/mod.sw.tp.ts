""" Contains Materialflow class """

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
from tasksupervisor.api.materialflow_update import MaterialflowUpdate
from tasksupervisor.TaskSupervisor.transport_order import TransportOrder

logger = logging.getLogger(__name__)

class Materialflow(threading.Thread):
    """ Represents a set of tasks """ 
    def __init__(self, ownerId, _materialflow, _queue_to_scheduler, task_supervisor_knowledge, broker_ref_id):
        threading.Thread.__init__(self)
        logger.info("taskManager init")
        self.id = uuid.uuid4()
        self.task_supervisor_knowledge = task_supervisor_knowledge
        self.task_manager_name = _materialflow.name
        self.time = get_utc_time()
        self.transport_order_list = []
        self.ref_owner_id = ownerId
        self._materialflow = _materialflow
        self.broker_ref_id = broker_ref_id

        self._materialflow_update = None

        logger.info("taskMakanger name: %s, uuid: %s",
                    self.task_manager_name, str(self.id))

        self._queue_to_scheduler = _queue_to_scheduler
        self._start_task = None

        self._queue_to_transport_order = queue.Queue()
        self._running_transport_orders = {}
        self._repeat_forever = True

        self._materialflow.register_callback_triggered_by(self.cb_triggered_by)
        self._materialflow.register_callback_next_to(self.cb_next_to)
        self._materialflow.register_callback_finished_by(self.cb_finished_by)
        self._materialflow.register_callback_task_finished(self.cb_task_finished)
        self._materialflow.register_callback_all_finished(self.cb_all_finished)
        self._materialflow.register_callback_pickup_finished(self.cb_pickup_finished)
        self._materialflow.register_callback_delivery_finished(self.cb_delivery_finished)

        logger.info("taskManager init_done")


    def cb_triggered_by(self, mf_uuid, uuid_, event_information):
        print("cb_triggered_by from mf: " + str(mf_uuid))
        print("UUID: " + str(uuid_), "Event_Info: " + str(event_information))
        temp_uuid = str(uuid_)
        if temp_uuid not in self._running_transport_orders:
            self._running_transport_orders[temp_uuid] = TransportOrder(uuid_, self.id, self.ref_owner_id,
                                                                       self._queue_to_transport_order,
                                                                       self.task_supervisor_knowledge,
                                                                       self.broker_ref_id)
        self._running_transport_orders[temp_uuid].wait_for_triggered_by(event_information)
        if not self._running_transport_orders[temp_uuid].is_alive():
            self._running_transport_orders[temp_uuid].start()

    def cb_next_to(self, mf_uuid, transport_orders):
        print("cb_next_to from mf: " + str(mf_uuid))
        if self._repeat_forever:
            for key, to in transport_orders.items():
                print("key: ", key, "-> TO: ", to)
                temp_uuid = str(to.uuid)
                if temp_uuid not in self._running_transport_orders:
                    self._running_transport_orders[temp_uuid] = TransportOrder(to.uuid, self.id, self.ref_owner_id,
                                                                               self._queue_to_transport_order,
                                                                               self.task_supervisor_knowledge,
                                                                               self.broker_ref_id)
                self._running_transport_orders[temp_uuid].set_transport_info(to)
                if not self._running_transport_orders[temp_uuid].is_alive():
                    self._running_transport_orders[temp_uuid].start()

    def cb_pickup_finished(self, mf_uuid, uuid_):
        print("cb_pickup_finished from mf: " + str(mf_uuid))
        temp_uuid = str(uuid_)
        self._running_transport_orders[temp_uuid].load_agv()

    def cb_delivery_finished(self, mf_uuid, uuid_):
        print("cb_delivery_finished from mf: " + str(mf_uuid))
        temp_uuid = str(uuid_)
        self._running_transport_orders[temp_uuid].unload_agv()

    def cb_finished_by(self, mf_uuid, uuid_, event_information):
        print("cb_finished_by from mf: " + str(mf_uuid))
        print("UUID: " + str(uuid_), "Event_Info: " + str(event_information))
        temp_uuid = str(uuid_)
        if temp_uuid in self._running_transport_orders:
            self._running_transport_orders[temp_uuid].wait_for_finished_by(event_information)

    def cb_task_finished(self, mf_uuid, uuid_):
        print("cb_task_finished from mf: " + str(mf_uuid))
        temp_uuid = str(uuid_)
        if temp_uuid in self._running_transport_orders:
            self._running_transport_orders[temp_uuid].wait_for_finished_by(None)

        print("task with uuid " + str(uuid_) + " finished")
        self._running_transport_orders[temp_uuid].join()
        del self._running_transport_orders[temp_uuid]

    def cb_all_finished(self, mf_uuid):
        print("cb_all_finished from mf: " + str(mf_uuid))

    def set_active(self, is_active):
        self._repeat_forever = is_active

    def run(self):
        self._materialflow_update = MaterialflowUpdate(self)
        self.task_supervisor_knowledge.broker_connector.create(self._materialflow_update)

        self._materialflow.start()
        while self._materialflow.is_running() and self._repeat_forever:
            temp_uuid, temp_lotlan_event = self._queue_to_transport_order.get()

            if temp_lotlan_event is not None:
                if isinstance(temp_lotlan_event, Event):
                    self._materialflow.fire_event(temp_uuid, temp_lotlan_event)
            pass

        logger.info("Waiting for end")
        if not self._repeat_forever:
            for key_uuid, _ in self._running_transport_orders.items():
                temp_uuid = str(key_uuid)
                self._running_transport_orders[temp_uuid].join()
                del self._running_transport_orders[temp_uuid]

        self.task_supervisor_knowledge.broker_connector.delete(self._materialflow_update.id, self.broker_ref_id)

        self._queue_to_scheduler.put(self.task_manager_name)

    def __cmp__(self, other):
        if self.name == other:
            return 0
        return -1
