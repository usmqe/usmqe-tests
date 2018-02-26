"""
Some usefull model classes for common work with tendrl web
"""

from webstr.core import WebstrModel, By, PageElement, RootPageElement
from webstr.common.form import models as form

from usmqe.web.utils import StatusIcon


class ListMenuModel(WebstrModel):
    """
    auxiliary model for list menu (filter and order fields)
    """
    filter_by = form.Select(
        By.XPATH,
        '//select[contains(translate(@ng-model, "F", "f"), "filterBy")]')
    filter_input = form.TextInput(By.ID, 'filter')
    order_by = form.TextInput(
        By.XPATH,
        '//select[contains(@ng-model, "orderBy")]')
    order_btn = form.Button(
        By.XPATH,
        '//button[contains(@ng-init, "Order")]')


class UpperMenuModel(WebstrModel):
    """
    Common model for upper menu
    """
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
