"""
Some usefull model classes for common work with tendrl web
"""

from webstr.core import WebstrModel, By, PageElement, RootPageElement
from webstr.common.form import models as form
import webstr.patternfly.dropdown.models as dropdown

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
#    events_link
#    node_discovery_link
#    tasks_link
#    about_link
#    notifications_link
    user_link = PageElement(By.ID, locator="usermenu")


class UserMenuModel(dropdown.DropDownMenuModel):
    """
    Common page model for main page - user page
    """
    _base_locator = '//*[contains(@class, "dropdown user")]'\
                    '/*[contains(@class, "dropdown-menu")]/..'
    _root = RootPageElement(by=By.XPATH, locator=_base_locator + '/ul[./li]')
    logout = PageElement(by=By.LINK_TEXT, locator="Logout")


class AlertModel(WebstrModel):
    """
    model for any alert/notice message
    """
    _root = RootPageElement(By.XPATH, '//div[contains(@class, "alert")]')
    priority = StatusIcon(By.XPATH, './span')
    message = PageElement(By.XPATH, './strong')
    close_btn = form.Button(By.XPATH, './button')
