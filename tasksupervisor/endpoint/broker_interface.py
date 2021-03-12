import abc
import threading

class BrokerInterface(threading.Thread, metaclass=abc.ABCMeta):
    """ Implement this interface to make a Broker work with the Task Supervisor """

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'subscribe') and callable(subclass.subscribe) and
                hasattr(subclass, 'create') and callable(subclass.create) and
                hasattr(subclass, 'update') and callable(subclass.update) and
                hasattr(subclass, 'delete') and callable(subclass.delete) or 
                NotImplemented)

    @abc.abstractmethod
    def run(self):
        pass

    @abc.abstractmethod
    def subscribe(self, topic, opt_data = None):
        """ Handle Subscriptions """
        pass

    @abc.abstractmethod
    def create(self, data):
        """ Handle creation of new data entries """
        pass

    @abc.abstractmethod
    def update(self, data):
        """ Handle updating of the given data """
        pass

    @abc.abstractmethod
    def delete(self, data):
        """ Handle deletion of the given data """
        pass
