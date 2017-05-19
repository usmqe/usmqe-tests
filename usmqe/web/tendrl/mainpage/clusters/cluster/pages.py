"""
Page objects for cluster details navigation

Author: ltrilety
"""


import copy

from webstr.core import WebstrPage

import usmqe.web.tendrl.mainpage.clusters.cluster.models as m_cluster
from usmqe.web.tendrl.mainpage.dashboard.pages import Dashboard
from usmqe.web.tendrl.mainpage.hosts.pages import HostsList
from usmqe.web.tendrl.mainpage.file_shares.pages import FileSharesList
from usmqe.web.tendrl.mainpage.pools.pages import PoolsList
from usmqe.web.tendrl.mainpage.rbds.pages import RBDsList


class ClusterMenu(WebstrPage):
    """
    cluster details menu
    """
    _model = m_cluster.ClusterMenuModel
    _label = 'main page - clusters - cluster menu'
    _required_elems = ['overview_link', 'hosts_link']

    def open_overview(self, click_only=False):
        """
        open Overview tab

        Parameters:
            click_only (bool): if method should return Dashboard instance

        Returns:
            Dashboard instance if click_only is False
        """
        self._model.overview_link.click()
        if not click_only:
            return Dashboard(self.driver)

    def open_hosts(self, click_only=False):
        """
        open Hosts tab

        Parameters:
            click_only (bool): if method should return HostsList instance

        Returns:
            HostsList instance if click_only is False
        """
        self._model.hosts_link.click()
        if not click_only:
            return HostsList(self.driver)


class GlusterMenu(ClusterMenu):
    """
    gluster cluster specific details menu
    """
    _model = m_cluster.GlusterMenuModel
    _label = 'main page - clusters - gluster cluster menu'
    _required_elems = copy.deepcopy(ClusterMenu._required_elems)
    _required_elems.append('file_shares')

    def open_file_shares(self, click_only=False):
        """
        open File Shares tab

        Parameters:
            click_only (bool): if method should return FileSharesList instance

        Returns:
            FileSharesList instance if click_only is False
        """
        self._model.file_shares_link.click()
        if not click_only:
            return FileSharesList(self.driver)


class CephMenu(ClusterMenu):
    """
    ceph cluster specific details menu
    """
    _model = m_cluster.CephMenuModel
    _label = 'main page - clusters - ceph cluster menu'
    _required_elems = copy.deepcopy(ClusterMenu._required_elems)
    _required_elems.extend(['pools', 'rbds'])

    def open_pools(self, click_only=False):
        """
        open Pools tab

        Parameters:
            click_only (bool): if method should return PoolsList instance

        Returns:
            PoolsList instance if click_only is False
        """
        self._model.pools_link.click()
        if not click_only:
            return PoolsList(self.driver)

    def open_rbds(self, click_only=False):
        """
        open RBDs tab

        Parameters:
            click_only (bool): if method should return RBDsList instance

        Returns:
            RBDsList instance if click_only is False
        """
        self._model.rbds_link.click()
        if not click_only:
            return RBDsList(self.driver)
