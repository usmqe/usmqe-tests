"""
Page objects for navigation bars (both top and left menu bars).

* popup menus
* menubars

Author: ltrilety
"""


import copy

from usmqe.web.tendrl.auxiliary.pages import UpperMenu
from usmqe.web.tendrl.details.navpage import models as m_navpage
# TODO
# not available for now
# from usmqe.web.tendrl.clusters.pages import ClustersList
from usmqe.web.tendrl.details.hosts.pages import HostsList
from usmqe.web.tendrl.details.tasks.pages import TasksList


class NavMenuBars(UpperMenu):
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
    _required_elems = copy.deepcopy(UpperMenu._required_elems)
    _required_elems.extend([
        'clusters_link',
        'nodes_link',
        'volumes_link',
        'tasks_link',
        'events_link'
    ])

# TODO for open clusters page a "context switcher's" dropdown menu has to be used
#    def open_clusters(self, click_only=False):
#        """
#        Opens clusters page.
#
#        Parameters:
#            click_only (bool): just click on the link and return None
#
#        Returns:
#            Instance of ClustersList if click_only is False
#            None otherwise
#        """
#        self._model.clusters_link.click()
#        if click_only:
#            return None
#        return ClustersList(self.driver)

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

    def open_volumes(self, click_only=False):
        """
        Opens alerts page.

        Parameters:
            click_only (bool): just click on the link and return None

        Returns:
            Instance of AlertsList if click_only is False
            None otherwise
        """
        self._model.volumes_link.click()
        if click_only:
            return None
# TODO
# volumes not yet implemented
#        return VolumesList(self.driver)

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
        if click_only:
            return None
        return TasksList(self.driver)

    def open_events(self, click_only=False):
        """
        Opens users page.

        Parameters:
            click_only (bool): just click on the link and return None

        Returns:
            Instance of UsersList if click_only is False
            None otherwise
        """
        self.open_admin_submenu()
        self._model.events_link.click()
# TODO
# uncomment when Events page will be working
#        if click_only:
#            return None
#        return EventsList(self.driver)
