from abc import ABC, abstractmethod
import os


class ServiceInterfaceMixin(ABC):
    def __init__(self, *args, **kwargs):
        pass

    @abstractmethod
    def send(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def connect(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def disconnect(self, *args, **kwargs):
        raise NotImplementedError

    def _get_secret(self, value):
        return os.getenv(value)

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()
