"""
Tendrl REST API for ceph.
"""

import pytest
from usmqe.api.tendrlapi.common import TendrlApi

LOGGER = pytest.get_logger("tendrlapi_ceph", module=True)


class TendrlApiCeph(TendrlApi):
    """ Ceph methods for Tendrl REST API.
    """
    def import_ceph_cluster(self, nodes):
        """ Import Ceph cluster.

        Args:
            nodes: node list of cluster which will be imported
        """
        TendrlApi.import_cluster("ceph", nodes)
