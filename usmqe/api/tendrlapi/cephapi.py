"""
Tendrl REST API for ceph.
"""

import pytest
from usmqe.api.tendrlapi.common import TendrlApi

LOGGER = pytest.get_logger("tendrlapi_ceph", module=True)


class TendrlApiCeph(TendrlApi):
    """ Ceph methods for Tendrl REST API.
    """
    pass
