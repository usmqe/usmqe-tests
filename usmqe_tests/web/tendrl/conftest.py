"""
Webadmin specific test case functionality.

Author: ltrilety
"""


import pytest

# Coming soon ...
# from usmqe.web.tendrl.loginpage import pages as loginpage
from usmqe.web.tendrl.mainpage.landing_page.pages import get_landing_page


@pytest.fixture(scope="function")
def log_in(testcase_set):
    """
    All tests which don't need to tweak login process and expects
    that the default user is already logged in
    for the test to work should extend this class.
    """
# NOTE: For now it just solves the landing page - no log in
#       Remove following line when log in is done
# TODO
# https://github.com/Tendrl/specifications/issues/128
    testcase_set.driver.get(pytest.config.getini("usm_web_url"))
    testcase_set.init_object = get_landing_page(testcase_set.driver)
    msg = "Initial element - Home page or navigation part of the main page "\
        "should contain all required components."
    pytest.check(testcase_set.init_object.is_present, msg)
    yield testcase_set
