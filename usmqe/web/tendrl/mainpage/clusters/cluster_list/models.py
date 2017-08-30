"""
Common page models for clusters.
"""


from webstr.core import By, PageElement
from webstr.common.form import models as form
import webstr.patternfly.contentviews.models as contentviews

from usmqe.web.tendrl.auxiliary.models import ListMenuModel
# from usmqe.web.utils import StatusIcon


LOCATION = '/#/clusters'


class ClustersMenuModel(ListMenuModel):
    """
    Clusters page top menu
    """
    header = PageElement(
        by=By.XPATH,
        locator="//h1[contains(text(),'Clusters')]")


class ClustersListModel(contentviews.ListViewModel):
    """ list of clusters with common cluster elements """


class ClustersRowModel(contentviews.ListViewRowModel):
    """
    Row in Cluster table model.
    """
#   https://github.com/Tendrl/specifications/pull/82
#
# TODO
# https://redhat.invisionapp.com/share/BR8JDCGSQ#/screens/185937524
# No status icon yet
#    status_icon = StatusIcon(By.XPATH, '')
#
    name_text = PageElement(
        by=By.XPATH,
        locator='.//div[contains(@class, "cluster-name")]')
    name = name_text

    cluster_version = PageElement(
        by=By.XPATH,
        locator='.//div[contains(text(),"Cluster Version")]'
        '/following-sibling::*')

    managed = PageElement(
        by=By.XPATH,
        locator='.//div[contains(text(),"Managed")]/following-sibling::*')

    volume_profile = PageElement(
        by=By.XPATH,
        locator='.//div[contains(text(),"Volume Profile")]'
        '/following-sibling::*')

    import_btn = form.Button(
        By.XPATH,
        '//button[@ng-click="clusterCntrl.goToImportFlow(cluster)"]')
# TODO
# add link to grafana when available


# TODO add HostsListModel and HostsRowModel
