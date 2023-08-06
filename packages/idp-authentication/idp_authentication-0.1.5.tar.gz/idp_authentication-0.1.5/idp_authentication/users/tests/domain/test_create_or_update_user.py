def test_create_user(container):
    data = {
        "username": "test0",
        "email": "test0@gmail.com",
        "first_name": "test",
        "last_name": "test",
    }
    create_user_use_case = (
        container.users_module().use_cases().create_or_update_user_use_case()
    )
    created_user = create_user_use_case.execute(data=data)
    assert created_user.username == data["username"]

    users_unit_of_work = container.users_module().users_unit_of_work()
    with users_unit_of_work:
        inserted_user = users_unit_of_work.user_repository.get_or_none(
            username=data["username"]
        )
        assert inserted_user is not None


def test_update_user(container, user):
    data = {
        "username": "test1",
        "email": "test@cardoai.com",
        "first_name": "test",
        "last_name": "test",
    }
    previous_user_email = user.email
    update_user_use_case = (
        container.users_module().use_cases().create_or_update_user_use_case()
    )
    updated_user = update_user_use_case.execute(data=data)
    assert previous_user_email != updated_user.email

    users_unit_of_work = container.users_module().users_unit_of_work()
    with users_unit_of_work as uow:
        db_user = uow.user_repository.get_or_none(username=data["username"])
        assert db_user.email == data["email"]
