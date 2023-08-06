from idp_authentication.users.base_classes.base_repository import BaseRepository
from idp_authentication.users.domain.entities import UserRole
from idp_authentication.users.domain.ports.repository import UserRoleRepositoryPort


class UserRoleRepository(BaseRepository, UserRoleRepositoryPort):
    entity = UserRole
