import abc


class FormalOptimizationInterface(metaclass=abc.ABCMeta):
    agv_manager = None
    agv_types = []
    agv_current_index = []
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'get_next_agv_by_type') and
                callable(subclass.get_next_agv_by_type) or
                NotImplemented)

    @abc.abstractmethod
    def get_next_agv_by_type(self, _task_id: str):
        """Load in the data set"""
        raise NotImplementedError


