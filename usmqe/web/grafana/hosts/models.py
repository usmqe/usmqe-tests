"""
Common page model for Grafana volumes page
"""


from webstr.core import WebstrModel, By

from usmqe.web.grafana.auxiliary.models import GenericChartModel, \
    SingleStatModel, GenericDropDownListModel


class ClusterListModel(GenericDropDownListModel):
    """
    DropDown list of clusters
    """
    _title = "Cluster Id"


class HostListModel(GenericDropDownListModel):
    """
    DropDown list of hosts
    """
    _title = "Host Name"


class MemoryFreeModel(SingleStatModel):
    """
    Memory Free model
    """
    _title = "Memory Free"


class MemoryUsedModel(SingleStatModel):
    """
    Memory Used model
    """
    _title = "Memory Used"


class StorageFreeModel(SingleStatModel):
    """
    Storage Free model
    """
    _title = "Storage Free"


class StorageUsedModel(SingleStatModel):
    """
    Storage Used model
    """
    _title = "Storage Used"


class MemoryModel(GenericChartModel):
    """
    Memory Model
    """
    _title = "Memory"


class StorageModel(GenericChartModel):
    """
    Storage Model
    """
    _title = "Storage"


class SwapModel(GenericChartModel):
    """
    Swap Model
    """
    _title = "Swap"


class CPUModel(GenericChartModel):
    """
    CPU Model
    """
    _title = "CPU"


class ThroughputClusterNetworkModel(GenericChartModel):
    """
    Throughput - Cluster Network Model
    """
    _title = "Throughput - Cluster Network"
