"""
Create Cluster wizard module.
"""


from webstr.core import By, PageElement
from webstr.common.form import models as form
import webstr.patternfly.contentviews.models as contentviews

from usmqe.web.tendrl.auxiliary.models import ListMenuModel
from usmqe.web.tendrl.mainpage.clusters.create_cluster_wizard.\
    general.models import StepButtonsModel

location = '/#/create-gluster-cluster'


class StepGeneralModel(StepButtonsModel):
    """
    model for create gluster cluster - General step
    """
    service = PageElement(By.NAME, "storageService")
    name = form.TextInput(By.NAME, "glusterClusterName")


class StepNetworkAndHostsModel(ListMenuModel, StepButtonsModel):
    """
    model for create gluster cluster - "Network & Hosts" step
    """
    # NOTE: will be changed
    # https://bugzilla.redhat.com/show_bug.cgi?id=1458706
    # https://bugzilla.redhat.com/show_bug.cgi?id=1458737
    # https://bugzilla.redhat.com/show_bug.cgi?id=1455229
    # menu
    select_all = PageElement(By.LINK_TEXT, "Select All")
    deselect_all = PageElement(By.LINK_TEXT, "Deselect All")
    cluster_network = form.Select(
        By.XPATH,
        '//select[contains(@ng-model, "ClusterNetwork")]')


class CreateHostsItemModel(contentviews.ListViewRowModel):
    """
    An item (row) in a Hosts list.
    """
    check = form.Checkbox(
        By.XPATH,
        './div[1]/input')
    name_label = PageElement(
        by=By.XPATH,
        locator="./div[2]")
    name = name_label
    cluster_net_if = PageElement(
        by=By.XPATH,
        locator="./div[3]/div/div[1]")
    cluster_net_address = PageElement(
        by=By.XPATH,
        locator="./div[3]/div/div[2]")
    disks = PageElement(
        by=By.XPATH,
        locator="./div[4]/div/div[2]")
    capacity = PageElement(
        by=By.XPATH,
        locator="./div[5]/div/div[2]")


class CreateHostsListModel(contentviews.ListViewModel):
    """
    Page model for list of nodes/hosts.
    """


class StepReviewModel(StepButtonsModel):
    """
    model for create gluster cluster - "Review" step
    """
    STEP_SUMMARY_PATH = '//div[contains(@ng-if, "selectedStep")]'
    # cluster summary
    CLUSTER_SUM_PATH = '{}/div[contains(concat(" ", @class, " "),'\
        '" single-create-cluster-summary ")]'.format(STEP_SUMMARY_PATH)
    name = PageElement(
        by=By.XPATH,
        locator='{}/div[1]/div[2]'.format(CLUSTER_SUM_PATH))
    devices = PageElement(
        by=By.XPATH,
        locator='{}/div[2]/div[2]'.format(CLUSTER_SUM_PATH))
    capacity = PageElement(
        by=By.XPATH,
        locator='{}/div[3]/div[2]'.format(CLUSTER_SUM_PATH))
    cluster_network = PageElement(
        by=By.XPATH,
        locator='{}/div[4]/div[2]'.format(CLUSTER_SUM_PATH))
    # hosts summary
    host_nr = '{}/h3'.format(STEP_SUMMARY_PATH)

    create_cluster_btn = StepButtonsModel.next_btn


class HostsSumItemModel(contentviews.ListViewRowModel):
    """
    An item (row) in a Hosts list.
    """
    name_label = PageElement(
        by=By.XPATH,
        locator="./div/div/div[2]//strong")
    name = name_label
    settings = PageElement(
        by=By.XPATH,
        locator="./div/div/div[2]//h5")
    interface = PageElement(
        by=By.XPATH,
        locator="./div/div/div[3]//strong")
    address = PageElement(
        by=By.XPATH,
        locator="./div/div/div[3]/div/div")


class HostsSumListModel(contentviews.ListViewModel):
    """
    Page model for list of nodes/hosts.
    """
