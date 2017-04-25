"""
Webadmin specific test case functionality.

Author: ltrilety
"""


import pytest

from webstr.core import test
from usmqe.web.tendrl.loginpage import pages as loginpage
from usmqe.web.tendrl.landing_page.pages import get_landing_page
from usmqe.web.tendrl.auxiliary.pages import UpperMenu


class CommonTestCase(test.UITestCase):
    """
    class similar to base UITestCase, only it will remember
    two additional informations

    Atributes:
        loginpage - LoginPage object instance
        init_object - Initial page deputy instance
    """
    loginpage = None
    init_object = None


@pytest.fixture(scope="function", autouse=True)
def testcase_set():
    """
    open browser
    """
    testcase = CommonTestCase()
    testcase.set_up()
    yield testcase


@pytest.fixture(scope="function")
def testcase_end(testcase_set):
    """
    close browser
    """
    yield testcase_set
    testcase_set.tear_down()


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
    upper_menu = UpperMenu(testcase_end.driver)
    user_menu = upper_menu.open_user_menu()
    user_menu.logout()


@pytest.fixture(scope="function")
def valid_credentials(log_in, log_out):
    """
    Similar as for API valid_session_credentials,
    this fixture takes care about authentication.
    Login default usmqe user account (username and password comes
    from usm.ini config file).
    There is a difference with API though
        - the fixture is not valid for the whole session
          user is logged in at the test begin and log out when the test ends
    """
    yield log_in
