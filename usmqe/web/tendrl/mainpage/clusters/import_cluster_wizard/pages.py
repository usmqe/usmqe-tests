"""
Import Cluster wizard module.
"""


from webstr.core import WebstrPage
import webstr.patternfly.contentviews.pages as contentviews

import usmqe.web.tendrl.mainpage.clusters.\
    import_cluster_wizard.models as m_wizard
from usmqe.web.tendrl.auxiliary.pages import ListMenu


class ImportCluster(ListMenu):
    """
    Import Cluster page
    """
    _model = m_wizard.ImportClusterModel
    _label = 'clusters import page'
    _required_elems = [
        'label',
        'cluster',
        'refresh_btn',
        'import_btn',
        'cancel_btn'
    ]

    @property
    def hosts(self):
        """
        get hosts list
        """
        return HostsList(self.driver)

# TODO ... not ready yet, not sure what selector should be
    def choose_cluster(self, selector):
        """
        choose the cluster to be imported
        """
        pass

    def refresh_hosts(self):
        """
        click on refresh button
        """
        self._model.refresh_btn.click()

    def import_click(self):
        """
        click on import button
        """
        self._model.import_btn.click()

    def cancel(self):
        """
        click on cancel button
        """
        self._model.cancel_btn.click()

    @property
    def cluster_id(self):
        """
        returns cluster id
        """
        return self._model.cluster_id.text

    @property
    def storage_service(self):
        """
        returns storage service
        """
        return self._model.storage_service.text


class ImportClusterSummary(WebstrPage):
    """
    Import Cluster - Review Summary page
    """
    _model = m_wizard.ImportClusterSummaryModel
    _label = 'clusters import Summary page'
    _required_elems = ['view_task_btn']

    def view_import_task(self):
        """ click on View Task Progress button
        """
        self._model.view_task_btn.click()


class HostsItem(contentviews.ListViewRow):
    """
    An item (row) in a Hosts list.
    """
    _model = m_wizard.HostsItemModel
    _label = 'clusters import host'
    _required_elems = ['name', 'release', 'role']

    @property
    def name(self):
        """
        returns host name
        """
        return self._model.name.text

    @property
    def release(self):
        """
        returns installed ceph/gluster release
        """
        return self._model.release.text

    @property
    def role(self):
        """
        returns host role
        """
        return self._model.role.text


class HostsList(contentviews.ListView):
    """
    List of nodes/hosts.
    """
    _model = m_wizard.HostsListModel
    _label = 'clusters import hosts list'
    _row_class = HostsItem
