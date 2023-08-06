import abc
from typing import Any, Literal

from idp_authentication.custom_types import ALL
from idp_authentication.enums import ChoiceEnum
from idp_authentication.users.domain.ports.unit_of_work import UsersUnitOfWorkPort


class UseCasePort(abc.ABC):
    @abc.abstractmethod
    def execute(self, *args, **kwargs):
        """Execute the use case."""


class BaseUseCase(UseCasePort):
    def __init__(
        self,
        users_unit_of_work: UsersUnitOfWorkPort,
        roles: ChoiceEnum,
        app_entity_types: list[str],
    ):
        self.users_unit_of_work = users_unit_of_work
        self.roles = roles
        self.app_entity_types = app_entity_types

    @abc.abstractmethod
    def execute(self, *args, **kwargs):
        """Execute the use case."""

    def _verify_app_entity_type(self, app_entity_type: str):
        assert (
            app_entity_type in self.app_entity_types
        ), f"App Entity type does not exist: {app_entity_type}"

    def _verify_role(self, role: ChoiceEnum):
        assert role in self.roles, f"Role does not exist: {role}"

    def _get_allowed_app_entity_records_identifiers(
        self,
        user,
        role: ChoiceEnum,
        app_entity_type: str,
        permission: str = None,
    ) -> list[Any] | Literal[ALL]:
        """
        Gets the identifiers of the app entity records that the user can access.
        If no restriction both on role and permission level, return '__all__'
        Args:
            user:               The user performing the request
            role:               The role that the user is acting as.
            app_entity_type:    The app entity being accessed
            permission:         In case of specific permissions we can have permission restrictions
                                    through IDP. The value is the name of the permission
        Returns:
            List of identifiers of App Entity Records that the user can access
        """

        with self.users_unit_of_work as uow:
            self._verify_role(role)
            self._verify_app_entity_type(app_entity_type)

            user_role = uow.user_role_repository.get_first(user_id=user.id, role=role)
            if not user_role:
                return []

            # Permission restriction get precedence, if existing, for the given app_entity
            if permission:
                permission_restrictions = user_role.permission_restrictions
                if (
                    permission_restrictions
                    and permission in permission_restrictions.keys()
                ):
                    permission_restriction = permission_restrictions.get(permission)
                    if permission_app_entity_restriction := permission_restriction.get(
                        app_entity_type
                    ):
                        return permission_app_entity_restriction

            # Verify if there is any restriction on the entity for the user
            app_entities_restrictions = user_role.app_entities_restrictions
            if app_entities_restrictions and (
                app_entity_restriction := app_entities_restrictions.get(app_entity_type)
            ):
                return app_entity_restriction

            return ALL
