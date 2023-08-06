from abc import ABC, abstractmethod


class EventProducerPort(ABC):
    @abstractmethod
    def produce(self, topic: str, key: str, value: dict):
        """Produce"""
