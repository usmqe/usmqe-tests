"""
Common page model for Grafana bricks page
"""


from webstr.core import WebstrModel, By

from usmqe.web.grafana.auxiliary.models import GenericChartModel, \
    GenericDropDownListModel


class ClusterListModel(GenericDropDownListModel):
    """
    DropDown list of clusters
    """
    _title = "Cluster Id"


class BrickListModel(GenericDropDownListModel):
    """
    DropDown list of bricks
    """
    _title = "Brick Name"


class BricksUtilizationModel(GenericChartModel):
    """
    Bricks Utilization Model
    """
    _title = "Bricks Utilization"


class InodeUtilizationModel(GenericChartModel):
    """
    Inode Utilization model
    """
    _title = "Inode Utilization"
