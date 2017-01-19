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

    def import_cluster(self, name, hosts=None):
        """
        Import cluster via the wizard.

        Args:
            name (str): name of cluster
            hosts (list): list of dictionaries
                          {'hostname': <hostname>,
                           'role': <'Monitor' or 'OSD Host'>}
                          by default all host are selected with default roles
        """
        # TODO: support other options
        self.start_import_cluster_wizard()
        # TODO: close the warning dialogue about unaccepted hosts if needed
#        current_page = wizard.ImportClusterConfigure(self.driver)
# Coming soon...
#        current_page.get_model_element("next_btn").click()
#        current_page.name = name
#        current_page.click_next()
#        current_page = wizard.CreateClusterSelectHost(self.driver)
#        if hosts is None:
#            current_page.select_all()
#        else:
#            pass
#            # TODO: click on some hosts and choose their role
#        current_page.click_next()
#        current_page = wizard.CreateClusterChooseNetwork(self.driver)
#        current_page.click_next()
#        current_page = wizard.CreateClusterStorageProfiles(self.driver)
#        current_page.click_next()
#        current_page = wizard.CreateClusterReview(self.driver)
#        current_page.create()


class ClusterRow(contentviews.ListViewRow):
    """
    Cluster in Clusters list
    """
    _model = m_cluster_list.ClusterRowModel
    _required_elems = []

# Coming soon...
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
