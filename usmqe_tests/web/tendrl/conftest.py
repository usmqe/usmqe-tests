"""
Webadmin specific test case functionality.

Author: ltrilety
"""


import pytest

from usmqe.web.tendrl.loginpage import pages as loginpage
from usmqe.web.tendrl.mainpage.landing_page.pages import get_landing_page
from usmqe.web.tendrl.auxiliary.pages import UpperMenu


@pytest.fixture(scope="function")
def log_in(testcase_set):
    """
    All tests which don't need to tweak login process and expects
    that the default user is already logged in
    for the test to work should extend this class.
    """
    testcase_set.loginpage = loginpage.LoginPage(
        testcase_set.driver,
        pytest.config.getini("usm_web_url"))
    testcase_set.loginpage.login_user(
        pytest.config.getini("usm_username"),
        pytest.config.getini("usm_password"))
    testcase_set.init_object = get_landing_page(testcase_set.driver)
    msg = "Initial element - Home page or navigation part of the main page "\
        "should contain all required components."
    pytest.check(testcase_set.init_object.is_present, msg)
    yield testcase_set


@pytest.fixture(scope="function")
def log_out(testcase_end):
    """ fixture for logging out """
    yield testcase_end
    if testcase_end.init_object is None:
        upper_menu = UpperMenu(testcase_end.driver)
        user_menu = upper_menu.open_user_menu()
    else:
        user_menu = testcase_end.init_object.open_user_menu()
    user_menu.logout()
