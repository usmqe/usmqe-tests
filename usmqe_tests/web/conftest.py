# vim: set tabstop=2 shiftwidth=2 softtabstop=2 colorcolumn=120:
"""
Webadmin specific test case functionality.

Author: pnovotny, ltrilety, mkudlej
"""


import pytest

from webstr.core import test


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
