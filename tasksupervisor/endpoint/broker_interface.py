import abc
import uuid

class BrokerInterface(metaclass=abc.ABCMeta):
    """ Implement this interface to make a Broker work with the Task Supervisor """

    def __init__(self, broker_connector, broker_name=""):
        self.broker_id = uuid.uuid4()
        self.broker_connector = broker_connector
        self.broker_name = broker_name

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'start_interface') and callable(subclass.start_interface) and
                hasattr(subclass, 'subscribe') and callable(subclass.subscribe) and
                hasattr(subclass, 'create') and callable(subclass.create) and
                hasattr(subclass, 'update') and callable(subclass.update) and
                hasattr(subclass, 'delete') and callable(subclass.delete) and
                hasattr(subclass, 'shutdown') and callable(subclass.shutdown) or
                NotImplemented)

    @abc.abstractmethod
    def start_interface(self):
        """ The interface will be started from here. """
        pass

    @abc.abstractmethod
    def subscribe(self, topic, opt_data=None, generic=False):
        """
        Subscribes to the given topic. 

        Parameters:
        topic           -- Will always be an api entity object. Could be converted into a broker specific format.
        opt_data        -- Optional data depending on the given topic. Check the documentation for more info.
        generic         -- Boolean, True when subscription should be generic and False if not

        Return value:
        subscription_id -- An id which is related to the subscription
        """
        pass

    @abc.abstractmethod
    def create(self, entity):
        """
        Creates a new entry for the entity at the broker. Converts given api entity object into a broker specific format.
        
        Parameters:
        entity          -- An api entity object used in the TaskSupervisor.
        """
        pass

    @abc.abstractmethod
    def update(self, entity):
        """
        Updates the given entity at the broker. Converts given api entity object into a broker specific format.
        
        Parameters:
        entity          -- An api entity object used in the TaskSupervisor.
        """
        pass

    @abc.abstractmethod
    def delete(self, id, delete_entity=True):
        """
        Handles deletion of entities and subscriptions.

        Parameters:
        id              -- Either an entity id or an subscription id depending on delete_entity
        delete_entity   -- Boolean, True if the id is from an entity and False if it is a subscription id
        """
        pass

    @abc.abstractmethod
    def shutdown(self):
        """
        Gets called by the BrokerConnector when the TaskSupervisor is terminated.
        """
        pass
