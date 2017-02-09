# vim: set tabstop=2 shiftwidth=2 softtabstop=2 colorcolumn=120:
"""
Import Cluster wizard module.
"""


from webstr.core import WebstrModel, By, PageElement
from webstr.common.form import models as form
import webstr.patternfly.contentviews.models as contentviews

location = '/#/import-cluster'


class ImportClusterModel(WebstrModel):
    """
    model for Import Cluster - Configure Cluster page
    """
    label = PageElement(By.XPATH, '//h2/label')
    cluster = form.Select(
        By.XPATH,
        '//select[@data-ng-model="importClusterCntrl.selectedCluster"]')
    filter_by = form.Select(
        By.XPATH,
        '//select[@ng-model="importClusterCntrl.filterBy"]')
    filter_input = form.TextInput(By.ID, 'filter')
    order_by = form.TextInput(
        By.XPATH,
        '//select[@ng-model="importClusterCntrl.orderBy"]')
    order_btn = form.Button(
        By.XPATH,
        '//button[contains(@ng-init, "Order")]')
    refresh_btn = form.Button(
        By.XPATH,
        '//button[contains(text(), "Refresh")]')
    import_btn = form.Button(By.XPATH, '//button[contains(text(), "Import")]')
    cancel_btn = form.Button(By.XPATH, '//button[contains(text(), "Cancel")]')


class ImportClusterSummaryModel(WebstrModel):
    """
    model for Import Cluster - Summary page
    """
    view_task_btn = form.Button(
        By.XPATH,
        '//button[contains(text(), "View Task Progress"')


class HostItemModel(contentviews.ListViewRowModel):
    """
    An item (row) in a Hosts list.
    """
    name_label = PageElement(
        by=By.XPATH,
        locator=".//div[@class='list-group-item']/div[1]")
    release = PageElement(
        by=By.XPATH,
        locator=".//div[@class='list-group-item']/div[2]//h5[2]")
    name = name_label


class HostsListModel(contentviews.ListViewModel):
    """
    Page model for list of nodes/hosts.
    """
