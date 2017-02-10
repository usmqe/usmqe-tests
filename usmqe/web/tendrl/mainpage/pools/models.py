"""
Common page model for pools.
"""


from webstr.core import By, PageElement
from webstr.common.form import models as form
import webstr.patternfly.contentviews.models as contentviews
import webstr.patternfly.dropdown.models as dropdown

from usmqe.web.utils import StatusIcon
from usmqe.web.tendrl.auxiliary.models import ListMenuModel

LOCATION = "#/pool"


class PoolsMenuModel(ListMenuModel):
    """
    Pools page top menu
    """
    header = PageElement(by=By.XPATH, locator="//h1[text()='Pools']")


class PoolsItemModel(contentviews.ListViewRowModel):
    """
    An item (row) in a Pools list.
    """
# Design: https://redhat.invisionapp.com/share/BR8JDCGSQ
    status_icon = StatusIcon(
        by=By.XPATH,
        locator=".//span[contains(@ng-if,'pool.status')]")
# TODO
# not sure about locator as I don't have any pool available
    name_label = PageElement(by=By.XPATH, locator="./div/a")
# TODO
# add other elements when available
# https://github.com/Tendrl/specifications/pull/95
# https://github.com/Tendrl/specifications/pull/77

    name = name_label

    menu_link = form.Button(by=By.ID, locator="dropdownKebabRight12")


class PoolsListModel(contentviews.ListViewModel):
    """
    Page model for list of pools.
    """


# TODO
# Coming soon...
# not sure about the menu as I don't have any pool available
class PoolsRowMenuModel(dropdown.DropDownMenuModel):
    """ menu availalble for a host/row """
# TODO
# change following line when available, it's just an example
    edit_link = PageElement(by=By.LINK_TEXT, locator='Edit')
    grow_link = PageElement(by=By.LINK_TEXT, locator='Grow')
    remove_link = PageElement(by=By.LINK_TEXT, locator='Remove')
