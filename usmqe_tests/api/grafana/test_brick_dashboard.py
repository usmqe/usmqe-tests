"""
REST API test suite - Grafana dashboard brick-dashboard
"""

import pytest
from usmqe.api.grafanaapi import grafanaapi


LOGGER = pytest.get_logger('brick_dashboard', module=True)


@pytest.mark.testready
@pytest.mark.author("ebondare@redhat.com")
def test_brick_dashboard_layout():
    """
    Check that layout of dashboard is according to specification:
    ``https://github.com/Tendrl/specifications/issues/230``
    """
    grafana = grafanaapi.GrafanaApi()
    """
    :step:
      Send **GET** request to:
      ``GRAFANA/dashboards/db/brick-dashboard`` and get layout structure.
      Compare structure of panels and rows as defined in specification:
      ``https://github.com/Tendrl/specifications/issues/230``
    :result:
      Defined structure and structure from Grafana API are equivalent.
    """

    structure_defined = {
        'At-a-Glance': [
            'Status',
            'Capacity Utilization',
            'Capacity Utilization',
            'Capacity Available',
            'Weekly Growth Rate',
            'Weeks Remaining',
            'Healing',
            'Brick IOPS',
            'LVM Thin Pool Meta Data %',
            'LVM Thin Pool Data Usage %'],
        'Disk Load': [
            'Throughput',
            'Disk IOPS',
            'Latency']}

    grafana.compare_structure(structure_defined, "brick-dashboard")
