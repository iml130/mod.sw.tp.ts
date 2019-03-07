from abc import ABC, abstractmethod
import uuid

class AbstractTask(ABC):
    def __init__(self):
        self.id = str(uuid.uuid4())

    def __