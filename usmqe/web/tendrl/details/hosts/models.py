"""
Common page model for hosts.
"""


from webstr.core import By, PageElement
from webstr.common.form import models as form
import webstr.patternfly.contentviews.models as contentviews
import webstr.patternfly.dropdown.models as dropdown

from usmqe.web.utils import StatusIcon
from usmqe.web.tendrl.auxiliary.models import FilterListMenuModel,\
    OrderListMenuModel

# The URL is not much usable as the correct one ends with /<cluster_id>
LOCATION = "#/cluster-hosts"


class HostsMenuModel(FilterListMenuModel, OrderListMenuModel):
    """
    Hosts page top menu
    """
    header = PageElement(by=By.XPATH, locator="//h1[contains(text(),'Hosts')]")


class HostsItemModel(contentviews.ListViewRowModel):
    """
    An item (row) in a Hosts list.
    """

    def _instance_identifier(self):
        """
        instance identifier: line number - 1
        """
        return self._name - 1

# Design: https://redhat.invisionapp.com/share/BR8JDCGSQ
    status_icon = StatusIcon(
        by=By.XPATH,
        locator=".//i[contains(@ng-class,'host.status')]")
    name_label = PageElement(
        by=By.XPATH,
        locator=".//div[contains(@class,'host-name')]")
    name = name_label

    gluster_label = PageElement(
        by=By.XPATH,
        locator=".//div[contains(text(),'Gluster Version')]")
    gluster_value = PageElement(
        by=By.XPATH,
        locator=".//div[contains(text(),'Gluster Version')]"
        "/following-sibling::*")

    roles_label = PageElement(
        by=By.XPATH,
        locator=".//div[contains(text(),'Role')]")
    roles_value = PageElement(
        by=By.XPATH,
        locator=".//div[contains(text(),'Role')]/following-sibling::*")

    bricks_label = PageElement(
        by=By.XPATH,
        locator=".//div[contains(text(),'Bricks')]")
    bricks_value = PageElement(
        by=By.XPATH,
        locator=".//div[contains(text(),'Bricks')]/following-sibling::*")

    alerts_label = PageElement(
        by=By.XPATH,
        locator=".//div[contains(text(),'Alerts')]")
    alerts_value = PageElement(
        by=By.XPATH,
        locator=".//div[contains(text(),'Alerts')]/following-sibling::*")

    dashboard_btn = form.Button(
        by=By.XPATH,
        locator=".//button[contains(@class,'dashboard-btn')]")

# no menu as of now
#    menu_link = form.Button(by=By.ID, locator="dropdownKebabRight12")


class HostsListModel(contentviews.ListViewModel):
    """
    Page model for list of nodes/hosts.
    """


# TODO
# Coming soon...
class HostsRowMenuModel(dropdown.DropDownMenuModel):
    """ menu availalble for a host/row """
#    forget_link = PageElement(by=By.LINK_TEXT, locator='Forget')
#    remove_link = PageElement(by=By.LINK_TEXT, locator='Remove')
#    replace_link = PageElement(by=By.LINK_TEXT, locator='Replace')
