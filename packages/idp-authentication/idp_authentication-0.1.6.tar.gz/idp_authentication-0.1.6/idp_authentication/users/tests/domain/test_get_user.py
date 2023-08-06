import pytest

from idp_authentication import User
from idp_authentication.exceptions import UserNotFound


def test_get_user_use_case(container, user):
    get_user_use_case = container.users_module().use_cases().get_user_use_case()
    get_user = get_user_use_case.execute(username=user.username)
    assert isinstance(get_user, User)
    assert get_user.username == user.username


def test_get_user_use_case_raises_error_on_invalid_username(container):
    get_user_use_case = container.users_module().use_cases().get_user_use_case()
    with pytest.raises(
        UserNotFound, match="User with username=invalid_username not found!"
    ):
        get_user_use_case.execute(username="invalid_username")
