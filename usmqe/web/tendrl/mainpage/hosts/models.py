"""
Common page model for hosts.
"""


from webstr.core import By, PageElement, DynamicPageElement
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
    header = PageElement(by=By.XPATH, locator="//h1[contains(text(),'Hosts']")


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
        locator=".//span[contains(@ng-if,'host.status')]")
    name_label = PageElement(
        by=By.XPATH,
        locator="./div/a")
    name = name_label
# TODO
# https://github.com/Tendrl/specifications/pull/95
# https://github.com/Tendrl/specifications/pull/77
#    ip_label = PageElement(
#        by=By.XPATH,
#        locator=".//span[contains(@ng-bind,'host.management_ip4')]")
#    ip = ip_label

    storage_locator = ".//donut-chart[@id='storage-donut-chart%d']"
    storage_label = DynamicPageElement(
        by=By.XPATH,
        locator="{}//*[contains(text(),'Storage')]".format(storage_locator))
    storage_used_chart = DynamicPageElement(
        by=By.XPATH,
        locator="{}/span[1]".format(storage_locator))
    storage_used_nr = DynamicPageElement(
        by=By.XPATH,
        locator="{}/span[2]/[contains(@ng-if,'vm.chartData.used')]".
        format(storage_locator))
    # TODO make helper if needed
    #      as of now there's not just number in text(), bu also 'of ' string
    #      e.g. 'of XXXX', where the important part is just XXXX
    storage_total_nr = DynamicPageElement(
        by=By.XPATH,
        locator="{}/span[2]/[contains(@ng-if,'vm.chartData.total')]".
        format(storage_locator))

    cpu_locator = ".//donut-chart[@id='cpu-donut-chart%d']"
    cpu_label = DynamicPageElement(
        by=By.XPATH,
        locator="{}//*[contains(text(),'CPU')]".format(cpu_locator))
    cpu_percent_chart = DynamicPageElement(
        by=By.XPATH,
        locator="{}/span[1]".format(cpu_locator))
    # TODO make helper if needed
    #      as of now there's not just number in text(), bu also ' % ' string
    #      e.g. ' XXXX %', where the important part is just XXXX
    cpu_percent = DynamicPageElement(
        by=By.XPATH,
        locator="{}/span[2]/[contains(@ng-if,'vm.chartData.used')]".
        format(cpu_locator))

    memory_locator = ".//donut-chart[@id='memory-donut-chart%d']"
    memory_label = DynamicPageElement(
        by=By.XPATH,
        locator="{}//*[contains(text(),'Memory')]".format(memory_locator))
    memory_used_chart = DynamicPageElement(
        by=By.XPATH,
        locator="{}/span[1]".format(memory_locator))
    memory_used_nr = DynamicPageElement(
        by=By.XPATH,
        locator="{}/span[2]/[contains(@ng-if,'vm.chartData.used')]".
        format(memory_locator))
    # TODO make helper if needed
    #      as of now there's not just number in text(), bu also 'of ' string
    #      e.g. 'of XXXX', where the important part is just XXXX
    memory_total_nr = DynamicPageElement(
        by=By.XPATH,
        locator="{}/span[2]/[contains(@ng-if,'vm.chartData.total')]".
        format(memory_locator))

    cluster_label = PageElement(
        by=By.XPATH,
        locator=".//div/b[contains(text(),'Cluster')]")
    cluster_value = PageElement(
        by=By.XPATH,
        locator=".//div/b[contains(text(),'Cluster')]/following-sibling::*")

    roles_label = PageElement(
        by=By.XPATH,
        locator=".//div/b[contains(text(),'Role')]")
    roles_value = PageElement(
        by=By.XPATH,
        locator=".//*[contains(@ng-if,'host.role')]")

    alerts_label = PageElement(
        by=By.XPATH,
        locator=".//div/b[contains(text(),'Alerts')]")
    alerts_value = PageElement(
        by=By.XPATH,
        locator=".//div/b[contains(text(),'Alerts')]/following-sibling::*")

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
