"""
Webadmin specific test case functionality.

Author: ltrilety
"""


import pytest

from usmqe.web.skyring.loginpage import pages as loginpage


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
    testcase_set.init_object = testcase_set.loginpage.login_user(
        pytest.config.getini("usm_username"),
        pytest.config.getini("usm_password"))
    msg = "Navigation part of the main page should contain all "\
        "required components."
    pytest.check(testcase_set.init_object.is_present, msg)
    yield testcase_set
