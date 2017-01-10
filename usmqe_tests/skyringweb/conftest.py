# vim: set tabstop=2 shiftwidth=2 softtabstop=2 colorcolumn=120:
"""
Webadmin specific test case functionality.

Author: pnovotny, ltrilety, mkudlej
"""


import pytest
LOGGER = pytest.get_logger('testcase', module=True)

from webstr.core import test
from selenium.common import exceptions as selenium_ex
from webstr.selenium.driver import Driver

from usmqe.web.skyring.loginpage import pages as loginpage


class CommonTestCase(test.UITestCase):
    """
    class similar to base UITestCase, only it will remember
    two additional informations

    Parameters:
        loginpage - LoginPage object instance
        navbar - NavMenuBars instance
    """
    loginpage = None
    navbar = None


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
    yield
    testcase_set.tear_down()


@pytest.fixture(scope="function")
def log_in(testcase_set):
    """
    All tests which don't need to tweak login process and expects that the default user is already logged in
    for the test to work should extend this class.
    """
    testcase_set.loginpage = loginpage.LoginPage(testcase_set.driver)
    testcase_set.navbar = testcase_set.loginpage.login_user(
        pytest.config.getini("usm_username"),
        pytest.config.getini("usm_password"))
    msg = "Navigation part of the main page should contain all required components."
    pytest.check(testcase_set.navbar.is_present, msg)
    yield testcase_set
