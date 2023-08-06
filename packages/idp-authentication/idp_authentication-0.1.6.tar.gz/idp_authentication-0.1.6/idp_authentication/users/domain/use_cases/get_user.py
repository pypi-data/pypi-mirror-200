from idp_authentication.exceptions import UserNotFound
from idp_authentication.users.base_classes.base_use_case import UseCasePort
from idp_authentication.users.domain.entities.user import User
from idp_authentication.users.domain.ports.unit_of_work import UsersUnitOfWorkPort


class GetUserUseCase(UseCasePort):
    """
    Get user by idp_user_id.
    """

    def __init__(self, users_unit_of_work: UsersUnitOfWorkPort):
        self.users_unit_of_work = users_unit_of_work

    def execute(self, /, username: str) -> User:
        """Get user by username."""
        with self.users_unit_of_work as uow:
            user: User = uow.user_repository.get_first(username=username)
            if user is None:
                raise UserNotFound(username)

            return user
