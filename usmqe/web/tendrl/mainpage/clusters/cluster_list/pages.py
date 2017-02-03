"""
Clusters page abstraction.
"""


from webstr.core import WebstrPage
from webstr.patternfly.contentviews import pages as contentviews

import usmqe.web.tendrl.mainpage.clusters.cluster_list.models as m_cluster_list
# import usmqe.web.tendrl.mainpage.clusters.import_cluster_wizard as wizard


class ClustersMenu(WebstrPage):
    """
    Clusters page top menu
    """
    _model = m_cluster_list.ClustersMenuModel
    _label = 'cluster page top menu'
    _required_elems = ['header', 'search', 'import_btn']

    def start_import_cluster_wizard(self):
        """
        Just click on button to start Import Cluster wizard
        Nothing else is done.
        """
        self._model.import_btn.click()

# TODO
#    # NOTE: it will be probably splitted to two methods
#    # import_gluster_cluster and import_ceph_cluster
#    def import_cluster(self, name, hosts=None):
#        """
#        Import cluster via the wizard.
#
#        Args:
#            name (str): name of cluster
#            hosts (list): list of dictionaries
#                          {'hostname': <hostname>,
#                           'role': <'Monitor' or 'OSD Host'>}
#                          by default all host are selected with default roles
#        """
#        # TODO: support other options
#        self.start_import_cluster_wizard()
#        current_page = wizard.ImportCluster(self.driver)
#        # TODO: choose cluster
#        # TODO: set name https://github.com/Tendrl/api/issues/70
#        # TODO: check and work with hosts
#        current_page.import_click()
#        # TODO: work or return the object representing
#        #       next page with link to a task


class ClusterRow(contentviews.ListViewRow):
    """
    Cluster in Clusters list
    """
    _model = m_cluster_list.ClusterRowModel
    _required_elems = []

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
