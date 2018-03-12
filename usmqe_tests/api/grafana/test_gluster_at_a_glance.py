"""
REST API test suite - Grafana dashboard Gluster-At-A-Glance
"""

import pytest
from usmqe.api.grafanaapi import grafanaapi


LOGGER = pytest.get_logger('gluster_at_a_glance', module=True)
"""@pylatest default
Setup
=====

Prepare USM cluster accordingly to documentation.
``GRAFANA`` for this file stands for Grafana API url used by tested Tendrl
server.
``GRAPHITE`` for this file stands for Graphite API url used by tested Tendrl
server.

"""

"""@pylatest default
Teardown
========
"""


def test_layout():
    """@pylatest grafana/layout
    API-grafana: layout
    *******************

    .. test_metadata:: author fbalak@redhat.com

    Description
    ===========

    Check that layout of dashboard is according to specification:
    ``https://github.com/Tendrl/specifications/issues/222``
    """
    api = grafanaapi.GrafanaApi()
    """@pylatest grafana/layout
    .. test_step:: 1

        Send **GET** request to ``GRAFANA/dasboards/db/gluster-at-a-glance``.

    .. test_result:: 1

        JSON structure containing data related to layout is returned.
    """
    layout = api.get_dashboard("tendrl-gluster-at-a-glance")
    pytest.check(
        len(layout) > 0,
        layout)

# TODO(fbalak) check all rows and panels are in place
