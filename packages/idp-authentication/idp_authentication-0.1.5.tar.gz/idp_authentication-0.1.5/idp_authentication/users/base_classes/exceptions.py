from abc import ABC, abstractmethod


class ExceptionBase(Exception, ABC):
    def __init__(self, message, metadata=None):
        super().__init__(message)
        self.message = message
        self.metadata = metadata

    def __str__(self):
        return self.message

    @property
    @abstractmethod
    def code(self) -> str:
        """code must be implemented by subclass"""

    def to_dictionary(self) -> dict:
        return {"message": self.message, "code": self.code, "metadata": self.metadata}
