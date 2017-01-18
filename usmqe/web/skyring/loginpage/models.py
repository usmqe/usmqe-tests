"""
Common page model for login page.
"""


import pytest

from webstr.core import WebstrModel, By, PageElement
from webstr.common.form import models as form


# part of url which is placed after 'usm_web_url'
# for getting on the described page in the module
LOCATION = None


class LoginPageModel(WebstrModel):
    """
    Common page model for the login page.
    """
    username = form.TextInput(by=By.ID, locator='inputUsername')
    password = form.PasswordInput(by=By.ID, locator='inputPassword')
    login_btn = form.Button(
        by=By.XPATH,
        locator='//*[@class="btn btn-primary btn-lg"]')
    error_label = PageElement(
        by=By.XPATH,
        locator='//*[@ng-bind="login.errorMsg"]/..')
