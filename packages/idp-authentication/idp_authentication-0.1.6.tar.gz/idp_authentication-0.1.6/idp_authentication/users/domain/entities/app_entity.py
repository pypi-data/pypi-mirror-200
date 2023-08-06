from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class AppEntity(ABC):
    """Base class for all entities that are part of an application."""

    @property
    @abstractmethod
    def idp_identifier(self):
        """Returns the identifier attribute of the app entity."""

    @property
    @abstractmethod
    def idp_label(self):
        """Returns the label attribute of the app entity."""

    @property
    def entity_type(self):
        """
        Returns the entity type of the app entity.
        By default, this is the class name of the app entity, to lower.
        Can be overridden in subclasses.
        """
        return self.__class__.__name__.lower()
