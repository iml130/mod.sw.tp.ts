""" Contains FormalControlInterface class """

import abc

class FormalControlInterface(metaclass=abc.ABCMeta):
    """ Interface for controlling the AGV """
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'create_transport_order') and
                callable(subclass.create_transport_order) and hasattr(subclass, 'manual_action_acknowledge') and
                callable(subclass.manual_action_acknowledge) or
                NotImplemented)

    @abc.abstractmethod
    def create_transport_order(self, task_id: str, from_id: str, to_id: str):
        """Load in the data set"""
        raise NotImplementedError

    @abc.abstractmethod
    def manual_action_acknowledge(self):
        """Load in the data set"""
        raise NotImplementedError
