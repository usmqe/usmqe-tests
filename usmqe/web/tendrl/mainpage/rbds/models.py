"""
Common page model for rbds.
"""


from webstr.core import By, PageElement
from webstr.common.form import models as form
import webstr.patternfly.contentviews.models as contentviews
import webstr.patternfly.dropdown.models as dropdown

from usmqe.web.utils import StatusIcon
from usmqe.web.tendrl.auxiliary.models import ListMenuModel

LOCATION = "#/rbd"


class RBDsMenuModel(ListMenuModel):
    """
    RBDs page top menu
    """
    header = PageElement(by=By.XPATH, locator="//h1[text()='RBDs']")


class RBDsItemModel(contentviews.ListViewRowModel):
    """
    An item (row) in a RBDs list.
    """
# Design: https://redhat.invisionapp.com/share/BR8JDCGSQ
    status_icon = StatusIcon(
        by=By.XPATH,
        locator=".//span[contains(@ng-if,'rbd.status')]")
# TODO
# not sure about locator as I don't have any rbd available
    name_label = PageElement(by=By.XPATH, locator="./div/a")
# TODO
# add other elements

    name = name_label

    menu_link = form.Button(by=By.ID, locator="dropdownKebabRight12")


class RBDsListModel(contentviews.ListViewModel):
    """
    Page model for list of rbds.
    """


# TODO
# Coming soon...
# not sure about the menu as I don't have any rbd available
class RBDsRowMenuModel(dropdown.DropDownMenuModel):
    """ menu availalble for a host/row """
# TODO
# change following line when available, it's just an example
    edit_link = PageElement(by=By.LINK_TEXT, locator='Edit')
    remove_link = PageElement(by=By.LINK_TEXT, locator='Remove')
