"""
Page objects for navigation bars (both top and left menu bars).

* popup menus
* menubars

Author: ltrilety
"""


from webstr.core import WebstrPage

from usmqe.web.tendrl.mainpage.navpage import models as m_navpage
# from usmqe.web.tendrl.mainpage.dashboard.pages import Dashboard
from usmqe.web.tendrl.mainpage.clusters.cluster_list.pages import ClustersMenu
from usmqe.web.tendrl.mainpage.hosts.pages import HostsMenu


class NavMenuBars(WebstrPage):
    """
    Common page object for navigation bars:

    - left navigation menu bar (with links to other pages)
    - top navigation menu bar (with icons for popup menus)

    Atributes:
        _model - page model
        _label - human readable description of this *page object*
        _required_elems - web elements to be checked
    """
    _model = m_navpage.NavMenuBarsModel
    _label = 'main page - menu bar'
    _required_elems = [
        # left part of upper navbar
        # Coming soon...
        # right part of upper navbar
        # Coming soon...
        # left navbar
        # 'dashboard_link',
        'clusters_link',
        'nodes_link'
    ]

#    def open_dashboard(self, click_only=False):
#        """
#        Opens dashboard page.
#
#        Parameters:
#            click_only (bool): just click on the link and return None
#
#        Returns:
#            Instance of Dasboard
#        """
#        self._model.dashboard_link.click()
#        if click_only:
#            return None
#        return Dashboard(self.driver)

    def open_clusters(self, click_only=False):
        """
        Opens clusters page.

        Args:
            click_only (bool): just click on the link and return None

        Returns:
            Instance of ClusterList
        """
        self._model.clusters_link.click()
        if click_only:
            return None
        return ClustersMenu(self.driver)

    def open_hosts(self):
        """
        Opens hosts page.
        """
        self._model.nodes_link.click()
        return HostsMenu(self.driver)
