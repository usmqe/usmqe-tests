"""
Some usefull methods and classes for common work with web
"""

from selenium.common import exceptions as selenium_ex
from webstr.selenium.driver import Driver
from webstr.core import BaseWebElementHelper, PageElement


def refresh_driver(testcase, relogin=False):
    """
    Reload page or log again and go back to the volumes tab
    if reload of the page fails because there is no page present
    it logs again anyway

    Atributes:
        testcase - instance of webstr.core.test.UITestCase
        relogin - reload driver and log again

    Returns:
        True if log in was done, False otherwise
    """
    if relogin:
        try:
            testcase.tear_down()
        except selenium_ex.WebDriverException:
            Driver.destroy_default_driver()
        testcase.set_up()
        return True
    else:
        try:
            testcase.driver.refresh()
            return False
        except selenium_ex.WebDriverException:
            # if it fails log again
            Driver.destroy_default_driver()
            testcase.set_up()
            return True


class StatusIconHelper(BaseWebElementHelper):
    """
    StatusIcon helper (Selenium webelement wrapper).
    Provides basic methods for manipulation with a status icon.
    """

    @property
    def value(self):
        """
        find status

        Returns:
            value of title attribute of the StatusIcon element
        """
        return self.get_attribute('title')


class StatusIcon(PageElement):
    """
    Page element for a status icon.
    """
    _helper = StatusIconHelper
