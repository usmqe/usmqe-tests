"""
Grafana Volumes page abstraction
"""

from webstr.core import WebstrPage

from usmqe.web.grafana.auxiliary.pages import SingleStat, GenericChart, \
    GenericDropDownList
import usmqe.web.grafana.hosts.models as m_hosts

location = ':3000/dashboard/db/tendrl-gluster-hosts'


class ClusterList(GenericDropDownList):
    """
    DropDown list of clusters
    """
    _model = m_hosts.ClusterListModel
    _label = 'Cluster select list'

    def selected_cluster(self):
        """ returns selected cluster """
        return self.value

    def choose_cluster(self, cluster_id):
        """
        Select cluster

        Parameters:
            cluster_id (string): cluster id
        """
        self.value = cluster_id


class HostList(GenericDropDownList):
    """
    DropDown list of hosts
    """
    _model = m_hosts.HostListModel
    _label = 'Host select list'

    def selected_host(self):
        """ returns selected host """
        return self.value

    def choose_host(self, host_name):
        """
        Select host

        Parameters:
            host_name (string): host name
        """
        self.value = host_name


class MemoryFree(SingleStat):
    """
    page object for Memory Free panel
    """
    _model = m_hosts.MemoryFreeModel
    _label = 'Memory Free panel'


class MemoryUsed(SingleStat):
    """
    page object for Memory Used panel
    """
    _model = m_hosts.MemoryUsedModel
    _label = 'Memory Used panel'


class StorageFree(SingleStat):
    """
    page object for Storage Free panel
    """
    _model = m_hosts.StorageFreeModel
    _label = 'Storage Free panel'


class StorageUsed(SingleStat):
    """
    page object for Storage Used panel
    """
    _model = m_hosts.StorageUsedModel
    _label = 'Storage Used panel'


class Memory(GenericChart):
    """
    page object for Memory panel
    """
    _model = m_hosts.MemoryModel
    _label = 'Memory panel'


class Storage(GenericChart):
    """
    page object for Storage panel
    """
    _model = m_hosts.StorageModel
    _label = 'Storage panel'


class Swap(GenericChart):
    """
    page object for Swap panel
    """
    _model = m_hosts.SwapModel
    _label = 'Swap panel'


class CPU(GenericChart):
    """
    page object for CPU panel
    """
    _model = m_hosts.CPUModel
    _label = 'CPU panel'


class ThroughputClusterNetwork(GenericChart):
    """
    page object for Throughput - Cluster Network panel
    """
    _model = m_hosts.ThroughputClusterNetworkModel
    _label = 'Throughput - Cluster Network panel'
