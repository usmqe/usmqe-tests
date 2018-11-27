"""
REST API test suite - Grafana dashboard volume-dashboard
"""

import pytest
from usmqe.api.grafanaapi import grafanaapi


LOGGER = pytest.get_logger('volume_dashboard', module=True)


@pytest.mark.testready
@pytest.mark.author("ebondare@redhat.com")
def test_volume_dashboard_layout():
    """
    Check that layout of dashboard is according to specification:
    ``https://github.com/Tendrl/specifications/issues/224``
    """
    grafana = grafanaapi.GrafanaApi()

    """
    :step:
      Send **GET** request to:
      ``GRAFANA/dashboards/db/volume-dashboard`` and get layout structure.
      Compare structure of panels and rows as defined in specification:
      ``https://github.com/Tendrl/specifications/issues/224``
    :result:
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
