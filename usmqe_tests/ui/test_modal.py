import pytest
from usmqe.base.application.implementations.web_ui import ViaWebUI
from usmqe.base.application import Application


def test_modal(application):
    """
    Test admin's About modal
    """
    """
    :step:
      Log in as admin and check the modal contents
    :result:
      About modal shows valid information described in
      https://bugzilla.redhat.com/show_bug.cgi?id=1627988
    """
    view = ViaWebUI.navigate_to(application.web_ui, "LoggedIn")
    modal_info = {"Version": "3.4",
                  "User": "admin",
                  "User Role": "admin",
                  "Browser": "chrome",
                  "Browser OS": "linux"}
    for key in modal_info:
        real_value = view.get_detail(key).lower()
        assert real_value == modal_info[key]


@pytest.mark.parametrize("role", ["normal", "limited"])
def test_modal_username_role(application, role, valid_session_credentials):
    """
    Test normal and limited users' About modal
    """
    """
    :step:
      Create normal or limited user
    :result:
      Normal or limited user is created
    """
    user = application.collections.users.create(
        user_id="{}_user_auto".format(role),
        name="{} user".format(role),
        email="{}user@tendrl.org".format(role),
        notifications_on=False,
        password="1234567890",
        role=role)
    temp_app = Application(hostname="ebondare-usm1-server.usmqe.lab.eng.brq.redhat.com",
                           scheme="http",
                           username=user.user_id,
                           password=user.password)
    """
    :step:
      Log in as normal or limited user and check the modal contents
    :result:
      About modal shows valid information described in
      https://bugzilla.redhat.com/show_bug.cgi?id=1627988
    """
    view = ViaWebUI.navigate_to(temp_app.web_ui, "LoggedIn")
    modal_info = {"Version": "3.4",
                  "User": user.name,
                  "User Role": user.role,
                  "Browser": "chrome",
                  "Browser OS": "linux"}
    for key in modal_info:
        real_value = view.get_detail(key).lower()
        assert real_value == modal_info[key]
    user.delete()
    assert not user.exists
