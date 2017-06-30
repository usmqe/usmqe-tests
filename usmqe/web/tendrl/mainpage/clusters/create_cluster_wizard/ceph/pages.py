"""
Import Cluster wizard module.
"""


import copy

from webstr.core import WebstrPage, DynamicWebstrPage
import webstr.patternfly.contentviews.pages as contentviews
import webstr.common.containers.pages as containers

import usmqe.web.tendrl.mainpage.clusters.create_cluster_wizard.\
    ceph.models as m_ceph
from usmqe.web.tendrl.auxiliary.pages import ListMenu
from usmqe.web.tendrl.mainpage.clusters.create_cluster_wizard.\
    general.pages import StepButtons


class StepGeneral(StepButtons):
    """
    page object for create ceph cluster - General step
    """
    _model = m_ceph.StepGeneralModel
    _label = 'create ceph cluster - General step'
    _required_elems = copy.deepcopy(StepButtons._required_elems)
    _required_elems.extend([
        'service', 'name', 'production_use', 'demo_use'])

    def set_name(self, value):
        """
        set new name

        Parameters:
            value (str): new name
        """
        self._model.name.value = value

    @property
    def service(self):
        """
        return service text
        """
        return self._model.service.text

    def production_use(self):
        """
        choose production use
        """
        self._model.production_use.value = True

    def demo_use(self):
        """
        choose Evaluation or Demonstration use
        """
        self._model.demo_use.value = True


class StepNetworkAndHosts(StepButtons):
    """
    page object for create ceph cluster - "Network & Hosts" step
    """
    _model = m_ceph.StepNetworkAndHostsModel
    _label = 'create ceph cluster - Network & Hosts step'
    _required_elems = copy.deepcopy(StepButtons._required_elems)
    _required_elems.extend([
        'select_all', 'deselect_all', 'cluster_network', 'public_network'])

    def select_all(self):
        """
        select all displayed hosts
        """
        self._model.select_all.click()

    def deselect_all(self):
        """
        deselect all displayed hosts
        """
        self._model.deselect_all.click()

    @property
    def cluster_network(self):
        """
        returns selected cluster network
        """
        return self._model.cluster_network.value

    @cluster_network.setter
    def cluster_network(self, net_addr):
        """
        set cluster network

        Parameters:
            net_addr (str): cluster network address
        """
        self._model.cluster_network.value = net_addr

    @property
    def public_network(self):
        """
        returns selected public network
        """
        return self._model.public_network.value

    @public_network.setter
    def public_network(self, net_addr):
        """
        set public network

        Parameters:
            net_addr (str): public network address
        """
        self._model.public_network.value = net_addr


class CreateHostsItem(contentviews.ListViewRow):
    """
    An item (row) in a Hosts list.
    """
    _model = m_ceph.CreateHostsItemModel
    _label = 'create ceph cluster - Hosts row'
    _required_elems = [
        'check',
        'name',
        'cluster_net_if',
        'cluster_net_address',
        'public_net_if',
        'public_net_address']

    def select(self):
        """
        check the row
        """
        self._model.check.check()

    @property
    def name(self):
        """
        returns hostname
        """
        return self._model.name.text


class CreateHostsList(contentviews.ListView):
    """
    Page object for list of nodes/hosts.
    """
    _model = m_ceph.CreateHostsListModel
    _label = 'create ceph cluster hosts'
    _row_class = CreateHostsItem


class StepRoles(ListMenu, StepButtons):
    """
    page object for create ceph cluster - "Roles" step
    """
    _model = m_ceph.CreateHostsItemModel
    _label = 'create ceph cluster - Hosts row'


class RolesSummary(WebstrPage):
    """
    create ceph cluster - "Roles" step summary
    """
    _model = m_ceph.RolesSummaryModel
    _label = 'Roles step summary'
    _required_elems = [
        'nr',
        'monitors',
        'OSDs',
        'devices',
        'capacity']


class RolesHostsItem(contentviews.ListViewRow):
    """
    An item (row) in a Hosts list.
    """
    _model = m_ceph.RolesHostsItemModel
    _label = 'Roles step hosts row'
    _required_elems = [
        'name',
        'interfaces_nr',
        'devices',
        'free_devices',
        'capacity',
        'role']

    @property
    def name(self):
        """
        returns hostname
        """
        return self._model.name.text

    @property
    def role(self):
        """
        returns selected role
        """
        return self._model.role.value

    @role.setter
    def role(self, role):
        """
        set role

        Parameters:
            role (str): chosen role
        """
        self._model.role.value = role


class RolesHostsList(contentviews.ListView):
    """
    Page object for list of nodes/hosts.
    """
    _model = m_ceph.RolesHostsListModel
    _label = 'Roles step hosts list'
    _row_class = RolesHostsItem


class StepJournalConf(ListMenu, StepButtons):
    """
    page object for create ceph cluster - "Journal Configuration" step
    """
    _model = m_ceph.StepJournalConfModel
    _label = 'create ceph cluster - Journal Configuration step'


class JournalHostsItem(containers.ContainerRowBase):
    """
    An item (row) in a Hosts list.
    """
    _model = m_ceph.JournalHostsItemModel
    _label = 'Journal configuration hosts row'
    _required_elems = [
        'expand_symbol',
        'hide_symbol',
        'name',
        'devices',
        'journal_size',
        'journal_size_units',
        'journal_conf']

    def is_active(symbol):
        """
        finds out if expand/hide symbol is active

        Parameters:
            symbol: selenium object

        Returns:
            True if the symbol is active, False otherwise
        """
        if 'ng_hide' in symbol.get_attribute('class'):
            return False
        else:
            return True

    def expand(self):
        """
        expand disk devices list if possible

        Returns:
            JournalHostsItemTC or JournalHostsItemTD instance in regards
              to current journal configuration
        """
        if JournalHostsItem.is_active(self._model.expand_symbol):
            self._model.expand_symbol.click()
        if self.journal_conf == 'dedicated':
            JournalHostsItemTD(self.driver, self._name)
        else:
            JournalHostsItemTC(self.driver, self._name)

    def hide(self):
        """
        hide disk devices list if possible
        """
        if JournalHostsItem.is_active(self._model.hide_symbol):
            self._model.hide_symbol.click()

    @property
    def name(self):
        """
        returns hostname
        """
        return self._model.name.text

    @property
    def journal_size(self):
        """
        returns current journal size
        """
        return self._model.journal_size.value

    @journal_size.setter
    def journal_size(self, value):
        """
        set journal size

        Parameters:
            value (str): journal size
        """
        self._model.journal_size.value = value

    @property
    def journal_size_units(self):
        """
        returns current journal size units
        """
        return self._model.journal_size_units.value

    @journal_size_units.setter
    def journal_size_units(self, units):
        """
        set journal size units

        Parameters:
            units (str): journal size units
                         'GB' or 'MB'
        """
        self._model.journal_size_units.value = units

    @property
    def journal_conf(self):
        """
        returns current journal configuration
          'dedicated' or 'colocated'
        """
        return self._model.journal_size.value

    @journal_conf.setter
    def journal_conf(self, value):
        """
        set journal configuration

        Parameters:
            value (str): journal configuration
                         'dedicated' or 'colocated'
        """
        self._model.journal_conf.value = value


class HostsItemTIterator(containers.ContainerIterator):
    """
    Iterator class for JournalHostsItemTC and JournalHostsItemTD.
    """

    def __init__(self, driver, row_element_list, row_class, row_id):
        """
        Arguments:
            driver: selenium web driver
            row_element_list (list): rows class attribute of container class
            row_class: class representing single line or item
            row_id (str): number of the row in which the list is located
        """
        super().__init__(driver, row_element_list, row_class)
        self._row_id = row_id

    def __next__(self):
        """
        Return current item element.
        """
        # this code expects that the table row doesn't disappear
        table_row = self._row_class(
            self._driver,
            (self._row_id, next(self._id_iter)))
        return table_row


class HostsItemT(DynamicWebstrPage):
    """
    Available devices configuration table
    """
    _model = m_ceph.JournalHostsItemTModel
    _iter_class = HostsItemTIterator
    _required_elems = ['_root']

    def __iter__(self):
        """
        Create new iterator object for this table.
        """
        row_element_list = self._model.rows
        return self._iter_class(
            self.driver, row_element_list,
            self._row_class, self._name)

    def __len__(self):
        """
        Returns:
            number of rows
        """
        return len(self._model.rows)


class JournalHostsItemTCRow(DynamicWebstrPage):
    """
    Available devices configuration table row - dedicated journal

    Note: the name has to be tuple with two values,
          number of row in the hosts list and
          number of row in the devices table
    """
    _model = m_ceph.JournalHostsItemTCRowModel
    _label = 'Colocated journal host devices table row'
    _required_elems = ['device', 'device_type', 'journal']


class JournalHostsItemTC(HostsItemT):
    """
    Available devices configuration table - colocated journal
    """
    _label = 'Colocated journal host devices table'
    _row_class = JournalHostsItemTCRow


class JournalHostsItemTDRow(DynamicWebstrPage):
    """
    Available devices configuration table row - dedicated journal

    Note: the name has to be tuple with two values,
          number of row in the hosts list and
          number of row in the devices table
    """
    _model = m_ceph.JournalHostsItemTDRowModel
    _label = 'Dedicated journal host devices table row'
    _required_elems = ['device', 'device_type', 'capacity']


class JournalHostsItemTD(HostsItemT):
    """
    Available devices configuration table - dedicated journal
    """
    _label = 'Dedicated journal host devices table'
    _row_class = JournalHostsItemTDRow


class JournalHostsList(containers.ContainerBase):
    """
    Page object for list of nodes/hosts.
    """
    _model = m_ceph.JournalHostsListModel
    _label = 'Journal configuration hosts list'
    _row_class = JournalHostsItem


class StepReview(StepButtons):
    """
    page object for create ceph cluster - "Review" step
    """
    _model = m_ceph.StepReviewModel
    _label = 'create ceph cluster - Review step'
    _required_elems = copy.deepcopy(StepButtons._required_elems)
    _required_elems.extend([
        'name',
        'devices',
        'capacity',
        'cluster_network',
        'public_network',
        'mon_nr',
        'osd_nr'])

    create_cluster = StepButtons.click_next


class MonSummaryRow(containers.ContainerRowBase):
    """
    page object for Monitor Summary Row
    """
    _model = m_ceph.MonSummaryRowModel
    _label = 'review monitor summary row'
    _required_elems = ['name', 'settings', 'interface', 'address']


class MonSummary(containers.ContainerBase):
    """
    page object for Monitor Summary
    """
    _label = 'review monitor summary'
    _required_elems = ['_root']
    _row_class = MonSummaryRow


class OSDSumItem(containers.ContainerRowBase):
    """
    An item (row) in a Hosts list.
    """
    _model = m_ceph.MonSummaryRowModel
    _label = 'review OSD summary row'
    _required_elems = [
        'expand_symbol',
        'hide_symbol',
        'name',
        'settings',
        'interface',
        'address',
        'journal_conf',
        'journal_size']


class OSDSumItemTDRow(DynamicWebstrPage):
    """
    Devices OSD Summary table row - dedicated journal

    Note: the name has to be tuple with two values,
          number of row in the hosts list and
          number of row in the devices table
    """
    _model = m_ceph.OSDSumItemTDRowModel
    _label = 'review OSD summary device row'
    _required_elems = ['device', 'device_type', 'journal']


class OSDSumItemTD(HostsItemT):
    """
    Devices OSD Summary table - dedicated journal
    """
    _label = 'review OSD summary devices table'
    _row_class = OSDSumItemTDRow


class OSDSumItemTCRow(DynamicWebstrPage):
    """
    Devices OSD Summary table row - colocated journal

    Note: the name has to be tuple with two values,
          number of row in the hosts list and
          number of row in the devices table
    """
    _model = m_ceph.OSDSumItemTCRowModel
    _label = 'review OSD summary device row'
    _required_elems = ['device', 'device_type', 'capacity']


class OSDSumItemTC(HostsItemT):
    """
    Devices OSD Summary table - colocated journal
    """
    _label = 'review OSD summary devices table'
    _row_class = OSDSumItemTCRow


class OSDSumList(containers.ContainerBase):
    """
    Page object for list of nodes/hosts.
    """
    _model = m_ceph.MonSummaryModel
    _label = 'review OSD summary'
    _required_elems = ['_root']
