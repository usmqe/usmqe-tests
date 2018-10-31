import pytest

#LOGGER = pytest.get_logger('ui_user_testing', module=True)


@pytest.mark.parametrize("role", ["normal", "limited"])
def test_user_crud(application, role):
    user = application.collections.users.create(
        user_id="{}_user_auto".format(role),
        name="Autotest {} User".format(role),
        email="{}user@tendrl.org".format(role),
        notifications_on=True,
        password="1234567890",
        role=role
    )
    assert user.exists
    user.delete()
    assert not user.exists

