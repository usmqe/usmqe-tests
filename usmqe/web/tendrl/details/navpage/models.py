"""
Common page model for navigation bars.
"""


# import pytest

from webstr.core import By, PageElement

from usmqe.web.tendrl.auxiliary.models import UpperMenuModel


# part of url which is placed after 'usm_web_url'
# for getting on the described page in the module
LOCATION = '/#'


class NavMenuBarsModel(UpperMenuModel):
    """
    Common page model for the main page - navigation.
    """
# TODO
# Coming soon...
#    # right part of upper navbar

    # left navbar
    # dashboard_link = PageElement(by=By.LINK_TEXT, locator="Dashboard")
    clusters_link = PageElement(by=By.LINK_TEXT, locator="Clusters")
    nodes_link = PageElement(by=By.LINK_TEXT, locator="Hosts")
    alerts_link = PageElement(by=By.LINK_TEXT, locator="Alerts")
    admin_link = PageElement(by=By.LINK_TEXT, locator="Admin")
    # Admin sub-menu links
    tasks_link = PageElement(by=By.LINK_TEXT, locator='Tasks')
    tasks_link = PageElement(by=By.LINK_TEXT, locator='Users')
