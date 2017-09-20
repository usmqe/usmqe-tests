"""
Grafana Volumes page abstraction
"""

from usmqe.web.grafana.auxiliary.pages import SingleStat, GenericChart, \
    GenericDropDownList
import usmqe.web.grafana.volumes.models as m_volumes

location = ':3000/dashboard/db/tendrl-gluster-volumes'


class ClusterList(GenericDropDownList):
    """
    DropDown list of clusters
    """
    _model = m_volumes.ClusterListModel
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


class VolumeList(GenericDropDownList):
    """
    DropDown list of volumes
    """
    _model = m_volumes.VolumeListModel
    _label = 'Volume select list'

    def selected_volume(self):
        """ returns selected volume """
        return self.value

    def choose_brick(self, volume_name):
        """
        Select volume

        Parameters:
            volume_name (string): volume name
        """
        self.value = volume_name


class VolumeStatus(SingleStat):
    """
    page object for Volume Status panel
    """
    _model = m_volumes.VolumeStatusModel
    _label = 'Volume Status panel'


class BrickCount(SingleStat):
    """
    page object for Brick Count panel
    """
    _model = m_volumes.BrickCountModel
    _label = 'Brick Count panel'


class ConnectionCount(SingleStat):
    """
    page object for Connection Count panel
    """
    _model = m_volumes.ConnectionCountModel
    _label = 'Connection Count panel'


class VolumeUtilization(GenericChart):
    """
    page object for Volume Utilization panel
    """
    _model = m_volumes.VolumeUtilizationModel
    _label = 'Volume Utilization panel'
