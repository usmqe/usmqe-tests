"""
REST API test suite - Grafana dashboard volume-dashboard
"""

import pytest
import time
from usmqe.api.grafanaapi import grafanaapi
from usmqe.api.graphiteapi import graphiteapi


LOGGER = pytest.get_logger('volume_dashboard', module=True)


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


@pytest.mark.author("fbalak@redhat.com")
def test_capacity_utilization_gauge(
        workload_capacity_utilization, cluster_reuse):
    """
    Check that Grafana panel *Capacity Utilization* gauge chart is showing
    correct values.
    """
    # TODO(fbalak): get this number dynamically
    # number of samples from graphite target per minute
    if cluster_reuse["short_name"]:
        cluster_identifier = cluster_reuse["short_name"]
    else:
        cluster_identifier = cluster_reuse["integration_id"]

    grafana = grafanaapi.GrafanaApi()
    graphite = graphiteapi.GraphiteApi()

    capacity_panel = grafana.get_panel(
        "Capacity Utilization",
        row_title="Capacity",
        dashboard="volume-dashboard",
        panel_type="singlestat")

    """
    :step:
      Send **GET** request to ``GRAPHITE/render?target=[target]&format=json``
      where [target] is part of uri obtained from previous GRAFANA call.
      There should be target for capacity utilization of a host.
      Compare number of hosts from Graphite with value retrieved from
      ``workload_capacity_utilization`` fixture.
    :result:
      JSON structure containing data related to capacity utilization is similar
      to values set by ``workload_capacity_utilization`` fixture in given time.
    """
    # get graphite target pointing at data containing number of host
    targets = grafana.get_panel_chart_targets(capacity_panel, cluster_identifier)
    targets_used = (targets[0][0],)
    for key, target_expected in enumerate((
            "pcnt_used",)):
        pytest.check(
            targets_used[key].endswith(target_expected),
            "There is used target that ends with `{}`".format(target_expected))
    # make sure that all data in graphite are saved
    time.sleep(2)
    graphite.compare_data_mean(
        workload_capacity_utilization["result"],
        targets_used,
        workload_capacity_utilization["start"],
        workload_capacity_utilization["end"],
        divergence=15)
