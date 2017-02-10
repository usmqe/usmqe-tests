"""
Common page model for navigation bars.
"""


# import pytest

from webstr.core import WebstrModel, By, PageElement


# part of url which is placed after 'usm_web_url'
# for getting on the described page in the module
LOCATION = '/#'


class NavMenuBarsModel(WebstrModel):
    """
    Common page model for the main page - navigation.
    """
# Coming soon...
#    # left part of upper navbar

# TODO
# Coming soon...
# Waiting for functional upper navbar
#    # right part of upper navbar

    # left navbar
    # dashboard_link = PageElement(by=By.LINK_TEXT, locator="Dashboard")
    clusters_link = PageElement(by=By.LINK_TEXT, locator="Clusters")
    nodes_link = PageElement(by=By.LINK_TEXT, locator="Hosts")
    file_shares_link = PageElement(by=By.LINK_TEXT, locator="File Shares")
    pools_link = PageElement(by=By.LINK_TEXT, locator="Pools")
    admin_link = PageElement(by=By.LINK_TEXT, locator="Admin")
    # Admin sub-menu links
    tasks_link = PageElement(by=By.LINK_TEXT, locator='Tasks')
