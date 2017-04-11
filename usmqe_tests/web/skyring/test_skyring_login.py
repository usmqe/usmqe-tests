"""
Description: Simple log in test

Author: ltrilety
"""

import pytest

from selenium.webdriver.common.keys import Keys

from webstr.selenium.ui.support import WebDriverWait, WaitForWebstrPage

from usmqe.web.skyring.loginpage import pages as loginpage
from usmqe.web.skyring.mainpage.navpage import pages as navpage


# NOTE: example of test with log_in fixture used
#       it should not be run hence not in the name
def not_test_it(log_in, testcase_end):
    """ example of test with log_in fixture,
    with prepared log in outside of test
    """
    pytest.check(log_in.loginpage)
    pytest.check(log_in.init_object)


def test_positive_login(testcase_set, testcase_end):
    """@usmid web/login_positive
    Login as valid user.
    """
    loginpage_inst = loginpage.LoginPage(
        testcase_set.driver,
        pytest.config.getini("usm_web_url"))
    page_inst = loginpage_inst.login_user(
        pytest.config.getini("usm_username"),
        pytest.config.getini("usm_password"))
    pytest.check(
        page_inst.__class__.__name__ == 'NavMenuBars',
        "Login and wait for main page.")


@pytest.mark.parametrize(("username", "password", "error_message"), [
    ("none", "none", "Authentication Error!"),
    ("", "", "The username and password cannot be blank."),
    (True, "", "The username and password cannot be blank."),
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
    pytest.check(
        loginpage_inst.fill_form_values(username, password),
        "Fill bad credentials")
    loginpage_inst.get_model_element("login_btn").click()
    # check error message
    tmp_obj = loginpage_inst.get_model_element("error_label")
    pytest.check(tmp_obj.is_displayed(), "Error message is visible.")
    if error_message.startswith("Auth"):
        pytest.check(tmp_obj.text == error_message,
                     "Error message contains error text.",
                     issue="Not needed trailing dot.")
    else:
        pytest.check(tmp_obj.text == error_message,
                     "Error message contains error text.")
    pytest.check(tmp_obj.get_attribute("class").index("alert-danger") > -1,
                 "Error message is red.")


def test_login_positive_enter(testcase_set, testcase_end):
    """@usmid web/login_positive_enter
    Submit login form by "Enter" key
    """
    loginpage_inst = loginpage.LoginPage(
        testcase_set.driver,
        pytest.config.getini("usm_web_url"))
    pytest.check(
        loginpage_inst.fill_form_values(
            pytest.config.getini("usm_username"),
            pytest.config.getini("usm_password")),
        "Fill form for submit by enter.")

    loginpage_inst.get_model_element("password").send_keys(Keys.ENTER)
    # TODO https://github.com/skyrings/kitoon/issues/94
    # https://bugzilla.redhat.com/show_bug.cgi?id=1298539
    WaitForWebstrPage(loginpage_inst, 10).to_disappear()
    navpag = navpage.NavMenuBars(testcase_set.driver)
    pytest.check(
        WebDriverWait(navpag, timeout=10).until(
            lambda navpag: navpag.get_model_element("navbar_brand")),
        "Wait for navpage")
