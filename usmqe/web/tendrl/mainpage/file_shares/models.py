"""
Common page model for File Shares.
"""


from webstr.core import By, PageElement
from webstr.common.form import models as form
import webstr.patternfly.contentviews.models as contentviews
import webstr.patternfly.dropdown.models as dropdown

from usmqe.web.utils import StatusIcon
from usmqe.web.tendrl.auxiliary.models import ListMenuModel

LOCATION = "#/file-share"


class FileSharesMenuModel(ListMenuModel):
    """
    File Shares page top menu
    """
    header = PageElement(by=By.XPATH, locator="//h1[text()='File Shares']")
    # TODO add other elements filter, order_by and add button


class FileSharesItemModel(contentviews.ListViewRowModel):
    """
    An item (row) in a File Shares list.
    """
# Design: https://redhat.invisionapp.com/share/BR8JDCGSQ
    status_icon = StatusIcon(
        by=By.XPATH,
        locator=".//span[contains(@ng-if,'fileShare.status')]")
    name_label = PageElement(by=By.XPATH, locator="./div[2]//a")
    volume_type = PageElement(by=By.XPATH, locator="./div[2]//small")
# TODO
# put other parameters here when they will be available
# https://github.com/Tendrl/specifications/pull/95
# https://github.com/Tendrl/specifications/pull/77
    num_bricks = PageElement(
        by=By.XPATH,
        locator=".//b[contains(text(),'Bricks')]/../h5")

    name = name_label

    menu_link = form.Button(by=By.ID, locator="dropdownKebabRight12")


class FileSharesListModel(contentviews.ListViewModel):
    """
    Page model for list of file shares.
    """


# TODO
# Coming soon...
# waiting until the menu will be active
class FileSharesRowMenuModel(dropdown.DropDownMenuModel):
    """ menu available for a file shares/row """
    edit_link = PageElement(by=By.LINK_TEXT, locator='Edit')
    stop_link = PageElement(by=By.LINK_TEXT, locator='Stop')
    rebalance_link = PageElement(by=By.LINK_TEXT, locator='Rebalance')
    remove_link = PageElement(by=By.LINK_TEXT, locator='Remove')
