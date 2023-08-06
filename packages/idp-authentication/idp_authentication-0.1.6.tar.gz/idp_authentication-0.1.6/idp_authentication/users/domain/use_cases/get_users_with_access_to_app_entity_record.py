from typing import Any

from idp_authentication.enums import ChoiceEnum
from idp_authentication.users.base_classes.base_use_case import BaseUseCase


class GetUsersWithAccessToAppEntityRecordUseCase(BaseUseCase):
    def execute(
        self,
        app_entity_type: str,
        record_identifier: Any,
        roles: list[ChoiceEnum | str],
    ):
        self._verify_app_entity_type(app_entity_type)
        for role in roles:
            self._verify_role(role)

        with self.users_unit_of_work as uow:
            return uow.user_repository.get_users_with_access_to_records(
                app_entity_type=app_entity_type,
                record_identifier=record_identifier,
                roles=roles,
            )
