"""
Create Cluster wizard module.
"""


from webstr.core import WebstrModel, By, PageElement, RootPageElement,\
    NameRootPageElement, DynamicWebstrModel, DynamicPageElement
from webstr.common.form import models as form
import webstr.patternfly.contentviews.models as contentviews

from usmqe.web.tendrl.auxiliary.models import ListMenuModel
from usmqe.web.tendrl.mainpage.clusters.create_cluster_wizard.general.\
    models import StepButtonsModel

location = '/#/create-ceph-cluster'


class StepGeneralModel(StepButtonsModel):
    """
    model for create ceph cluster - General step
    """
    service = PageElement(By.NAME, "storageService")
    name = form.TextInput(By.NAME, "cephClusterName")
    production_use = form.Radio(By.ID, 'production')
    demo_use = form.Radio(By.ID, "poc")


class StepNetworkAndHostsModel(StepButtonsModel):
    """
    model for create ceph cluster - "Network & Hosts" step
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
        '//select[contains(@ng-model,"ClusterNetwork")]')
    public_network = form.Select(
        By.XPATH,
        '//select[contains(@ng-model,"PublicNetwork")]')


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
    public_net_if = PageElement(
        by=By.XPATH,
        locator="./div[3]/div/div[1]")
    public_net_address = PageElement(
        by=By.XPATH,
        locator="./div[3]/div/div[2]")


class CreateHostsListModel(contentviews.ListViewModel):
    """
    Page model for list of nodes/hosts.
    """


class StepRolesModel(ListMenuModel, StepButtonsModel):
    """
    model for create ceph cluster - "Roles" step
    """
    def __init__(self, driver):
        """ init """
        super().__init__(driver)
        self.hosts_summary = RolesSummaryModel(self.driver)


class RolesSummaryModel(WebstrModel):
    """
    create ceph cluster - "Roles" step summary
    """
    _root = RootPageElement(
        By.XPATH,
        '//div[contains(@class, "available-host-list")]')
    nr = PageElement(By.XPATH, './div[1]/div/div[2]')
    monitors = PageElement(By.XPATH, './div[2]//h5')
    OSDs = PageElement(By.XPATH, './div[3]//h5')
    devices = PageElement(By.XPATH, './div[4]//h5')
    capacity = PageElement(By.XPATH, './div[5]//h5')


class RolesHostsItemModel(contentviews.ListViewRowModel):
    """
    An item (row) in a Hosts list.
    """
    name_label = PageElement(
        by=By.XPATH,
        locator="./div[1]")
    name = name_label
    interfaces_nr = PageElement(
        by=By.XPATH,
        locator="./div[2]//h5")
    devices = PageElement(
        by=By.XPATH,
        locator="./div[3]//h5")
    free_devices = PageElement(
        by=By.XPATH,
        locator="./div[4]//h5")
    capacity = PageElement(
        by=By.XPATH,
        locator="./div[5]//h5")
    role = form.Select(
        by=By.XPATH,
        locator="./div[5]//select")


class RolesHostsListModel(contentviews.ListViewModel):
    """
    Page model for list of nodes/hosts.
    """


class StepJournalConfModel(ListMenuModel, StepButtonsModel):
    """
    model for create ceph cluster - "Journal Configuration" step
    """


class JournalHostsItemModel(DynamicWebstrModel):
    """
    An item (row) in a Hosts list.
    """
    ITEM_PATH = '(//*[contains(concat(" ", @class, " "), '\
        '" list-view-pf ")])[%d]'
    _root = NameRootPageElement(By.XPATH, ITEM_PATH)
    # Note: inactive symbol has ng-hide in class
    expand_symbol = PageElement(
        by=By.XPATH,
        locator="./div/div/div[1]/i[1]")
    hide_symbol = PageElement(
        by=By.XPATH,
        locator="./div/div/div[1]/i[2]")
    name_label = PageElement(
        by=By.XPATH,
        locator="./div/div/div[2]//strong")
    name = name_label
    devices = PageElement(
        by=By.XPATH,
        locator="./div/div/div[2]//h5")
    journal_size = form.TextInput(
        by=By.XPATH,
        locator="./div/div/div[3]//input")
    journal_size_units = form.Select(
        by=By.XPATH,
        locator="./div/div/div[3]//select")
    # dedicated X colocated
    journal_conf = form.Select(
        by=By.XPATH,
        locator="./div/div/div[4]//select")


class JournalHostsItemTModel(DynamicWebstrModel):
    """
    Available devices configuration table
    """
    _root = NameRootPageElement(
        By.XPATH,
        '{}//table'.format(JournalHostsItemModel.ITEM_PATH))
    rows = DynamicPageElement(
        By.XPATH,
        '{}//table/tr'.format(JournalHostsItemModel.ITEM_PATH),
        as_list=True)


class JournalHostsItemTDRowModel(DynamicWebstrModel):
    """
    Available devices configuration table row - dedicated journal

    Note: the name has to be tuple with two values,
          number of row in the hosts list and
          number of row in the devices table
    """
    _root = NameRootPageElement(
        By.XPATH,
        '{}//table/tr[%d]'.format(JournalHostsItemModel.ITEM_PATH))
    device = PageElement(by=By.XPATH, locator='./td[1]/div[1]')
    device_type = PageElement(by=By.XPATH, locator='./td[1]/div[2]')
    journal = PageElement(by=By.XPATH, locator='./td[2]')


class JournalHostsItemTCRowModel(DynamicWebstrModel):
    """
    Available devices configuration table row - colocated journal

    Note: the name has to be tuple with two values,
          number of row in the hosts list and
          number of row in the devices table
    """
    _root = NameRootPageElement(
        By.XPATH,
        '{}//table/tr[%d]'.format(JournalHostsItemModel.ITEM_PATH))
    device = PageElement(by=By.XPATH, locator='./td[1]')
    device_type = PageElement(by=By.XPATH, locator='./td[2]')
    capacity = PageElement(by=By.XPATH, locator='./td[3]')


class JournalHostsListModel(WebstrModel):
    """
    Page model for list of nodes/hosts.
    """
    _root = None
    rows = PageElement(
        by=By.XPATH,
        locator='//*[contains(concat(" ", @class, " "), " list-view-pf ")]',
        as_list=True)


class StepReviewModel(StepButtonsModel):
    """
    model for create ceph cluster - "Review" step
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
    public_network = PageElement(
        by=By.XPATH,
        locator='{}/div[5]/div[2]'.format(CLUSTER_SUM_PATH))
    # monitor summary
    mon_nr = '{}/h3[1]'.format(STEP_SUMMARY_PATH)
    # OSDs summary
    osd_nr = '{}/h3[2]'.format(STEP_SUMMARY_PATH)

    create_cluster_btn = StepButtonsModel.next_btn


class MonSummaryRowModel(DynamicWebstrModel):
    """
    model for Monitor Summary Row
    """
    _root = NameRootPageElement(
        By.XPATH,
        '{}/div[2]/div[%d]'.format(StepReviewModel.STEP_SUMMARY_PATH))
    name = PageElement(By.XPATH, './div/div/div[1]//strong')
    settings = PageElement(By.XPATH, './div/div/div[1]//h5')
    interface = PageElement(By.XPATH, './div/div/div[2]//strong')
    address = PageElement(By.XPATH, './div/div/div[2]/div/div')


class MonSummaryModel(WebstrModel):
    """
    model for Monitor Summary
    """
    _root = RootPageElement(
        By.XPATH,
        '{}/div[2]'.format(StepReviewModel.STEP_SUMMARY_PATH))
    rows = PageElement(
        by=By.XPATH,
        locator='{}/div[2]/div'.format(StepReviewModel.STEP_SUMMARY_PATH),
        as_list=True)


class OSDSumItemModel(DynamicWebstrModel):
    """
    An item (row) in a Hosts list.
    """
    ITEM_PATH = '(//{}/*[contains(concat(" ", @class, " "), '\
        '" list-view-pf ")])[%d]'.format(StepReviewModel.STEP_SUMMARY_PATH)
    _root = NameRootPageElement(By.XPATH, ITEM_PATH)
    # Note: inactive symbol has ng-hide in class
    expand_symbol = PageElement(
        by=By.XPATH,
        locator="./div/div/div[1]/i[1]")
    hide_symbol = PageElement(
        by=By.XPATH,
        locator="./div/div/div[1]/i[2]")
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
    journal_conf = PageElement(
        by=By.XPATH,
        locator="./div/div/div[4]//h5")
    journal_size = form.TextInput(
        by=By.XPATH,
        locator="./div/div/div[5]//h5")


class OSDSumItemTModel(DynamicWebstrModel):
    """
    Devices OSD Summary table
    """
    _root = NameRootPageElement(
        By.XPATH,
        '{}//table'.format(OSDSumItemModel.ITEM_PATH))
    rows = DynamicPageElement(
        By.XPATH,
        '{}//table/tr'.format(OSDSumItemModel.ITEM_PATH),
        as_list=True)


class OSDSumItemTDRowModel(DynamicWebstrModel):
    """
    Devices OSD Summary table row - dedicated journal

    Note: the name has to be tuple with two values,
          number of row in the hosts list and
          number of row in the devices table
    """
    _root = NameRootPageElement(
        By.XPATH,
        '{}//table/tr[%d]'.format(OSDSumItemModel.ITEM_PATH))
    device = PageElement(by=By.XPATH, locator='./td[1]/div[1]')
    device_type = PageElement(by=By.XPATH, locator='./td[1]/div[2]')
    journal = PageElement(by=By.XPATH, locator='./td[2]')


class OSDSumItemTCRowModel(DynamicWebstrModel):
    """
    Devices OSD Summary table row - colocated journal

    Note: the name has to be tuple with two values,
          number of row in the hosts list and
          number of row in the devices table
    """
    _root = NameRootPageElement(
        By.XPATH,
        '{}//table/tr[%d]'.format(OSDSumItemModel.ITEM_PATH))
    device = PageElement(by=By.XPATH, locator='./td[1]')
    device_type = PageElement(by=By.XPATH, locator='./td[2]')
    capacity = PageElement(by=By.XPATH, locator='./td[3]')


class OSDSumListModel(WebstrModel):
    """
    Page model for list of nodes/hosts.
    """
    _root = RootPageElement(
        By.XPATH,
        '{}/div[4]'.format(StepReviewModel.STEP_SUMMARY_PATH))
    rows = PageElement(
        by=By.XPATH,
        locator='//{}/*[contains(concat(" ", @class, " "), '
        '" list-view-pf ")]'.format(StepReviewModel.STEP_SUMMARY_PATH),
        as_list=True)
