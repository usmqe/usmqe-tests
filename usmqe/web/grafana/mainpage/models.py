"""
Common page model for Grafana main page
"""


from usmqe.web.grafana.auxiliary.models import SingleStatModel, \
    GenericChartModel, GenericDropDownListModel


class ClusterListModel(GenericDropDownListModel):
    """
    DropDown list of clusters
    """
    _title = "Cluster Id"


class StatusModel(SingleStatModel):
    """
    Status model
    """
    _title = "Status"


class QuorumStatusModel(SingleStatModel):
    """
    Quorum Status model
    """
    _title = "Quorum Status"


class HostsModel(SingleStatModel):
    """
    Hosts model
    """
    _title = "Hosts"


class VolumesModel(SingleStatModel):
    """
    Volumes model
    """
    _title = "Volumes"


class BricksModel(SingleStatModel):
    """
    Bricks model
    """
    _title = "Bricks"


class ClusterUtilizationModel(GenericChartModel):
    """
    Cluster Utilization Model
    """
    _title = "Cluster Utilization"


class HostsUpModel(SingleStatModel):
    """
    Hosts Up model
    """
    _title = "Hosts Up"


class HostsDownModel(SingleStatModel):
    """
    Hosts Down model
    """
    _title = "Hosts Down"


class VolumesUpModel(SingleStatModel):
    """
    Volumes Up model
    """
    _title = "Volumes Up"


class VolumesDownModel(SingleStatModel):
    """
    Volumes Down model
    """
    _title = "Volumes Down"


class BricksUpModel(SingleStatModel):
    """
    Bricks Up model
    """
    _title = "Bricks Up"


class BricksDownModel(SingleStatModel):
    """
    Bricks Down model
    """
    _title = "Bricks Down"


class IOPSReadsModel(GenericChartModel):
    """
    IOPS Reads model
    """
    _title = "IOPS Reads"


class IOPSWritesModel(GenericChartModel):
    """
    IOPS Writes model
    """
    _title = "IOPS Writes"


class InodeUtilizationModel(GenericChartModel):
    """
    Inode Utilization model
    """
    _title = "Inode Utilization"
