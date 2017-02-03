"""
Common page model for navigation bars.
"""


from webstr.core import WebstrModel, By, PageElement
from webstr.common.form import models as form


# part of url which is placed after 'usm_web_url'
# for getting on the described page in the module
LOCATION = '/#/landing-page'
# LOCATION = '/#/home'


class HomeModel(WebstrModel):
    """
    Common page model for the home page.
    """
    welcome_message = PageElement(by=By.XPATH, locator='//h1/label')
    import_btn = form.Button(
        by=By.XPATH,
        locator='//button[contains(text(), "Import Cluster")]')
# Coming soon...
# TODO
# https://tendrl.atlassian.net/browse/TEN-187
# https://tendrl.atlassian.net/browse/TEN-190
#   create_btn = form.Button(by=By.XPATH,
#                            locator='//*[@class="navbar-toggle"]')
