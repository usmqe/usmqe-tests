"""
Import Cluster wizard module.
"""


from webstr.core import By, PageElement
from webstr.common.form import models as form
import webstr.patternfly.contentviews.models as contentviews

from usmqe.web.tendrl.auxiliary.models import ListMenuModel
from usmqe.web.tendrl.mainpage.clusters.models import ViewTaskPageModel

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


class ImportClusterSummaryModel(ViewTaskPageModel):
    """
    model for Import Cluster - Summary page
    """


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
