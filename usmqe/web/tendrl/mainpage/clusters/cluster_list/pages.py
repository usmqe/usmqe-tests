"""
Clusters page abstraction.
"""


import copy

from webstr.patternfly.contentviews import pages as contentviews

import usmqe.web.tendrl.mainpage.clusters.cluster_list.models as m_cluster_list
from usmqe.web.tendrl.auxiliary.pages import ListMenu
from usmqe.web.tendrl.mainpage.clusters.pages import ClustersWorkBase


class ClustersMenu(ListMenu, ClustersWorkBase):
    """
    Clusters page top menu
    """
    _model = m_cluster_list.ClustersMenuModel
    _label = 'cluster page top menu'
    _required_elems = copy.deepcopy(ListMenu._required_elems)
    _required_elems.extend(['header'])


class ClustersRow(contentviews.ListViewRow):
    """
    Cluster in Clusters list
    """
    _model = m_cluster_list.ClustersRowModel
    _required_elems = ['name_text']

    @property
    def name(self):
        """ returns cluster name """
        return self._model.name_text.text

    def open_details(self):
        """
        click on chosen cluster
        """
        self._model._root.click()

    def click_on_import(self):
        """
        click on Import Cluster button
        """
        self._model.import_btn.click()

    @property
    def managed(self):
        """
        returns if the cluster is managed
        """
        if self._model.managed.text.lower() == 'no':
            return False
        else:
            return True


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
