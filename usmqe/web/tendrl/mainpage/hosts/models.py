"""
Common page model for hosts.
"""


from webstr.core import WebstrModel, By, PageElement
from webstr.common.form import models as form
import webstr.patternfly.contentviews.models as contentviews

LOCATION = "#/node"


class HostsMenuModel(WebstrModel):
    """
    Hosts page top menu
    """
    header = PageElement(by=By.XPATH, locator="//h1[text()='Hosts']")
    # TODO add other elements filter, order_by and add button


class HostItemModel(contentviews.ListViewRowModel):
    """
    An item (row) in a Hosts list.
    """
# TODO
# https://github.com/Tendrl/specifications/pull/95
# https://github.com/Tendrl/specifications/pull/77
#    type_label = PageElement(by=By.XPATH, locator=".//span[@ng-bind='host.cluster_type']")
#    status_icon = PageElement(by=By.XPATH, locator=".//span[contains(@class,'status-icon')]")
    name_label = PageElement(
        by=By.XPATH,
        locator=".//p[contains(@ng-bind,'node.fqdn')]")
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
#    cluster_value = PageElement(by=By.XPATH, locator=".//div[.='Cluster']/following-sibling::*")
#
#    roles_label = PageElement(by=By.XPATH, locator=".//div[.='Roles']")
#    roles_value = PageElement(by=By.XPATH, locator=".//div[.='Roles']/following-sibling::*")
#
#    info_version_label = PageElement(by=By.XPATH, locator=".//span[.='Version : ']")
#    info_version_value = PageElement(
#        by=By.XPATH,
#        locator=".//span[.='Version : ']/following-sibling::*")
#
#    info_kernel_label = PageElement(by=By.XPATH, locator=".//span[.='Kernel : ']")
#    info_kernel_value = PageElement(
#        by=By.XPATH,
#        locator=".//span[.='Kernel : ']/following-sibling::*")
#
#    alerts_label = PageElement(by=By.XPATH, locator=".//div[.='Alerts']")
#    alerts_value = PageElement(by=By.XPATH, locator=".//div[.='Alerts']/following-sibling::*/span")
#
    name = name_label
#
#    # TODO: use menu object instead
#    menu_link = PageElement(by=By.XPATH, locator=".//div[last()]/a/i")
#    menu_delete = PageElement(by=By.XPATH, locator=".//div[last()]/ul/li/a")


class HostsListModel(contentviews.ListViewModel):
    """
    Page model for list of nodes/hosts.
    """
