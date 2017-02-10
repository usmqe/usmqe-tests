"""
Common page models for clusters.
"""


from webstr.core import By, PageElement
from webstr.common.form import models as form
import webstr.patternfly.contentviews.models as contentviews
import webstr.patternfly.dropdown.models as dropdown

from usmqe.web.tendrl.auxiliary.models import ListMenuModel


LOCATION = '/#/cluster'


class ClustersMenuModel(ListMenuModel):
    """
    Clusters page top menu
    """
    header = PageElement(by=By.XPATH, locator="//h1[text()='Clusters']")
    import_btn = form.Button(
        By.XPATH,
        '//button[@ng-click="cluster.importCluster()"]')


class ClustersListModel(contentviews.ListViewModel):
    """ list of clusters with common cluster elements """


class ClustersRowModel(contentviews.ListViewRowModel):
    """
    Row in Cluster table model.
    """
#   TODO
#   https://github.com/Tendrl/specifications/pull/82
#    type_text = PageElement(
#        by=By.XPATH,
#        locator='.//span[contains(@class, \'vertical-text-for-\')]')
#
#    # TODO: change it to patternfly icon
#    status_icon = PageElement(By.XPATH, './/*[contains(@class, "pficon"]')
#
#    name_text = PageElement(by=By.XPATH, locator='.//a[contains(@href, \'#/clusters/detail/\')]')
#    usage_percent_text = PageElement(
#        by=By.XPATH,
#        locator='.//div[contains(@class, \'percentage-heading\')]')
#    usage_text = PageElement(by=By.XPATH, locator='.//div[contains(@class, \'percentage-used\')]')
#    disk_info_text = PageElement(
#        by=By.XPATH,
#        locator='.//div[contains(@class, \'disk-info-cart\')]')
#
#    iops_value = PageElement(by=By.XPATH, locator='.//chart-column[@column-id=\'IOPS-0\']')
#    iops_text = PageElement(
#        by=By.XPATH,
#        locator='.//chart-column[@column-id=\'IOPS-0\']/chart-gauge')
#
#    hosts_value = PageElement(by=By.XPATH, locator='.//div[@ng-bind=\'cluster.no_of_hosts\']')
#    hosts_text = PageElement(
#        by=By.XPATH,
#        locator='.//div[@ng-bind=\'cluster.no_of_hosts\']/preceding-sibling::div')
#
#    pools_value = PageElement(
#        by=By.XPATH,
#        locator='.//div[@ng-bind=\'cluster.no_of_volumes_or_pools\']')
#    pools_text = PageElement(
#        by=By.XPATH,
#        locator='.//div[@ng-bind=\'cluster.no_of_volumes_or_pools\']/preceding-sibling::div')
#
#    alerts_value = PageElement(
#        by=By.XPATH,
#        locator='.//span[@ng-bind=\'cluster.alerts\']')
#    alerts_text = PageElement(
#        by=By.XPATH,
#        locator='.//span[@ng-bind=\'cluster.alerts\']/../preceding-sibling::div')
#
#    menu_locator = './/a[@data-template=\'views/clusters/cluster-menu-dropdown.tpl.html\']/i'
#    menu_link = PageElement(by=By.XPATH, locator=menu_locator)


# Coming soon...
# class ClusterRowMenu(dropdown.DropDownMenu):
#    """ menu availalble for a cluster/row """
#    expand_link = PageElement(by=By.LINK_TEXT, locator='Expand')
#    enable_link = PageElement(by=By.LINK_TEXT, locator='Manage')
#    disable_link = PageElement(by=By.LINK_TEXT, locator='UnManage')
#    forget_link = PageElement(by=By.LINK_TEXT, locator='Forget')
