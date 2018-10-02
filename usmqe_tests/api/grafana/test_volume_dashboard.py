"""
REST API test suite - Grafana dashboard volume-dashboard
"""

import pytest
from usmqe.api.grafanaapi import grafanaapi


LOGGER = pytest.get_logger('volume_dashboard', module=True)
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


def test_volume_dashboard_layout():
    """@pylatest grafana/layout
    API-grafana: layout
    *******************

    .. test_metadata:: author ebondare@redhat.com

    Description
    ===========

    Check that layout of dashboard is according to specification:
    ``https://github.com/Tendrl/specifications/issues/224``
    """
    grafana = grafanaapi.GrafanaApi()

    """@pylatest grafana/layout
    .. test_step:: 1

        Send **GET** request to:
        ``GRAFANA/dashboards/db/volume-dashboard`` and get layout structure.
        Compare structure of panels and rows as defined in specification:
        ``https://github.com/Tendrl/specifications/issues/224``

    .. test_result:: 1

        Defined structure and structure from Grafana API are equivalent.
    """

    structure_defined = {
        'At-a-Glance': [
            'Health',
            'Bricks',
            'Brick Status',
            'Geo-Replication Sessions',
            'Rebalance',
            'Rebalance Status',
            'Snapshots'],
        'Capacity': [
            'Capacity Utilization',
            'Capacity Available',
            'Weekly Growth Rate',
            'Weeks Remaining',
            'Capacity Utilization'],
        'Performance': [
            'IOPS',
            'LVM Thin Pool Metadata %',
            'LVM Thin Pool Data Usage %'],
        'Profiling Information': [
            'Top File Operations',
            'File Operations For Locks',
            'File Operations for Read/Write',
            'File Operations for Inode Operations',
            'File Operations for Entry Operations']}
    grafana.compare_structure(structure_defined, "volume-dashboard")
