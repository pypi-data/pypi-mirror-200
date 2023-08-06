from typing import Any, List

from idp_authentication.custom_types import ALL
from idp_authentication.enums import ChoiceEnum
from idp_authentication.exceptions import AccessDenied
from idp_authentication.users.base_classes.base_use_case import BaseUseCase


class AuthorizeEntityRecordsUseCase(BaseUseCase):
    def execute(
        self,
        user,
        role: ChoiceEnum,
        app_entity_type: str,
        app_entity_records_identifiers: List[Any],
        permission: str = None,
    ):
        """
        Verify if the user has access to the requested entity records.
        If a permission is specified, and it has restrictable=True, the access is verified based on it.
        Args:
            user:                           The user performing the request
            role:                           The role that the user is acting as.
            app_entity_type:                The app entity being accessed
            app_entity_records_identifiers: The identifiers of the records belonging to the specified app entity
            permission:                     In case of specific permissions we can have permission restrictions
                                                through IDP. The value is the name of the permission
        Raises:
            AccessDenied: In case the requested records are not allowed
        """

        allowed_app_entity_records_identifiers = (
            self._get_allowed_app_entity_records_identifiers(
                user=user,
                role=role,
                app_entity_type=app_entity_type,
                permission=permission,
            )
        )

        if allowed_app_entity_records_identifiers == ALL:
            return

        if not set(app_entity_records_identifiers).issubset(
            set(allowed_app_entity_records_identifiers)
        ):
            raise AccessDenied(
                "You are not allowed to access the records in the requested entity!"
            )
