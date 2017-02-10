"""
Hosts page abstraction.
"""


from webstr.patternfly.contentviews import pages as contentviews

import usmqe.web.tendrl.mainpage.hosts.models as m_hosts
from usmqe.web.tendrl.auxiliary.pages import ListMenu


class HostsMenu(ListMenu):
    """
    page object for hosts top menu
    """
    _model = m_hosts.HostsMenuModel
    _label = 'hosts top menu'
    _required_elems = ListMenu._required_elems
    _required_elems.append('header')


class HostsItem(contentviews.ListViewRow):
    """
    An item (row) in a Hosts list.
    """
    _model = m_hosts.HostsItemModel
    _label = 'hosts row'
    _required_elems = ['_root', 'name_label']


class HostsList(contentviews.ListView):
    """
    Base page object for List of nodes.
    """
    _model = m_hosts.HostsListModel
    _label = 'main page - hosts'
    _row_class = HostsItem
