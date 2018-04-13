"""
Import Cluster wizard module.
"""


from webstr.core import By, PageElement, NameRootPageElement
from webstr.common.form import models as form
import webstr.patternfly.contentviews.models as contentviews

from usmqe.web.tendrl.auxiliary.models import FilterListMenuModel,\
    OrderListMenuModel
from usmqe.web.tendrl.clusters.auxiliary.models import ViewTaskPageModel

# The URL is not much usable as the correct one ends with /<cluster_id>
location = '/#/import-cluster'


class ImportClusterModel(FilterListMenuModel, OrderListMenuModel):
    """
    model for Import Cluster - Configure Cluster page
    """
    label = PageElement(By.XPATH, '//h1')
    profile_check = form.Checkbox(By.NAME, "volumeProfile")
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
        locator=".//div[contains(@class, 'host-name')]")
    release = PageElement(
        by=By.XPATH,
        locator=".//div[contains(@class, 'host-release')]")
    name = name_label
    role = PageElement(
        By.XPATH,
        ".//div[contains(@class, 'list-view-pf-additional-info')]/div[2]")
    _root = NameRootPageElement(
        by=By.XPATH,
        locator='({}//*[contains(concat(" ", @class, " "),'
        ' " list-group-item ")][@ng-repeat])[%d]'.format(
            contentviews.ListViewModel.LIST_XPATH))


class HostsListModel(contentviews.ListViewModel):
    """
    Page model for list of nodes/hosts.
    """
    rows = PageElement(
        by=By.XPATH,
        locator="{}//*[contains(concat(' ', @class, ' '),"
        " ' list-group-item ')][@ng-repeat]".format(
            contentviews.ListViewModel.LIST_XPATH),
        as_list=True)
