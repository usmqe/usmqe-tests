"""
Hosts page abstraction.
"""


import copy

from webstr.patternfly.contentviews import pages as contentviews
import webstr.patternfly.dropdown.pages as dropdown

import usmqe.web.tendrl.details.hosts.models as m_hosts
from usmqe.web.tendrl.auxiliary.pages import ListMenu


class HostsMenu(ListMenu):
    """
    page object for hosts top menu
    """
    _model = m_hosts.HostsMenuModel
    _label = 'hosts top menu'
    _required_elems = copy.deepcopy(ListMenu._required_elems)
    _required_elems.append('header')


class HostsItem(contentviews.ListViewRow):
    """
    An item (row) in a Hosts list.
    """
    _model = m_hosts.HostsItemModel
    _label = 'hosts row'
    _required_elems = [
        '_root',
        'status_icon',
        'name_label',
        'gluster_label',
        'gluster_value',
        'roles_label',
        'roles_value',
        'bricks_label',
        'bricks_value',
        'alerts_label',
        'alerts_value',
        'dashboard_link']

    @property
    def status(self):
        """
        find status

        Returns:
            status_icon element title
        """
        return self._model.status_icon.value

    @property
    def name(self):
        """
        returns proper hostname
        """
        return self._model.name.text

    @property
    def gluster_version(self):
        """
        returns gluster version of cluster in which host is located
        """
        return self._model.gluster_value.text

    @property
    def role(self):
        """
        return host role
            text value of roles_value field
        """
        return self._model.roles_value.text

    @property
    def bricks_nr(self):
        """
        return number of bricks on the host
        """
        return self._model.bricks_value.text

    @property
    def alerts_nr(self):
        """
        returns number of alerts related to the cluster as string
            text value of alerts_value field
        """
        return self._model.alerts_value.text

    def dashboard_open(self):
        """
        click on dashboard button
        """
        self._model.dashboard_btn.click()


class HostsList(contentviews.ListView):
    """
    Base page object for List of nodes.
    """
    _model = m_hosts.HostsListModel
    _label = 'main page - hosts'
    _row_class = HostsItem


class HostsRowMenu(dropdown.DropDownMenu):
    """
    page object for hosts row menu
    """
    _model = m_hosts.HostsRowMenuModel
    _label = 'hosts row menu'
    _required_elems = []
