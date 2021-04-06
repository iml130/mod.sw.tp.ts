import abc
import uuid

class BrokerInterface(metaclass=abc.ABCMeta):
    """ Implement this interface to make a Broker work with the Task Supervisor """

    def __init__(self, broker_name=""):
        self.broker_id = uuid.uuid4()
        self.broker_name = broker_name

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'subscribe') and callable(subclass.subscribe) and
                hasattr(subclass, 'create') and callable(subclass.create) and
                hasattr(subclass, 'update') and callable(subclass.update) and
                hasattr(subclass, 'delete') and callable(subclass.delete) or 
                NotImplemented)

    @abc.abstractmethod
    def start_interface(self):
        pass

    @abc.abstractmethod
    def subscribe(self, topic, opt_data=None, generic=False):
        """ Handle Subscriptions """
        pass

    @abc.abstractmethod
    def create(self, entity):
        """ Handle creation of new data entries """
        pass

    @abc.abstractmethod
    def update(self, entity):
        """ Handle updating of the given data """
        pass

    @abc.abstractmethod
    def delete(self, entity_id):
        """ Handle deletion of the given data """
        pass

    @abc.abstractmethod
    def shutdown(self):
        pass
