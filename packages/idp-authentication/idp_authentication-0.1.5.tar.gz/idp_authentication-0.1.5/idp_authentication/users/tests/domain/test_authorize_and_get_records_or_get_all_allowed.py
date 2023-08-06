import pytest

from idp_authentication.conftest import (
    TEST_PERMISSION,
    TEST_ROLE_1,
    TEST_ROLE_2,
    VEHICLE_APP_ENTITY_IDENTIFIER,
)
from idp_authentication.exceptions import AccessDenied


@pytest.mark.parametrize(
    "app_entity_records_identifiers, permission, role",
    [
        ([1], TEST_PERMISSION, TEST_ROLE_1),
        ([1, 2], None, TEST_ROLE_1),
    ],
)
def test_authorize_or_get_all_record_identifiers_use_case_does_not_raise_error_on_valid_access(
    container, user, app_entity_records_identifiers, permission, role
):
    authorize_or_get_all_record_identifiers_use_case = (
        container.users_module()
        .use_cases()
        .authorize_or_get_all_record_identifiers_use_case()
    )
    authorize_or_get_all_record_identifiers_use_case.execute(
        user=user,
        role=role,
        app_entity_type=VEHICLE_APP_ENTITY_IDENTIFIER,
        app_entity_records_identifiers=app_entity_records_identifiers,
        permission=permission,
    )


@pytest.mark.parametrize(
    "app_entity_records_identifiers, permission, role",
    [
        ([3], None, TEST_ROLE_1),
        ([2], TEST_PERMISSION, TEST_ROLE_1),
        ([1], None, TEST_ROLE_2),
    ],
)
def test_authorize_or_get_all_record_identifiers_use_case_raises_error_on_invalid_access(
    container, user, app_entity_records_identifiers, permission, role
):
    authorize_or_get_all_record_identifiers_use_case = (
        container.users_module()
        .use_cases()
        .authorize_or_get_all_record_identifiers_use_case()
    )
    with pytest.raises(
        AccessDenied,
        match="You are not allowed to access the records in the requested entity",
    ):
        authorize_or_get_all_record_identifiers_use_case.execute(
            user=user,
            role=role,
            app_entity_type=VEHICLE_APP_ENTITY_IDENTIFIER,
            app_entity_records_identifiers=app_entity_records_identifiers,
            permission=permission,
        )
