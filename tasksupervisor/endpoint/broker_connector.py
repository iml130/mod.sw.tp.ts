from tasksupervisor import my_globals

class BrokerConnector:
    """
        Layer between Broker Interfaces and Supervisor.
        Manages multiple Interface instances and the correct distribution of messages
    """

    def __init__(self, ):
        self.interfaces = []
        self.interface_mf_ids_dict = dict()
        self.mf_ids_interface_dict = dict()

    def register_interface(self, interface):
        self.interfaces.append(interface)
        self.interface_mf_ids_dict[interface] = []

    def subscribe_specific(self, topic):
        pass

    def subscribe_generic(self, topic):
        for interface in self.interfaces:
            interface.subscribe(topic)

    def retreive(self, data, interface):
        class_name = str(data.__class__.__name__)
        if class_name == "Materialflow":
            self.interface_mf_ids_dict[interface].append(data.id)
            my_globals.taskQueue.put((data, class_name))

    def create(data):
        pass

    def update(data):
        pass

    def delete(data):
        pass
