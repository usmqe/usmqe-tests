# vim: set tabstop=2 shiftwidth=2 softtabstop=2 colorcolumn=120:
"""
Common page model for login page.
"""


import pytest

from webstr.core import WebstrModel, By, PageElement
from webstr.common.form import models as form


#location = pytest.config.getini("usm_web_url")


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
    #location = pytest.config.getini("usm_web_url")

    def __init__(self, driver):
        """
        Save the webdriver instance to attribute.

        Parameters:
            driver: webdriver instance
        """
        self.location = pytest.config.getini("usm_web_url")
        super(WebstrModel, self).__init__(driver)
