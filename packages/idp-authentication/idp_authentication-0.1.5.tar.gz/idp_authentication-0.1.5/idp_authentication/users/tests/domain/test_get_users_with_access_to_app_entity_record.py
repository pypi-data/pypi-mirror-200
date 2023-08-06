import pytest

from idp_authentication import UserRole
from idp_authentication.conftest import (
    TEST_ROLE_1,
    TEST_ROLE_2,
    VEHICLE_APP_ENTITY_IDENTIFIER,
)


@pytest.mark.parametrize(
    "role, app_entities_restrictions, has_access",
    [
        (TEST_ROLE_1, None, True),
        (TEST_ROLE_1, {VEHICLE_APP_ENTITY_IDENTIFIER: None}, True),
        (TEST_ROLE_1, {VEHICLE_APP_ENTITY_IDENTIFIER: [1, 2]}, True),
        (TEST_ROLE_1, {VEHICLE_APP_ENTITY_IDENTIFIER: [3, 4]}, False),
        (TEST_ROLE_1, {"other_entity": [1, 2]}, False),
        (TEST_ROLE_2, {VEHICLE_APP_ENTITY_IDENTIFIER: [1, 2]}, False),
    ],
)
def test_get_users_with_access_to_app_entity_record_use_case(
    container, make_user, role, app_entities_restrictions, has_access
):
    # Arrange
    user = make_user(
        user_roles=[
            UserRole(
                role=role,
                app_entities_restrictions=app_entities_restrictions,
            )
        ]
    )
    record_identifier = 1

    # Act
    user_with_access_to_app = (
        container.users_module()
        .use_cases()
        .get_users_with_access_to_app_entity_record_use_case()
    )
    users = user_with_access_to_app.execute(
        app_entity_type=VEHICLE_APP_ENTITY_IDENTIFIER,
        record_identifier=record_identifier,
        roles=[TEST_ROLE_1],
    )

    # Assert
    assert has_access is (user.id in [u.id for u in users])


def test_get_users_with_access_to_app_entity_record_use_case_does_not_return_inactive_users(
    container, make_user
):
    # Arrange
    record_identifier = 1
    user = make_user(
        is_active=False,
        user_roles=[
            UserRole(
                role=TEST_ROLE_1,
                app_entities_restrictions={
                    VEHICLE_APP_ENTITY_IDENTIFIER: [record_identifier]
                },
            )
        ],
    )

    # Act
    user_with_access_to_app = (
        container.users_module()
        .use_cases()
        .get_users_with_access_to_app_entity_record_use_case()
    )
    users = user_with_access_to_app.execute(
        app_entity_type=VEHICLE_APP_ENTITY_IDENTIFIER,
        record_identifier=record_identifier,
        roles=[TEST_ROLE_1],
    )

    # Assert
    assert user.id not in [u.id for u in users]
