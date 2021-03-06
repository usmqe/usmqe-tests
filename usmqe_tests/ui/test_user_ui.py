import pytest
from usmqe.web.application.implementations.web_ui import ViaWebUI
import copy
from wait_for import TimedOutError
from urllib.parse import urlparse

from usmqe.api.tendrlapi import user as tendrlapi_user
from usmqe.web.application import Application
from usmqe.usmqeconfig import UsmConfig


CONF = UsmConfig()


@pytest.mark.testready
@pytest.mark.author("ebondare@redhat.com")
@pytest.mark.happypath
@pytest.mark.parametrize("role", ["normal", "limited"])
def test_user_crud(application, role, valid_session_credentials):
    """
    Create, edit and delete normal and limited user.
    """
    """
    :step:
      Create user
    :result:
      User is created
    """
    user = application.collections.users.create(
        user_id="{}_user_auto".format(role),
        name="{} user".format(role),
        email="{}user@example.com".format(role),
        notifications_on=False,
        password="1234567890",
        role=role
    )
    pytest.check(user.exists,
                 "Check that new user can be found on UI Users page")
    test = tendrlapi_user.ApiUser(auth=valid_session_credentials)
    user_data = {
        "name": user.name,
        "username": user.user_id,
        "email": user.email,
        "role": user.role,
        "email_notifications": user.notifications_on}

    test.check_user(user_data)
    """
    :step:
      Edit user's email address and notification settings
    :result:
      User is edited
    """
    user.edit({
              "user_id": user.user_id,
              "name": user.name,
              "email": "edited_email_for_{}@example.com".format(role),
              "password": user.password,
              "confirm_password": user.password,
              "notifications_on": True
              })
    pytest.check(user.exists,
                 "Check that edited user can be found on UI Users page")
    pytest.check(user.email == "edited_email_for_{}@example.com".format(role),
                 "Check that user's e-mail has been edited")
    pytest.check(user.notifications_on,
                 "Check that user's notification settings have been edited")
    user_data["email"] = "edited_email_for_{}@example.com".format(role)
    user_data["email_notifications"] = True
    test.check_user(user_data)
    """
    :step:
      Log in as the edited user
    :result:
      User can log in
    """
    url = urlparse(CONF.config["usmqe"]["web_url"])
    app2 = Application(hostname=url.hostname,
                       scheme=url.scheme,
                       username=user.user_id,
                       password=user.password)
    ViaWebUI.navigate_to(app2.web_ui, "LoggedIn")
    app2.web_ui.browser_manager.quit()

    """
    :step:
      Delete user
    :result:
      User is deleted
    """
    user.delete()
    pytest.check(not user.exists,
                 "Check that user can't be found on UI Users page anymore.")


@pytest.mark.testready
@pytest.mark.author("ebondare@redhat.com")
@pytest.mark.negative
def test_user_creation_password_invalid(application, valid_session_credentials,
                                        valid_normal_user_data, invalid_password):
    """
    Attempt to create a user with an invalid password.
    """
    """
    :step:
      Attempt to add user with invalid password.
    :result:
      User is not created.
    """
    user = application.collections.users.create(
        user_id=valid_normal_user_data["username"],
        name=valid_normal_user_data["name"],
        email=valid_normal_user_data["email"],
        notifications_on=valid_normal_user_data["email_notifications"],
        password=invalid_password,
        role=valid_normal_user_data["role"]
    )
    pytest.check(not user.exists,
                 "Check that new user can't be found on UI Users page")
    """
    :step:
      Check that user hasn't been created using API
    :result:
      There's no user with the specified username
    """
    test = tendrlapi_user.ApiUser(auth=valid_session_credentials)
    user_data_password_invalid = copy.deepcopy(valid_normal_user_data)
    user_data_password_invalid["password"] = invalid_password
    asserts = {
        "ok": False,
        "reason": 'Not Found',
        "status": 404}
    not_found = test.get_user(user_data_password_invalid["username"], asserts_in=asserts)
    pytest.check("Not found" in str(not_found),
                 "Check that new user can't be found using API")


@pytest.mark.testready
@pytest.mark.author("ebondare@redhat.com")
@pytest.mark.happypath
def test_edit_email_password(valid_new_normal_user, valid_password):
    """
    Change user's password and email in My Settings and login with new password.
    """
    """
    :step:
      Log in and edit user's email and password in My Settings
    :result:
      User's email and password are changed
    """
    url = urlparse(CONF.config["usmqe"]["web_url"])
    app1 = Application(hostname=url.hostname,
                       scheme=url.scheme,
                       username=valid_new_normal_user["username"],
                       password=valid_new_normal_user["password"])
    ViaWebUI.navigate_to(app1.web_ui, "LoggedIn")
    new_data = {"email": "new_user_email@example.com",
                "password": valid_password,
                "confirm_password": valid_password}
    app1.collections.users.edit_logged_in_user(new_data)
    """
    :step:
      Log in using the new passord
    :result:
      User is able to log in with the new password
    """
    app1.web_ui.browser_manager.quit()
    app2 = Application(hostname=url.hostname,
                       scheme=url.scheme,
                       username=valid_new_normal_user["username"],
                       password=valid_password)
    ViaWebUI.navigate_to(app2.web_ui, "LoggedIn")
    app2.web_ui.browser_manager.quit()


@pytest.mark.testready
@pytest.mark.author("ebondare@redhat.com")
@pytest.mark.happypath
def test_edit_email_only(valid_new_normal_user):
    """
    Change user's email in My Settings and login again.
    Fails due to https://bugzilla.redhat.com/show_bug.cgi?id=1654623
    """
    """
    :step:
      Log in and edit user's email in My Settings
    :result:
      User's email is changed
    """
    url = urlparse(CONF.config["usmqe"]["web_url"])
    app1 = Application(hostname=url.hostname,
                       scheme=url.scheme,
                       username=valid_new_normal_user["username"],
                       password=valid_new_normal_user["password"])
    ViaWebUI.navigate_to(app1.web_ui, "LoggedIn")
    new_data = {"email": "new_user_email@example.com"}
    app1.collections.users.edit_logged_in_user(new_data)
    app1.web_ui.browser_manager.quit()
    """
    :step:
      Log in using the old password
    :result:
      User is able to log in with the old password.
      Fails due to https://bugzilla.redhat.com/show_bug.cgi?id=1654623
    """
    app2 = Application(hostname=url.hostname,
                       scheme=url.scheme,
                       username=valid_new_normal_user["username"],
                       password=valid_new_normal_user["password"])
    try:
        ViaWebUI.navigate_to(app2.web_ui, "LoggedIn")
        app2.web_ui.browser_manager.quit()
    except TimedOutError:
        pytest.check(False,
                     issue='https://bugzilla.redhat.com/show_bug.cgi?id=1654623')
