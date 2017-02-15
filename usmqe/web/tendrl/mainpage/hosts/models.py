"""
Common page model for hosts.
"""


from webstr.core import By, PageElement
from webstr.common.form import models as form
import webstr.patternfly.contentviews.models as contentviews
import webstr.patternfly.dropdown.models as dropdown

from usmqe.web.utils import StatusIcon
from usmqe.web.tendrl.auxiliary.models import ListMenuModel

LOCATION = "#/node"


class HostsMenuModel(ListMenuModel):
    """
    Hosts page top menu
    """
    header = PageElement(by=By.XPATH, locator="//h1[text()='Hosts']")


class HostsItemModel(contentviews.ListViewRowModel):
    """
    An item (row) in a Hosts list.
    """
# Design: https://redhat.invisionapp.com/share/BR8JDCGSQ
    status_icon = StatusIcon(
        by=By.XPATH,
        locator=".//span[contains(@ng-if,'host.status')]")
    name_label = PageElement(
        by=By.XPATH,
        locator="./div/a")
# TODO
# https://github.com/Tendrl/specifications/pull/95
# https://github.com/Tendrl/specifications/pull/77
#    ip_label = PageElement(
#        by=By.XPATH,
#        locator=".//span[contains(@ng-bind,'host.management_ip4')]")
#
#    cpu_label = PageElement(by=By.XPATH, locator=".//div[.='CPU']")
#    cpu_graph_free = PageElement(
#        by=By.XPATH,
#        locator=".//div[.='CPU']/..//chart-column[@column-id='Free']")
#    cpu_graph_using = PageElement(
#        by=By.XPATH,
#        locator=".//div[.='CPU']/..//chart-column[@column-id='Using']")
#    cpu_graph_title = PageElement(
#        by=By.XPATH,
#        locator=".//div[.='CPU']/..//chart-column[@column-id='Using']/*")
#
#    memory_label = PageElement(by=By.XPATH, locator=".//div[.='Memory']")
#    memory_graph_free = PageElement(
#        by=By.XPATH,
#        locator=".//div[.='Memory']/..//chart-column[@column-id='Free']")
#    memory_graph_using = PageElement(
#        by=By.XPATH,
#        locator=".//div[.='Memory']/..//chart-column[@column-id='Using']")
#    memory_graph_title = PageElement(
#        by=By.XPATH,
#        locator=".//div[.='Memory']/..//chart-column[@column-id='Using']/*")
#
#    cluster_label = PageElement(by=By.XPATH, locator=".//div[.='Cluster']")
#    cluster_value = PageElement(
#        by=By.XPATH,
#        locator=".//div[.='Cluster']/following-sibling::*")
#
#    roles_label = PageElement(by=By.XPATH, locator=".//div[.='Roles']")
#    roles_value = PageElement(
#        by=By.XPATH,
#        locator=".//div[.='Roles']/following-sibling::*")
#
#    info_version_label = PageElement(
#        by=By.XPATH,
#        locator=".//span[.='Version : ']")
#    info_version_value = PageElement(
#        by=By.XPATH,
#        locator=".//span[.='Version : ']/following-sibling::*")
#
#    info_kernel_label = PageElement(
#        by=By.XPATH,
#        locator=".//span[.='Kernel : ']")
#    info_kernel_value = PageElement(
#        by=By.XPATH,
#        locator=".//span[.='Kernel : ']/following-sibling::*")
#
#    alerts_label = PageElement(by=By.XPATH, locator=".//div[.='Alerts']")
#    alerts_value = PageElement(
#        by=By.XPATH,
#        locator=".//div[.='Alerts']/following-sibling::*/span")

    name = name_label

    menu_link = form.Button(by=By.ID, locator="dropdownKebabRight12")


class HostsListModel(contentviews.ListViewModel):
    """
    Page model for list of nodes/hosts.
    """


# TODO
# Coming soon...
class HostsRowMenuModel(dropdown.DropDownMenuModel):
    """ menu availalble for a host/row """
    forget_link = PageElement(by=By.LINK_TEXT, locator='Forget')
    remove_link = PageElement(by=By.LINK_TEXT, locator='Remove')
    replace_link = PageElement(by=By.LINK_TEXT, locator='Replace')
