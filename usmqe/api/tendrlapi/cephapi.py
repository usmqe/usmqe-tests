"""
Tendrl REST API for ceph.
"""

import pytest
from usmqe.api.tendrlapi.common import TendrlApi

LOGGER = pytest.get_logger("tendrlapi_ceph", module=True)


class TendrlApiCeph(TendrlApi):
    """ Ceph methods for Tendrl REST API.
    """
    def import_cluster(self, nodes, asserts_in=None):
        """ Import Ceph cluster.

        Args:
            nodes (list): node list of cluster which will be imported
            asserts_in (dict): assert values for this call and this method
        """
        return super().import_cluster(nodes, "ceph", asserts_in)
