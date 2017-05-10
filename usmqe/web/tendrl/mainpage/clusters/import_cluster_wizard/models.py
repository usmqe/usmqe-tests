"""
Import Cluster wizard module.
"""


from webstr.core import WebstrModel, By, PageElement
from webstr.common.form import models as form
import webstr.patternfly.contentviews.models as contentviews

from usmqe.web.tendrl.auxiliary.models import ListMenuModel

location = '/#/import-cluster'


class ImportClusterModel(ListMenuModel):
    """
    model for Import Cluster - Configure Cluster page
    """
    label = PageElement(By.XPATH, '//h2/label')
    cluster = form.Select(
        By.XPATH,
        '//select[@data-ng-model="importClusterCntrl.selectedCluster"]')
    cluster_id = PageElement(
        By.XPATH,
        '//div[@class="cluster-detail"]/div[1]/div[2]')
    storage_service = PageElement(
        By.XPATH,
        '//div[@class="cluster-detail"]/div[2]/div[2]')
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
        '//button[contains(@ng-click, "viewTaskProgress()")]')


class HostsItemModel(contentviews.ListViewRowModel):
    """
    An item (row) in a Hosts list.
    """
    name_label = PageElement(
        by=By.XPATH,
        locator="./div[1]")
    release = PageElement(
        by=By.XPATH,
        locator="./div[2]//h5[2]")
    name = name_label
    role = PageElement(
        by=By.XPATH,
        locator="./div[3]//h5[2]")


class HostsListModel(contentviews.ListViewModel):
    """
    Page model for list of nodes/hosts.
    """
