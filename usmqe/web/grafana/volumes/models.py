"""
Common page model for Grafana volumes page
"""


from webstr.core import WebstrModel, By

from usmqe.web.grafana.auxiliary.models import GenericChartModel, \
    SingleStatModel, GenericDropDownListModel


class ClusterListModel(GenericDropDownListModel)
    """
    DropDown list of clusters
    """
    _title = "Cluster Id"


class VolumeListModel(GenericDropDownListModel)
    """
    DropDown list of volumes
    """
    _title = "Volume Name"


class VolumeStatusModel(SingleStatModel):
    """
    Volume Status model
    """
    _title = "Volume Status"


class BrickCountModel(SingleStatModel):
    """
    Brick Count model
    """
    _title = "Brick Count"


class ConnectionCountModel(SingleStatModel):
    """
    Connection Count model
    """
    _title = "Connection Count"


class VolumeUtilizationModel(GenericChartModel):
    """
    Volume Utilization Model
    """
    _title = "Volume Utilization"
