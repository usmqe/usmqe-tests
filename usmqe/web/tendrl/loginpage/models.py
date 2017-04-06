"""
Common page model for login page.
"""


from webstr.core import WebstrModel, By, PageElement
from webstr.common.form import models as form


# part of url which is placed after 'usm_web_url'
# for getting on the described page in the module
LOCATION = None


class LoginPageModel(WebstrModel):
    """
    Common page model for the login page.
    """
    username = form.TextInput(by=By.ID, locator='username')
    password = form.PasswordInput(by=By.ID, locator='password')
    login_btn = form.Button(
        by=By.XPATH,
        locator='//*[contains(@class,"btn-lg")]')
    error_label = PageElement(
        by=By.XPATH,
        locator='//*[@ng-bind="loginCntrl.errorMsg"]/..')
