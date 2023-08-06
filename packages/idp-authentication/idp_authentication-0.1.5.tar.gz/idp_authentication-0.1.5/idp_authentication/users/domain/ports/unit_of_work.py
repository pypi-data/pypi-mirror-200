from abc import ABC, abstractmethod

from idp_authentication.users.domain.ports.repository import (
    UserRepositoryPort,
    UserRoleRepositoryPort,
)
from idp_authentication.users.domain.ports.session import SessionPort


class UnitOfWorkPort(ABC):
    session: SessionPort

    def __enter__(self):
        """To implement"""

    def __exit__(self, *args):
        """To implement"""

    @abstractmethod
    def commit(self):
        """Commit"""

    @abstractmethod
    def rollback(self):
        """Rollback"""


class UsersUnitOfWorkPort(UnitOfWorkPort, ABC):
    user_repository: UserRepositoryPort
    user_role_repository: UserRoleRepositoryPort
