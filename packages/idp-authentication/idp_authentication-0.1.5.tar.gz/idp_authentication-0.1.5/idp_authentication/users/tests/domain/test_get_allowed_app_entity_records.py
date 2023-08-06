from idp_authentication.conftest import (
    TEST_PERMISSION,
    TEST_ROLE_1,
    VEHICLE_APP_ENTITY_IDENTIFIER,
)


def test_get_allowed_app_entity_records_with_permission(container, user):
    get_allowed_app_entity_records = (
        container.users_module().use_cases().get_allowed_record_identifiers_use_case()
    )
    records = get_allowed_app_entity_records.execute(
        user=user,
        role=TEST_ROLE_1,
        app_entity_type=VEHICLE_APP_ENTITY_IDENTIFIER,
        permission=TEST_PERMISSION,
    )
    assert len(records) > 0


def test_get_allowed_app_entity_records_with_no_permission(container, user_2):
    get_allowed_app_entity_records = (
        container.users_module().use_cases().get_allowed_record_identifiers_use_case()
    )
    records = get_allowed_app_entity_records.execute(
        user=user_2,
        role=TEST_ROLE_1,
        app_entity_type=VEHICLE_APP_ENTITY_IDENTIFIER,
        permission=None,
    )
    assert len(records) == 0
