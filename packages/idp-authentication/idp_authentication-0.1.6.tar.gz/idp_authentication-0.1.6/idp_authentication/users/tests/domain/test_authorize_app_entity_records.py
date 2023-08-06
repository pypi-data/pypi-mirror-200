import pytest

from idp_authentication.conftest import (
    TEST_PERMISSION,
    TEST_ROLE_1,
    VEHICLE_APP_ENTITY_IDENTIFIER,
)
from idp_authentication.exceptions import AccessDenied


@pytest.mark.parametrize(
    "app_entity_records_identifiers, permission",
    [
        ([1], None),
        ([1, 2], None),
        ([1], TEST_PERMISSION),
    ],
)
def test_authorize_app_entity_records_does_not_raise_error_on_valid_access(
    container, user, app_entity_records_identifiers, permission
):
    authorize_app_entity_records = (
        container.users_module().use_cases().authorize_app_entity_records_use_case()
    )
    authorize_app_entity_records.execute(
        user=user,
        role=TEST_ROLE_1,
        app_entity_type=VEHICLE_APP_ENTITY_IDENTIFIER,
        app_entity_records_identifiers=app_entity_records_identifiers,
        permission=permission,
    )


@pytest.mark.parametrize(
    "app_entity_records_identifiers, permission",
    [
        ([3], None),
        ([2], TEST_PERMISSION),
    ],
)
def test_authorize_app_entity_records_raises_error_on_invalid_access(
    container, user, app_entity_records_identifiers, permission
):
    authorize_app_entity_records = (
        container.users_module().use_cases().authorize_app_entity_records_use_case()
    )
    with pytest.raises(
        AccessDenied,
        match="You are not allowed to access the records in the requested entity",
    ):
        authorize_app_entity_records.execute(
            user=user,
            role=TEST_ROLE_1,
            app_entity_type=VEHICLE_APP_ENTITY_IDENTIFIER,
            app_entity_records_identifiers=app_entity_records_identifiers,
            permission=permission,
        )
