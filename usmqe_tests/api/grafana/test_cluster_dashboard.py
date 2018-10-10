"""
REST API test suite - Grafana dashboard cluster-dashboard
"""

import pytest
from usmqe.api.grafanaapi import grafanaapi
from usmqe.api.graphiteapi import graphiteapi
from usmqe.gluster.gluster import GlusterCommon


LOGGER = pytest.get_logger('cluster_dashboard', module=True)
"""
Setup
=====

Prepare USM cluster accordingly to documentation.
``GRAFANA`` for this file stands for Grafana API url used by tested Tendrl
server.
``GRAPHITE`` for this file stands for Graphite API url used by tested Tendrl
server.

"""


@pytest.mark.author("fbalak@redhat.com")
def test_cluster_dashboard_layout():
    """
    layout
    ******

    Description
    ===========

    Check that layout of dashboard is according to specification:
    ``https://github.com/Tendrl/specifications/issues/222``
    """
    grafana = grafanaapi.GrafanaApi()

    """
    .. test_step:: 1

        Send **GET** request to:
        ``GRAFANA/dashboards/db/cluster-dashboard`` and get layout structure.
        Compare structure of panels and rows as defined in specification:
        ``https://github.com/Tendrl/specifications/issues/222``

    .. test_result:: 1

        Defined structure and structure from Grafana API are equivalent.
    """

    structure_defined = {
        'Header': [],
        'Top Consumers': [
            'Top 5 Utilization by Bricks',
            'Top 5 Utilization by Volume',
            'CPU Utilization by Host',
            'Memory Utilization by Host',
            'Ping Latency'],
        'At-a-glance': [
            'Health',
            'Snapshots',
            'Hosts',
            'Volumes',
            'Bricks',
            'Geo-Replication Session',
            'Connections',
            'IOPS',
            'Capacity Utilization',
            'Capacity Available',
            'Throughput'],
        'Status': [
            'Volume Status',
            'Host Status',
            'Brick Status']}
    grafana.compare_structure(structure_defined, "cluster-dashboard")


@pytest.mark.author("fbalak@redhat.com")
def test_hosts_panel_status(cluster_reuse):
    """
    API-grafana: hosts
    *******************

    Description
    ===========

    Check that Grafana panel *Hosts* is showing correct values.
    """
    if cluster_reuse["short_name"]:
        cluster_identifier = cluster_reuse["short_name"]
    else:
        cluster_identifier = cluster_reuse["integration_id"]
    gluster = GlusterCommon()
    states = gluster.get_cluster_hosts_connection_states(
        pytest.config.getini("usm_cluster_member"))
    grafana = grafanaapi.GrafanaApi()
    graphite = graphiteapi.GraphiteApi()
    """
    .. test_step:: 1

        Send **GET** request to:
        ``GRAFANA/dashboards/db/cluster-dashboard``.

    .. test_result:: 1

        JSON structure containing data related to layout is returned.
    """

    layout = grafana.get_dashboard("cluster-dashboard")
    assert len(layout) > 0

    """
    structure of grafana data:

    {
    ...
    "dashboard":
        "rows":
            [
                ...
                {
                ...
                "displayName": ...,
                "panels":
                    [
                        ...
                        {
                            ...
                            targets:
                                [
                                    ...
                                    {
                                        "refid": ...,
                                        "target": ...,
                                        ...
                                    }
                                    ...
                                ]
                            ...
                        }
                    ...
                    ]
                ...
                }
            ...
            ]
    """
    dashboard_rows = layout["dashboard"]["rows"]
    assert len(dashboard_rows) > 0
    # first row contains some links links and navigation
    assert len(dashboard_rows[0]) > 0
    # second row contains At-a-glance panels
    assert len(dashboard_rows[1]) > 0
    # third row contains Top Consumers panels
    assert len(dashboard_rows[2]) > 0
    # fourth row contains Status panels
    assert len(dashboard_rows[3]) > 0

    panels = dashboard_rows[1]["panels"]
    panel = [
        panel for panel in panels
        if "displayName" in panel and panel["displayName"] == "Hosts"
            ]
    """
    .. test_step:: 2

        Send **GET** request to ``GRAPHITE/render?target=[target]&format=json``
        where [target] is part of uri obtained from previous GRAFANA call.
        There should be target for Total number of hosts.
        Compare number of hosts from Graphite with value retrieved from gluster
        command.

    .. test_result:: 2

        JSON structure containing data relatedo Total host count with last
        value coresponding with output of gluster command.
    """
    # get graphite target pointing at data containing number of host
    target = panel[0]["targets"][0]["target"]
    target = target.replace("$cluster_id", cluster_identifier)
    LOGGER.debug("Total hosts target: {}".format(target))
    g_total = graphite.get_datapoints(target)[-1][0]
    pytest.check(
        g_total == len(states),
        "Number of total hosts in graphite ({}) should be {}".format(
            g_total, len(states)))

    """
    .. test_step:: 3

        Send **GET** request to ``GRAPHITE/render?target=[target]&format=json``
        where [target] is part of uri obtained from previous GRAFANA call.
        There should be target for number of hosts that are Up.
        Compare number of hosts from Graphite with value retrieved from gluster
        command.

    .. test_result:: 3

        JSON structure containing data related to Up host count with last
        value coresponding with output of gluster command.
    """
    # get graphite target pointing at data containing number of host that are
    # up
    target = panel[0]["targets"][1]["target"]
    target = target.replace("$cluster_id", cluster_identifier)
    LOGGER.debug("Up hosts target: {}".format(target))
    g_up = graphite.get_datapoints(target)[-1][0]
    real_up = []
    for host in states.keys():
        if states[host]:
            real_up.append(host)
    pytest.check(
        g_up == len(real_up),
        "Number of hosts that are up in graphite ({}) should be {}".format(
            g_up, len(real_up)))

    """
    .. test_step:: 4

        Send **GET** request to ``GRAPHITE/render?target=[target]&format=json``
        where [target] is part of uri obtained from previous GRAFANA call.
        There should be target for number of hosts that are Down.
        Compare number of hosts from Graphite with value retrieved from gluster
        command.

    .. test_result:: 4

        JSON structure containing data related to Down host count with last
        value coresponding with output of gluster command.
    """
    # get graphite target pointing at data containing number of host that are
    # down
    target = panel[0]["targets"][2]["target"]
    target = target.replace("$cluster_id", cluster_identifier)
    LOGGER.debug("Down hosts target: {}".format(target))
    g_down = graphite.get_datapoints(target)[-1][0]
    real_down = []
    for host in states.keys():
        if not states[host]:
            real_down.append(host)
    pytest.check(
        g_down == len(real_down),
        "Number of hosts that are down in graphite ({}) should be {}".format(
            g_down, len(real_down)))
