""" Contains BrokerConnector and BrokerException class """

from tasksupervisor import my_globals

class BrokerException(Exception):
    """
        Gets raised if something went wrong while interacting with the Broker.
        For example unexcepted or error status codes.
    """
    pass

class BrokerConnector:
    """
        Layer between Broker Interfaces and Supervisor.
        Manages multiple Interface instances and the correct distribution of messages
    """

    def __init__(self, task_supervisor):
        self.interfaces = {}
        self.task_supervisor = task_supervisor
        self.sensor_id_to_ids_dict = dict()

    def register_interface(self, interface):
        self.interfaces[interface.broker_id] = interface

    def unregister_interface(self, interface):
        if interface.broker_id in self.interfaces:
            del self.interfaces[interface.broker_id]

    def subscribe_to_specific(self, topic, broker_id, opt_data=None, generic=False):
        class_name = str(topic.__class__.__name__)
        if class_name == "SensorAgent":
            transport_order_id = opt_data.to_id
            self.sensor_id_to_ids_dict[topic.id] = []
            self.sensor_id_to_ids_dict[topic.id].append(transport_order_id)

        interface = self.get_interface_by_broker_id(broker_id)
        return interface.subscribe(topic, opt_data=opt_data, generic=generic)

    def subscribe_to_all(self, topic, opt_data=None, generic=False):
        for interface in self.interfaces.values():
            interface.subscribe(topic, opt_data=opt_data, generic=generic)

    def retreive(self, data, interface):
        class_name = str(data.__class__.__name__)
        if class_name == "Materialflow":
            data.broker_ref_id = interface.broker_id
            my_globals.taskQueue.put((data, class_name))
        elif class_name == "SensorAgent":
            for to_id in self.sensor_id_to_ids_dict[data.id]:
                self.task_supervisor.sensor_dispatcher.put_data(to_id, data)

    def create(self, entity):
        class_name = str(entity.__class__.__name__)

        if class_name == "TaskSupervisorInfo":
            for interface in self.interfaces.values():
                interface.create(entity)
        else:
            interface = self.get_interface_by_broker_id(entity.broker_ref_id)
            interface.create(entity)

    def update(self, entity):
        class_name = str(entity.__class__.__name__)

        if class_name == "TaskSupervisorInfo":
            for interface in self.interfaces.values():
                interface.update(entity)
        else:
            interface = self.get_interface_by_broker_id(entity.broker_ref_id)
            interface.update(entity)

    def delete(self, id_, broker_id, delete_entity=True):
        interface = self.get_interface_by_broker_id(broker_id)
        interface.delete(id_, delete_entity=delete_entity)

    def get_interface_by_broker_id(self, broker_id):
        if broker_id in self.interfaces:
            return self.interfaces[broker_id]
        raise ValueError("Unknown BrokerID: {}".format(broker_id))

    def shutdown(self):
        for interface in self.interfaces.values():
            interface.shutdown()
