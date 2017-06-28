"""
Import Cluster wizard module.
"""


import copy

import webstr.patternfly.contentviews.pages as contentviews

import usmqe.web.tendrl.mainpage.clusters.create_cluster_wizard.\
    gluster.models as m_gluster
from usmqe.web.tendrl.auxiliary.pages import ListMenu
from usmqe.web.tendrl.mainpage.clusters.create_cluster_wizard.\
    general.pages import StepButtons


class StepGeneral(StepButtons):
    """
    page object for create gluster cluster - General step
    """
    _model = m_gluster.StepGeneralModel
    _label = 'create gluster cluster - General step'
    _required_elems = copy.deepcopy(StepButtons._required_elems)
    _required_elems.extend(['service', 'name'])

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


class StepNetworkAndHosts(ListMenu, StepButtons):
    """
    page object for create gluster cluster - "Network & Hosts" step
    """
    _model = m_gluster.StepNetworkAndHostsModel
    _label = 'create gluster cluster - Network & Hosts step'
    _required_elems = copy.deepcopy(StepButtons._required_elems)
    _required_elems.extend(['select_all', 'deselect_all', 'cluster_network'])

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


class CreateHostsItem(contentviews.ListViewRow):
    """
    An item (row) in a Hosts list.
    """
    _model = m_gluster.CreateHostsItemModel
    _label = 'create gluster cluster - Hosts row'
    _required_elems = [
        'check',
        'name',
        'cluster_net_if',
        'cluster_net_address',
        'disks',
        'capacity']

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
    _model = m_gluster.CreateHostsListModel
    _label = 'create gluster cluster hosts'
    _row_class = CreateHostsItem


class StepReview(StepButtons):
    """
    page object for create gluster cluster - "Review" step
    """
    _model = m_gluster.StepReviewModel
    _label = 'create gluster cluster - Review step'
    _required_elems = copy.deepcopy(StepButtons._required_elems)
    _required_elems.extend([
        'name',
        'devices',
        'capacity',
        'cluster_network',
        'host_nr'])


class HostsSumItem(contentviews.ListViewRow):
    """
    Hosts summary row
    """
    _model = m_gluster.HostsSumItemModel
    _label = 'create gluster cluster - Hosts summary row'
    _required_elems = [
        'name',
        'settings',
        'interface',
        'address']


class HostsSumList(contentviews.ListView):
    """
    Page object for list of nodes/hosts.
    """
    _model = m_gluster.HostsSumListModel
    _label = 'create gluster cluster Hosts summary'
    _row_class = HostsSumItem
