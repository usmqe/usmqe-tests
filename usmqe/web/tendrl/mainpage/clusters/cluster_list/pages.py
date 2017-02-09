"""
Clusters page abstraction.
"""


from webstr.core import WebstrPage
from webstr.patternfly.contentviews import pages as contentviews

import usmqe.web.tendrl.mainpage.clusters.cluster_list.models as m_cluster_list
from usmqe.web.tendrl.mainpage.clusters.import_cluster_wizard.pages\
    import ImportCluster


class ClusterWorkBase(object):
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
        self.start_import_cluster()
        import_page = ImportCluster(self.driver)
# TODO: Check hosts list
        import_page.import_click()
# TODO: Wait till the cluster is imported
#       OR (probably better)
#       work or return the object representing
#       next page with link to a task
#       https://github.com/Tendrl/usmqe-tests/issues/33

# TODO
    def import_ceph_cluster(self, name=None, hosts=None):
        """
        import gluster cluster

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
        import gluster cluster

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
        import gluster cluster

        Parameters:
            name (str): name of the cluster
                        TODO: Not used for now
                              https://github.com/Tendrl/api/issues/70
            hosts (list): list of dictionaries
                          {'hostname': <hostname>,
                           'role': <'Monitor' or 'OSD Host'>, ...
        """
        raise NotImplementedError('create_ceph_cluster does not exist yet')


class ClustersMenu(WebstrPage, ClusterWorkBase):
    """
    Clusters page top menu
    """
    _model = m_cluster_list.ClustersMenuModel
    _label = 'cluster page top menu'
    _required_elems = ['header', 'search', 'import_btn']


class ClusterRow(contentviews.ListViewRow):
    """
    Cluster in Clusters list
    """
    _model = m_cluster_list.ClusterRowModel
    _required_elems = []

# TODO
# Coming soon...
# waiting for the model, see models.py
#    @property
#    def name(self):
#      """ returns cluster name """
#      return self._model.name_text.text
#
#    @property
#    def status(self):
#      """ returns status on behalf of status_icon """
#      return self._model.status_icon.get_attribute('title')
#
#    def open_row_menu(self):
#      """
#      open a dropdown menu for the row
#
#      Returns:
#          ClusterRowMenu instance
#      """
#      self._model.menu_link.click()
#      return ClusterRowMenu(self.driver)

# Coming soon...
# waiting for the model, see models.py
#  class ClusterRowMenu(dropdown.DropDownMenu):
#    """ menu availalble for a cluster/row """
#    _model = m_cluster_list.ClusterRowMenu
#    _required_elems = [
#      'expand_link',
#      'enable_link',
#      'disable_link',
#      'forget_link'
#    ]


class ClusterList(contentviews.ListView):
    """
    Base page object for Clusters list.

    Parameters:
      _location - initial URL to load upon instance creation
      _model - page model
    """
    _model = m_cluster_list.ClusterListModel
    _label = 'main page - clusters - list'
    _row_class = ClusterRow
