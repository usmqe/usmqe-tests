import pytest
from usmqe.base.application.implementations.web_ui import ViaWebUI
#LOGGER = pytest.get_logger('ui_user_testing', module=True)
import time


@pytest.mark.parametrize("role", ["normal"])
def test_user_crud(application, role):
    user = application.collections.users.create(
        user_id="{}_user_auto".format(role),
        name="{} user".format(role),
        email="{}user@tendrl.org".format(role),
        notifications_on=True,
        password="1234567890",
        role=role
    )
    assert user.exists
    user.edit({
              "user_id": user.user_id,
              "users_name": user.name,
              "email": "edited_email_for_{}@tendrl.org".format(role),
              "password": user.password,
              "confirm_password": user.password,
              })
    user.email = "edited_email_for_{}@tendrl.org".format(role)
    assert user.exists
    user.delete()
    assert not user.exists

