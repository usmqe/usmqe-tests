"""
Page objects for navigation bars (both top and left menu bars).

* popup menus
* menubars

Author: ltrilety
"""


from webstr.core import WebstrPage

from usmqe.web.tendrl.mainpage.navpage import models as m_navpage
# TODO
# not available for now
# from usmqe.web.tendrl.mainpage.dashboard.pages import Dashboard
from usmqe.web.tendrl.mainpage.clusters.cluster_list.pages import ClustersList
from usmqe.web.tendrl.mainpage.hosts.pages import HostsList
from usmqe.web.tendrl.mainpage.file_shares.pages import FileSharesList
from usmqe.web.tendrl.mainpage.pools.pages import PoolsList
# TODO
# not available yet
# from usmqe.web.tendrl.mainpage.admin.tasks.pages import TasksList


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
        'nodes_link',
        'file_shares_link',
        'pools_link'
    ]

# TODO
# dashboard page not working yet
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

        Parameters:
            click_only (bool): just click on the link and return None

        Returns:
            Instance of ClustersList if click_only is False
            None otherwise
        """
        self._model.clusters_link.click()
        if click_only:
            return None
        return ClustersList(self.driver)

    def open_hosts(self, click_only=False):
        """
        Opens hosts page.

        Parameters:
            click_only (bool): just click on the link and return None

        Returns:
            Instance of HostsList if click_only is False
            None otherwise
        """
        self._model.nodes_link.click()
        if click_only:
            return None
        return HostsList(self.driver)

    def open_file_shares(self, click_only=False):
        """
        Opens file shares page.

        Parameters:
            click_only (bool): just click on the link and return None

        Returns:
            Instance of FileSharesList if click_only is False
            None otherwise
        """
        self._model.file_shares_link.click()
        if click_only:
            return None
        return FileSharesList(self.driver)

    def open_pools(self, click_only=False):
        """
        Opens pools page.

        Parameters:
            click_only (bool): just click on the link and return None

        Returns:
            Instance of PoolsList if click_only is False
            None otherwise
        """
        self._model.pools_link.click()
        if click_only:
            return None
        return PoolsList(self.driver)

    def open_admin_submenu(self):
        """
        Opens admin sub-menu
        """
        self._model.admin_link.click()

    # Admin sub-menu links
    def open_tasks(self, click_only=False):
        """
        Opens tasks page.

        Parameters:
            click_only (bool): just click on the link and return None

        Returns:
            Instance of TasksList if click_only is False
            None otherwise
        """
        self.open_admin_submenu()
        self._model.tasks_link.click()
# TODO
# uncomment when Tasks page will be working
#        if click_only:
#            return None
#        return TasksList(self.driver)
