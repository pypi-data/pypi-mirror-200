from idp_authentication.users.adapters.repositories.user_repository import (
    UserRepository,
)
from idp_authentication.users.adapters.repositories.user_role_repository import (
    UserRoleRepository,
)
from idp_authentication.users.base_classes.base_unit_of_work import BaseUnitOfWork
from idp_authentication.users.domain.ports.repository import (
    UserRepositoryPort,
    UserRoleRepositoryPort,
)
from idp_authentication.users.domain.ports.unit_of_work import UsersUnitOfWorkPort


class UsersUnitOfWork(BaseUnitOfWork, UsersUnitOfWorkPort):
    user_repository: UserRepositoryPort
    user_role_repository: UserRoleRepositoryPort

    def __enter__(self):
        super().__enter__()

        self.user_repository = UserRepository(self.session)
        self.user_role_repository = UserRoleRepository(self.session)

        return self
