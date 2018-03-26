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
    # upper link
    clusters_link = PageElement(by=By.LINK_TEXT, locator="Clusters")
    # left navbar
    nodes_link = PageElement(by=By.LINK_TEXT, locator="Hosts")
    volumes_link = PageElement(by=By.LINK_TEXT, locator="Volumes")
    tasks_link = PageElement(by=By.LINK_TEXT, locator='Tasks')
    events_link = PageElement(by=By.LINK_TEXT, locator='Events')
