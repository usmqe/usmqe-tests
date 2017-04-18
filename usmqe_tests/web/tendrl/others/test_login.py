"""
Description: Simple tests for log in on tendrl UI

Author: ltrilety
"""


import pytest
from selenium.webdriver.common.keys import Keys

from webstr.selenium.ui.support import WaitForWebstrPage
from usmqe.web.tendrl.loginpage import pages as loginpage
from usmqe.web.tendrl.mainpage.landing_page.pages import get_landing_page

LOGGER = pytest.get_logger('login_test', module=True)


def test_positive_login(testcase_set, testcase_end):
    """@usmid web/login_positive
    Login as valid user.
    """
    loginpage_inst = loginpage.LoginPage(
        testcase_set.driver,
        pytest.config.getini("usm_web_url"))
    LOGGER.debug("Fill valid credentials and log in")
    loginpage_inst.login_user(
        pytest.config.getini("usm_username"),
        pytest.config.getini("usm_password"))
    page_inst = get_landing_page(testcase_set.driver)
    # Following check is extra, could be removed
    pytest.check(
        page_inst.is_present,
        "A user should be logged in and main page should be present.")


@pytest.mark.parametrize(("username", "password", "error_message"), [
    ("none", "none", "The username or password you entered does not"
     " match our records. Please try again."),
    ("", "", None),
    (True, "", None),
    ("", True, None),
])
def test_negative_login(testcase_set, testcase_end,
                        username, password, error_message):
    """
    test negative login cases
    """
    if username is True:
        username = pytest.config.getini("usm_username")
    if password is True:
        password = pytest.config.getini("usm_password")
    loginpage_inst = loginpage.LoginPage(
        testcase_set.driver,
        pytest.config.getini("usm_web_url"))
    LOGGER.debug("Fill invalid credentials")
    loginpage_inst.fill_form_values(username, password)
    LOGGER.debug("Click on Log In button")
    loginpage_inst.get_model_element("login_btn").click()
    # check error message
    pytest.check(loginpage_inst.is_present, "Still on the login page")
    if error_message is not None:
        tmp_obj = loginpage_inst.get_model_element("error_label")
        pytest.check(tmp_obj.is_displayed(), "Error message is visible.")
        pytest.check(tmp_obj.text == error_message,
                     "Error message should be: {}".format(error_message))
        pytest.check(tmp_obj.get_attribute("class").index("alert-danger") > -1,
                     "Error message shoul be red.")


def test_login_positive_enter(testcase_set, testcase_end):
    """@usmid web/login_positive_enter
    Submit login form by "Enter" key
    """
    loginpage_inst = loginpage.LoginPage(
        testcase_set.driver,
        pytest.config.getini("usm_web_url"))
    LOGGER.debug("Fill valid credentials")
    loginpage_inst.fill_form_values(
        pytest.config.getini("usm_username"),
        pytest.config.getini("usm_password"))

    LOGGER.debug("Press Enter")
    loginpage_inst.get_model_element("password").send_keys(Keys.ENTER)
    WaitForWebstrPage(loginpage_inst, 10).to_disappear()
    page_inst = get_landing_page(testcase_set.driver)
    # Following check is extra, could be removed
    pytest.check(
        page_inst.is_present,
        "User should be logged in")
