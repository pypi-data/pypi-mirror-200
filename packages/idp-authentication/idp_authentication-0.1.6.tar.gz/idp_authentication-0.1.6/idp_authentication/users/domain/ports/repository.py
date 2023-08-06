import abc
from typing import Any

from idp_authentication.enums import ChoiceEnum
from idp_authentication.users.domain.entities.user import User


class RepositoryPort(abc.ABC):
    @abc.abstractmethod
    def get_or_none(self, **kwargs) -> User:
        """Get a record by its attributes."""

    @abc.abstractmethod
    def get_first(self, **filters):
        """Get the first record, after applying filters"""

    @abc.abstractmethod
    def all(self):
        """Get all records"""

    @abc.abstractmethod
    def create(self, **kwargs):
        """Create a new record."""

    @abc.abstractmethod
    def update_record(self, record, **kwargs):
        """Update a record."""


class UserRepositoryPort(RepositoryPort, abc.ABC):
    """User repository port."""

    @abc.abstractmethod
    def get_users_with_access_to_records(
        self,
        app_entity_type: str,
        record_identifier: Any,
        roles: list[ChoiceEnum | str],
    ) -> list[User]:
        """Get users with access to records."""

    @abc.abstractmethod
    def remove_user_role(self, user, role):
        """Remove user role."""


class UserRoleRepositoryPort(RepositoryPort, abc.ABC):
    """User role repository port."""

    @abc.abstractmethod
    def delete(self, record):
        """Delete a record."""
