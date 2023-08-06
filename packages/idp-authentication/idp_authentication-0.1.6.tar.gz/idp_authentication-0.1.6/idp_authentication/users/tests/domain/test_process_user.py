from dataclasses import asdict

import pytest

from idp_authentication import User, UserRole
from idp_authentication.conftest import TEST_PERMISSION, TEST_ROLE_1, TEST_ROLE_2


@pytest.mark.parametrize(
    "user,user_role,expected_role",
    [
        ("user", "test_role_3", "test_role_3"),
        ("user_2", "test_role_4", "test_role_4"),
    ],
    indirect=["user"],
)
def test_user_role_create(container, session, user, user_role, expected_role):
    process_user, user_as_dict = process_user_use_case(container, user, user_role)
    new_role = UserRole(role=user_role, app_entities_restrictions={}, user_id=user.id)
    user_as_dict["user_roles"] = new_role
    process_user.execute(user_as_dict)
    updated_user = session.query(User).filter(User.id == user.id).first()
    assert updated_user.user_roles[0].role == expected_role


@pytest.mark.parametrize(
    "user,user_role,expected_role",
    [
        ("user", TEST_ROLE_1, TEST_ROLE_1),
        ("user_2", TEST_ROLE_2, TEST_ROLE_2),
    ],
    indirect=["user"],
)
def test_user_role_update(container, session, user, user_role, expected_role):
    process_user, user_as_dict = process_user_use_case(container, user, user_role)
    process_user.execute(user_as_dict)
    updated_user = session.query(User).filter(User.id == user.id).first()

    assert updated_user.user_roles[0].role == expected_role


def test_process_user_deletes_user_roles_when_user_has_no_access_in_app(
    container, user
):
    # Arrange
    process_user, user_as_dict = process_user_use_case(
        container, user, TEST_ROLE_1, app_identifier="another_app"
    )

    # Act
    process_user.execute(user_as_dict)

    # Assert
    users_unit_of_work = container.users_module().users_unit_of_work()
    with users_unit_of_work:
        db_user = users_unit_of_work.user_repository.get_or_none(username=user.username)
        assert db_user.user_roles == []


def process_user_use_case(container, user, user_role, app_identifier="test"):
    process_user = container.users_module().use_cases().process_user_message_use_case()
    user_as_dict = asdict(user)
    user_as_dict["app_specific_configs"] = {
        app_identifier: {
            "default": {
                user_role: {
                    "app_entities_restrictions": {
                        "vehicle": [3],
                    },
                    "permission_restrictions": {TEST_PERMISSION: {"vehicle": [1, 2]}},
                }
            }
        }
    }
    return process_user, user_as_dict
