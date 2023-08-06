from idp_authentication.enums import ChoiceEnum
from idp_authentication.users.base_classes.base_use_case import BaseUseCase


class GetAllowedRecordIdentifiersUseCase(BaseUseCase):
    """Get allowed app entity records identifiers use case."""

    def execute(
        self, user, role: ChoiceEnum, app_entity_type: str, permission: str = None
    ):
        return self._get_allowed_app_entity_records_identifiers(
            user=user,
            role=role,
            app_entity_type=app_entity_type,
            permission=permission,
        )
