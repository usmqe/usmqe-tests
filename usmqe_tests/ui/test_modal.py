import pytest
from usmqe.base.application.implementations.web_ui import ViaWebUI
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
