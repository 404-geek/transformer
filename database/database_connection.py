from abc import ABC, abstractmethod

class DatabaseConnection(ABC):
    def __init__(self):
        self.conn = None
        self.cur = None

    @abstractmethod
    def connect(self, *args, **kwargs):
        pass

    @abstractmethod
    def close(self):
        pass

    @abstractmethod
    def query(self, *args, **kwargs):
        pass