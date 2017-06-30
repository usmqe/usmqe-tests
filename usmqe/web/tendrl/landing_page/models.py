"""
Common page model for navigation bars.
"""


from webstr.core import By, PageElement
from webstr.common.form import models as form

from usmqe.web.tendrl.auxiliary.models import UpperMenuModel

# part of url which is placed after 'usm_web_url'
# for getting on the described page in the module
LOCATION = '/#/landing-page'
# LOCATION = '/#/home'


class HomeModel(UpperMenuModel):
    """
    Common page model for the home page.
    """
    welcome_message = PageElement(by=By.XPATH, locator='//h1/label')
    import_btn = form.Button(
        by=By.XPATH,
        locator='//button[contains(text(), "Import Cluster")]')
    create_btn = form.Button(
        by=By.XPATH,
        locator='//button[contains(text(), "Create Cluster")]')
