from typing import Any, Optional

from idp_authentication.enums import ChoiceEnum
from idp_authentication.users.base_classes.base_use_case import BaseUseCase, UseCasePort
from idp_authentication.users.domain.ports import unit_of_work


class AuthorizeOrGetAllAllowedRecordIdentifiersUseCase(BaseUseCase):
    def __init__(
        self,
        users_unit_of_work: unit_of_work.UsersUnitOfWorkPort,
        roles: ChoiceEnum,
        app_entity_types: list[str],
        authorize_app_entity_records_use_case: UseCasePort,
        get_allowed_record_identifiers_use_case: UseCasePort,
    ):
        super().__init__(
            users_unit_of_work=users_unit_of_work,
            roles=roles,
            app_entity_types=app_entity_types,
        )
        self.authorize_app_entity_records_use_case = (
            authorize_app_entity_records_use_case
        )
        self.get_allowed_record_identifiers_use_case = (
            get_allowed_record_identifiers_use_case
        )

    def execute(
        self,
        user,
        role: ChoiceEnum,
        app_entity_type: str,
        app_entity_records_identifiers: Optional[list[Any]],
        permission: str = None,
    ) -> list[Any]:
        """
        Make sure that the user can access the entity records being requested and return them.
        If no identifiers are being provided, return all allowed entity records.
        Args:
            user:                           The user performing the request
            role:                           The role that the user is acting as.
            app_entity_type:                The app entity being accessed
            app_entity_records_identifiers: The identifiers of the records belonging to the specified app entity
            permission:                     In case of specific permissions we can have permission restrictions
                                                through IDP. The value is the name of the permission
        Raises:
            PermissionDenied: In case the requested records are not allowed
        """

        if app_entity_records_identifiers:
            self.authorize_app_entity_records_use_case.execute(
                user=user,
                role=role,
                app_entity_type=app_entity_type,
                permission=permission,
                app_entity_records_identifiers=app_entity_records_identifiers,
            )
            return app_entity_records_identifiers
        else:
            return self.get_allowed_record_identifiers_use_case.execute(
                user=user,
                role=role,
                app_entity_type=app_entity_type,
                permission=permission,
            )
