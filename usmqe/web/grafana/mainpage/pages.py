"""
Main Grafana page abstraction
"""

from webstr.core import WebstrPage

from usmqe.web.grafana.auxiliary.pages import SingleStat, GenericChart, \
    GenericDropDownList
import usmqe.web.grafana.mainpage.models as m_mainpage
from usmqe.web.grafana.exceptions import ValueNotFoundError

location = ':3000/dashboard/db/tendrl-gluster-at-a-glance'


class ClusterList(GenericDropDownList):
    """
    DropDown list of clusters
    """
    _model = m_mainpage.ClusterListModel
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


class Status(SingleStat):
    """
    page object for Status panel
    """
    _model = m_mainpage.StatusModel
    _label = 'Status panel'


class QuorumStatus(SingleStat):
    """
    page object for Quorum Status panel
    """
    _model = m_mainpage.QuorumStatusModel
    _label = 'Quorum Status panel'


class Hosts(SingleStat):
    """
    page object for Hosts panel
    """
    _model = m_mainpage.HostsModel
    _label = 'Hosts panel'


class Volumes(SingleStat):
    """
    page object for Volumes panel
    """
    _model = m_mainpage.VolumesModel
    _label = 'Volumes panel'


class Bricks(SingleStat):
    """
    page object for Bricks panel
    """
    _model = m_mainpage.BricksModel
    _label = 'Bricks panel'


class ClusterUtilization(GenericChart):
    """
    page object for Cluster Utilization panel
    """
    _model = m_mainpage.ClusterUtilizationModel
    _label = 'Cluster Utilization panel'


class HostsUp(SingleStat):
    """
    page object for Hosts Up panel
    """
    _model = m_mainpage.HostsUpModel
    _label = 'Hosts Up panel'


class HostsDown(SingleStat):
    """
    page object for Hosts Down panel
    """
    _model = m_mainpage.HostsDownModel
    _label = 'Hosts Down panel'


class VolumesUp(SingleStat):
    """
    page object for Volumes Up panel
    """
    _model = m_mainpage.VolumesUpModel
    _label = 'Volumes Up panel'


class VolumesDown(SingleStat):
    """
    page object for Volumes Down panel
    """
    _model = m_mainpage.VolumesDownModel
    _label = 'Volumes Down panel'


class BricksUp(SingleStat):
    """
    page object for Bricks Up panel
    """
    _model = m_mainpage.BricksUpModel
    _label = 'Bricks Up panel'


class BricksDown(SingleStat):
    """
    page object for Bricks Down panel
    """
    _model = m_mainpage.BricksDownModel
    _label = 'Bricks Down panel'


class IOPSReads(GenericChart):
    """
    page object for IOPS Reads panel
    """
    _model = m_mainpage.IOPSReadsModel
    _label = 'IOPS Reads panel'


class IOPSWrites(GenericChart):
    """
    page object for IOPS Writes panel
    """
    _model = m_mainpage.IOPSWritesModel
    _label = 'IOPS Writes panel'


class InodeUtilization(GenericChart):
    """
    page object for Inode Utilization panel
    """
    _model = m_mainpage.InodeUtilizationModel
    _label = 'Inode Utilization panel'
