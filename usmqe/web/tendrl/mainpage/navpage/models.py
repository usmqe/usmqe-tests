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
#    navbar_toggle = form.Button(by=By.XPATH,
#                                locator='//*[@class="navbar-toggle"]')
#    navbar_brand = PageElement(by=By.XPATH,
#                               locator='//*[@class="navbar-brand"]')

# TODO
# Coming soon...
# Waiting for functional upper navbar
#    # right part of upper navbar
#    alerts_link = PageElement(
#        by=By.XPATH,
#        locator='//*[@data-template="views/base/alert-dropdown.tpl.html"]')
#    hosts_link_menu_locator = \
#        '//*[@data-template="views/base/discovered-hosts.tpl.html"]'
#    hosts_link_menu = PageElement(
#        by=By.XPATH,
#        locator=hosts_link_menu_locator)
#
#    progress_link_locator = \
#        '//*[@data-template="views/base/progress-dropdown.tpl.html"]'
#    progress_link = PageElement(
#        by=By.XPATH,
#        locator=progress_link_locator)
#
#    user_link_locator = \
#        '//*[@data-template="views/base/admin-dropdown.tpl.html"]'
#    user_link = PageElement(by=By.XPATH, locator=user_link_locator)

    # left navbar
    dashboard_link = PageElement(by=By.LINK_TEXT, locator="Dashboard")
    clusters_link = PageElement(by=By.LINK_TEXT, locator="Clusters")
    nodes_link = PageElement(by=By.LINK_TEXT, locator="Hosts")
# TODO
# Coming soon...
# Not working yet
#    storages_link = PageElement(by=By.LINK_TEXT, locator="Storage")
#    # Storages sub-menu links
#    pools_link = PageElement(by=By.LINK_TEXT, locator="Pools")
#    rbds_link = PageElement(by=By.LINK_TEXT, locator="RBDs")
#    admin_link = PageElement(by=By.LINK_TEXT, locator='Admin')
#    # Admin sub-enu links
#    tasks_link = PageElement(by=By.LINK_TEXT, locator='Tasks')
#    events_link = PageElement(by=By.LINK_TEXT, locator='Events')
#    users_link = PageElement(by=By.LINK_TEXT, locator='Users')
#    ldap_settings_link = PageElement(by=By.LINK_TEXT, locator='Ldap Settings')
#    mail_settings_link = PageElement(by=By.LINK_TEXT, locator='Mail Settings')
