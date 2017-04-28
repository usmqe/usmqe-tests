"""
Clusters page abstraction.
"""


import copy

from webstr.patternfly.contentviews import pages as contentviews
import webstr.patternfly.dropdown.pages as dropdown

import usmqe.web.tendrl.mainpage.clusters.cluster_list.models as m_cluster_list
from usmqe.web.tendrl.mainpage.clusters.import_cluster_wizard.pages\
    import ImportCluster, ImportClusterSummary
from usmqe.web.tendrl.auxiliary.pages import ListMenu
from usmqe.web.tendrl.mainpage.tasks.pages import TaskDetails


class ClustersWorkBase(object):
    """
    auxiliary base class with methods for work with clusters - create/import
    """

    def start_import_cluster(self):
        """
        auxiliary method for clicking on proper import button
        """
        self._model.import_btn.click()

    def start_create_cluster(self):
        """
        auxiliary method for clicking on proper create button
        """
        self._model.create_btn.click()

    def import_cluster(self, cluster_id=None, name=None, hosts=None):
        """
        import cluster

        Parameters:
            cluster_id (str): cluster id for choosing a cluster
                              which should be imported
            name (str): name of the cluster
                        TODO: Not used for now
                              https://github.com/Tendrl/api/issues/70
            hosts (list): list of dictionaries
                          {'hostname': <hostname>, 'release': <release>, ...
                          for check only
                          TODO: not used for now
        """
# TODO: Choose which cluster should be imported
# TODO: Change cluster name
#       https://github.com/Tendrl/api/issues/70
        self.start_import_cluster()
        import time
        import_page = ImportCluster(self.driver)
# TODO: Check hosts list
        import_page.import_click()
        # the page is not loaded completely, better to wait a little
        time.sleep(1)
        final_import_page = ImportClusterSummary(self.driver)
        final_import_page.view_import_task()
        return TaskDetails(self.driver)

# TODO
# both ceph and gluster are imported the same way as of now
# use import_cluster method instead
    def import_gluster_cluster(self, name=None, hosts=None):
        """
        import gluster cluster

        Parameters:
            name (str): name of the cluster
                        TODO: Not used for now
                              https://github.com/Tendrl/api/issues/70
            hosts (list): list of dictionaries
                          {'hostname': <hostname>, 'release': <release>, ...
                          for check only
                          TODO: not used for now
        """
        raise NotImplementedError('import_gluster_cluster does not exist yet')

# TODO
# both ceph and gluster are imported the same way as of now
# use import_cluster method instead
    def import_ceph_cluster(self, name=None, hosts=None):
        """
        import ceph cluster

        Parameters:
            name (str): name of the cluster
            hosts (list): list of dictionaries
                          {'hostname': <hostname>,
                           'role': <'Monitor' or 'OSD Host'>, ...
        """
        raise NotImplementedError('import_ceph_cluster does not exist yet')

# TODO
    def create_gluster_cluster(self, name=None, hosts=None):
        """
        create gluster cluster

        Parameters:
            name (str): name of the cluster
                        TODO: Not used for now
                              https://github.com/Tendrl/api/issues/70
            hosts (list): list of dictionaries
                          {'hostname': <hostname>, 'release': <release>, ...
                          for check only
        """
        raise NotImplementedError('create_gluster_cluster does not exist yet')

# TODO
    def create_ceph_cluster(self, name=None, hosts=None):
        """
        create ceph cluster

        Parameters:
            name (str): name of the cluster
                        TODO: Not used for now
                              https://github.com/Tendrl/api/issues/70
            hosts (list): list of dictionaries
                          {'hostname': <hostname>,
                           'role': <'Monitor' or 'OSD Host'>, ...
        """
        raise NotImplementedError('create_ceph_cluster does not exist yet')


class ClustersMenu(ListMenu, ClustersWorkBase):
    """
    Clusters page top menu
    """
    _model = m_cluster_list.ClustersMenuModel
    _label = 'cluster page top menu'
    _required_elems = copy.deepcopy(ListMenu._required_elems)
    _required_elems.extend(['header', 'import_btn'])


class ClustersRow(contentviews.ListViewRow):
    """
    Cluster in Clusters list
    """
    _model = m_cluster_list.ClustersRowModel
    _required_elems = [
        'name_text',
        'hosts_label',
        'hosts_value',
        'alerts_label',
        'alerts_value',
        'menu_link']

    @property
    def name(self):
        """ returns cluster name """
        return self._model.name_text.text

# TODO
# Coming soon...
# waiting for the model, see models.py
#    @property
#    def status(self):
#        """ returns status on behalf of status_icon """
#        return self._model.status_icon.get_attribute('title')

    @property
    def hosts_nr(self):
        """
        returns number of hosts in the cluster as string
            text value of hosts_value field
        """
        return self._model.hosts_value.text

    @property
    def file_shares_nr(self):
        """
        returns number of file shares in the cluster as string
            text value of file_shares_value field
        """
        return self._model.file_shares_value.text

    @property
    def pools_nr(self):
        """
        returns number of pools in the cluster as string
            text value of pools_value field
        """
        return self._model.pools_value.text

    @property
    def alerts_nr(self):
        """
        returns number of alerts related to the cluster as string
            text value of alerts_value field
        """
        return self._model.alerts_value.text

    def click_on_alerts(self):
        """
        click on alerts number
        """
        self._model.alerts_value.click()

    def open_menu(self):
        """
        open a dropdown menu for the row

        Returns:
            ClustersRowMenu instance
        """
        self._model.menu_link.click()
        return ClustersRowMenu(self.driver)


# Coming soon...
class ClustersRowMenu(dropdown.DropDownMenu):
    """ menu availalble for a cluster/row """
    _model = m_cluster_list.ClustersRowMenuModel
    _required_elems = [
      'expand_link',
      'shrink_link'
    ]

# TODO use menu


class ClustersList(contentviews.ListView):
    """
    Base page object for Clusters list.

    Parameters:
      _location - initial URL to load upon instance creation
      _model - page model
    """
    _model = m_cluster_list.ClustersListModel
    _label = 'main page - clusters - list'
    _row_class = ClustersRow
