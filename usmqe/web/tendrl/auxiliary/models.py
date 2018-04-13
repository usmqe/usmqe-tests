"""
Some usefull model classes for common work with tendrl web
"""

from webstr.core import WebstrModel, By, PageElement, RootPageElement,\
    DynamicWebstrModel, DynamicPageElement
from webstr.common.form import models as form
#
# from usmqe.web.utils import StatusIcon


class BaseListMenuModel(DynamicWebstrModel):
    """
    base auxiliary model for list menu (filter and order fields)
    """

    def __init__(self, driver):
        """
        Initialize the ListMenu instance

        Parameters:
            driver: webdriver instance
            name: page model instance name; this name is used for identifying
                  single instance along others, e.g., single VM in the VM list
        """
        super(DynamicWebstrModel, self).__init__(driver)
        self._link_text = ""

    def __setattr__(self, name, value):
        """ setter for link_text """
        if name == 'link_text':
            name = '_link_text'
        super(BaseListMenuModel, self).__setattr__(name, value)

    @property
    def _instance_identifier(self):
        """
        Page model instance identifier.

        Property method whose return value is used for string interpolation
        of locators of all dynamic elements.
        """
        return self._link_text


class FilterListMenuModel(BaseListMenuModel):
    """
    auxiliary model for list menu (filter and order fields)

    NOTE: Click on filter_by and order_by opens a menu with some links
          such links has will be instanced from Page object
          a _link_text parameter will be used
          e.g. name = PageElement(by=By.LINK_TEXT, locator="Name")
    """
    filter_by = form.Button(
        By.XPATH,
        '//button[contains(translate(@uib-tooltip, "F", "f"), "filter by")]')
    filter_by_value = DynamicPageElement(by=By.LINK_TEXT, locator="%s")
    # TODO In some cases the following is Button
    #      in other case it's real TextInput
    #      if not be aware with value property usage
    filter_input = form.TextInput(
        By.XPATH,
        '//div[contains(@ng-if, "filterType")]')
    filter_input_value = filter_by_value
    order_by = form.Button(
        By.XPATH,
        '(//*[@id="hostSort"]//button)[1]')

    # note the element is present only if some filter is active
    clear_all_filters = PageElement(
        by=By.LINK_TEXT,
        locator="Clear All Filters")

    # TODO add active filters elements
    #      note it's a list


class OrderListMenuModel(BaseListMenuModel):
    """
    auxiliary model for list menu (order fields)

    NOTE: Click on order_by opens a menu with some links
          such links has will be instanced from Page object
          a _link_text parameter will be used
          e.g. name = PageElement(by=By.LINK_TEXT, locator="Name")
    """
    order_by = form.Button(
        By.XPATH,
        '(//*[@id="hostSort"]//button)[1]')
    order_by_value = DynamicPageElement(by=By.LINK_TEXT, locator="%s")
    order_btn = form.Button(
        By.XPATH,
        '(//*[@id="hostSort"]//button)[2]')


class UpperMenuModel(WebstrModel):
    """
    Common model for upper menu
    """
    # right part of upper navbar
# TODO add context switcher drop-down list element
    # left part of upper navbar
# TODO: waiting for fix of https://github.com/Tendrl/ui/issues/839
#    users_link = PageElement(By.ID, locator="usermanagement")
#    alerts_link = PageElement(By.ID, locator="notifications")
    user_link = PageElement(By.ID, locator="usermenu")


class UserManagementModel(WebstrModel):
    """
    Common page model for main page - user management drop down menu
    """
    _base_locator = '//*[contains(@class, "dropdown admin")]'\
                    '/*[contains(@class, "dropdown-menu")]/..'
    _root = RootPageElement(by=By.XPATH, locator=_base_locator + '/ul[./li]')
    users = PageElement(by=By.LINK_TEXT, locator="Users")


# TODO: Alert list is not finished
#       Most probably other classes will be inherited not just WebstrModel
#       but some List and Row classes
class AlertListModel(WebstrModel):
    """
    model for drop-down alert list
    """
#    _root = RootPageElement(By.XPATH, '')


class AlertRowModel(WebstrModel):
    """
    model for any alert message
    """
#    priority = StatusIcon(By.XPATH, '')
#    message = PageElement(By.XPATH, '')


class UserMenuModel(WebstrModel):
    """
    Common page model for main page - user actions drop down menu
    """
    _base_locator = '//*[contains(@class, "dropdown user")]'\
                    '/*[contains(@class, "dropdown-menu")]/..'
    _root = RootPageElement(by=By.XPATH, locator=_base_locator + '/ul[./li]')
    my_settings = PageElement(by=By.LINK_TEXT, locator="My Settings")
    logout = PageElement(by=By.LINK_TEXT, locator="Logout")
