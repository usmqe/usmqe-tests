"""
Hosts page abstraction.
"""


from webstr.patternfly.contentviews import pages as contentviews
import webstr.patternfly.dropdown.pages as dropdown

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
    _required_elems = [
        '_root',
        'status_icon',
        'name_label',
        # TODO uncomment following lines when performance monitoring
        #      will work and charts will be available
        # 'storage_label',
        # 'storage_used_chart',
        # 'storage_used_nr',
        # 'storage_total_nr',
        # 'cpu_label',
        # 'cpu_percent_chart',
        # 'cpu_percent',
        # 'memory_label',
        # 'memory_used_chart',
        # 'memory_used_nr',
        # 'memory_total_nr',
        'cluster_label',
        'cluster_value',
        'roles_label',
        'roles_value',
        'alerts_label',
        'alerts_value',
        'menu_link']

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
    def ip(self):
        """
        returns host ip address
        """
        return self._model.ip.text

    @property
    def cluster(self):
        """
        returns cluster in which host is located
        """
        return self._model.cluster_value.text

    @property
    def role(self):
        """
        return host role
            text value of roles_value field
        """
        return self._model.roles_value.text

    @property
    def alerts_nr(self):
        """
        returns number of alerts related to the cluster as string
            text value of alerts_value field
        """
        return self._model.alerts_value.text

    def click_on_alerts(self):
        """
        click on alerts number
        """
        self._model.alerts_value.click()

    def open_menu(self):
        """
        open row menu

        Returns:
            HostsRowMenu instance
        """
        self._model.menu_link.click()
        return HostsRowMenu(self.driver)


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
    _required_elems = ['forget_link', 'remove_link', 'replace_link']

# TODO use menu
