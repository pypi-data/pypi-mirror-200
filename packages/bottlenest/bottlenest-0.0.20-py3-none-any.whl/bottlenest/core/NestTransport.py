from abc import ABC, abstractmethod


class NestTransport(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def getTransportKey(self):
        pass
