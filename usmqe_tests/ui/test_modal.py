import pytest
from usmqe.base.application.implementations.web_ui import ViaWebUI
from usmqe.base.application import Application
#LOGGER = pytest.get_logger('ui_user_testing', module=True)
import time
import copy
import json

from usmqe.base.application.views.common import BaseLoggedInView

from usmqe.api.tendrlapi import user as tendrlapi_user
from usmqe.api.tendrlapi.common import login, logout


def test_modal(application):
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
    user = application.collections.users.create(
        user_id="{}_user_auto".format(role),
        name="{} user".format(role),
        email="{}user@tendrl.org".format(role),
        notifications_on=False,
        password="1234567890",
        role=role
    )
    '''user_data = {
        "name": user.user_id,
        "username": user.name,
        "email": user.email,
        "role": user.role,
        "password": user.password,
        "email_notifications": user.notifications_on}'''
    temp_app = Application(hostname="ebondare-usm1-server.usmqe.lab.eng.brq.redhat.com", 
                           scheme="http", 
                           username=user.user_id, 
                           password=user.password)
    
    view = ViaWebUI.navigate_to(temp_app.web_ui, "LoggedIn")
    modal_info = {"Version": "3.4",
                  "User": user.name,
                  "User Role": user.role,
                  "Browser": "chrome",
                  "Browser OS": "linux"}
    for key in modal_info:
        real_value = view.get_detail(key).lower()
        assert real_value == modal_info[key]

    temp_app.web_ui.browser_manager.quit()    
    user.delete()
    assert not user.exists
