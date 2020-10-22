import abc


class FormalControlInterface(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'create_transport_order') and
                callable(subclass.create_transport_order) and hasattr(subclass, 'manual_action_acknowledge') and
                callable(subclass.manual_action_acknowledge) or
                NotImplemented)

    @abc.abstractmethod
    def create_transport_order(self, _task_id: str, _from_id: str, _to_id: str, _robot_id: str):
        """Load in the data set"""
        raise NotImplementedError

    @abc.abstractmethod
    def manual_action_acknowledge(self, _robot_id: str):
        """Load in the data set"""
        raise NotImplementedError
