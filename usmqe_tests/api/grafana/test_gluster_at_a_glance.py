"""
REST API test suite - Grafana dashboard Gluster-At-A-Glance
"""

import pytest
from usmqe.api.grafanaapi import grafanaapi
from usmqe.api.graphiteapi import graphiteapi
from usmqe.gluster.gluster import GlusterCommon


LOGGER = pytest.get_logger('gluster_at_a_glance', module=True)
"""@pylatest default
Setup
=====

Prepare USM cluster accordingly to documentation.
``GRAFANA`` for this file stands for Grafana API url used by tested Tendrl
server.
``GRAPHITE`` for this file stands for Graphite API url used by tested Tendrl
server.
``PREFIX`` for this file is either *tendrl* or *webadmin* based on os
distribution.

"""

"""@pylatest default
Teardown
========
"""


def test_layout(os_info):
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
    if os_info['name'] == "Red Hat Enterprise Linux Server":
        prefix = "webadmin"
    else:
        prefix = "tendrl"
    """@pylatest grafana/layout
    .. test_step:: 1

        Send **GET** request to:
        ``GRAFANA/dashboards/db/PREFIX-gluster-at-a-glance``.

    .. test_result:: 1

        JSON structure containing data related to layout is returned.
    """
    layout = api.get_dashboard("{}-gluster-at-a-glance".format(prefix))
    pytest.check(
        len(layout) > 0,
        layout)

    """@pylatest grafana/layout
    .. test_step:: 2

        Compare structure of panels and rows as defined in specification:
        ``https://github.com/Tendrl/specifications/issues/222``

    .. test_result:: 2

        Defined structure and structure from Grafana API are equivalent.
    """
    structure_defined = {
        'Header': [],
        'Top Consumers': [
            'Top 5 Utilization by Bricks',
            'Top 5 Utilization by Volume',
            'CPU Utilization by Host',
            'Memory Utilization by Host',
            'Ping Latency Trend'],
        'At-a-glance': [
            'Health',
            'Snapshots',
            'Hosts',
            'Volumes',
            'Bricks',
            'Geo-Replication Session',
            'Connection Trend',
            'IOPS',
            'Capacity Utilization',
            'Capacity Available',
            'Weekly Growth Rate',
            'Weeks Remaining',
            'Throughput Trend'],
        'Status': [
            'Volume Status',
            'Host Status',
            'Brick Status']}
    structure = {}
    for row in layout["dashboard"]["rows"]:
        structure[row["title"]] = []
        for panel in row["panels"]:
            if panel["title"]:
                structure[row["title"]].append(panel["title"])
            elif "displayName" in panel.keys() and panel["displayName"]:
                structure[row["title"]].append(panel["displayName"])

    LOGGER.debug("defined layout structure = {}".format(structure_defined))
    LOGGER.debug("layout structure in grafana = {}".format(structure))
    pytest.check(
        structure_defined == structure,
        "defined structure of panels should equal to structure in grafana")


def test_status(os_info, cluster_reuse):
    """@pylatest grafana/status
    API-grafana: hosts
    *******************

    .. test_metadata:: author fbalak@redhat.com

    Description
    ===========

    Check that Grafana panel *Hosts* is showing correct values.
    """
    gluster = GlusterCommon()
    states = gluster.get_cluster_hosts_connection_states(
        pytest.config.getini("usm_cluster_member"))
    grafana = grafanaapi.GrafanaApi()
    graphite = graphiteapi.GraphiteApi()
    if os_info['name'] == "Red Hat Enterprise Linux Server":
        prefix = "webadmin"
    else:
        prefix = "tendrl"
    """@pylatest grafana/hosts
    .. test_step:: 1

        Send **GET** request to:
        ``GRAFANA/dashboards/db/PREFIX-gluster-at-a-glance``.

    .. test_result:: 1

        JSON structure containing data related to layout is returned.
    """

    layout = grafana.get_dashboard("{}-gluster-at-a-glance".format(prefix))
    pytest.check(
        len(layout) > 0,
        layout)
    """@pylatest grafana/hosts
    .. test_step:: 2

        Send **GET** request to ``GRAPHITE/render?target=[target]&format=json``
        where [target] is part of uri obtained from previous GRAFANA call.
        There should be target for Total number of hosts.
        Compare number of hosts from Graphite with value retrieved from gluster
        command.

    .. test_result:: 2

        JSON structure containing data related to Total host count with last
        value coresponding with output of gluster command.
    """
    target = [
        panel for panel in layout["dashboard"]["rows"][1]["panels"]
        if "clusterName" in panel and panel["clusterName"] == "Hosts"
            ][0]["targets"][0]["target"]
    target = target.replace("$cluster_id", cluster_reuse["integration_id"])
    LOGGER.debug("Total hosts target: {}".format(target))
    g_total = graphite.get_datapoints(target)[-1][0]
    pytest.check(
        g_total == len(states),
        "Number of total hosts in graphite ({}) should be {}".format(
            g_total, len(states)))

    """@pylatest grafana/hosts
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
    target = [
        panel for panel in layout["dashboard"]["rows"][1]["panels"]
        if "clusterName" in panel and panel["clusterName"] == "Hosts"
            ][0]["targets"][1]["target"]
    target = target.replace("$cluster_id", cluster_reuse["integration_id"])
    LOGGER.debug("Up hosts target: {}".format(target))
    g_up = graphite.get_datapoints(target)[-1][0]
    t_up = []
    for host in states.keys():
        if states[host]:
            t_up.append(host)
    pytest.check(
        g_up == len(t_up),
        "Number of hosts that are up in graphite ({}) should be {}".format(
            g_up, len(t_up)))

    """@pylatest grafana/hosts
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
    target = [
        panel for panel in layout["dashboard"]["rows"][1]["panels"]
        if "clusterName" in panel and panel["clusterName"] == "Hosts"
            ][0]["targets"][2]["target"]
    target = target.replace("$cluster_id", cluster_reuse["integration_id"])
    LOGGER.debug("Down hosts target: {}".format(target))
    g_down = graphite.get_datapoints(target)[-1][0]
    t_down = []
    for host in states.keys():
        if not states[host]:
            t_down.append(host)
    pytest.check(
        g_down == len(t_down),
        "Number of hosts that are down in graphite ({}) should be {}".format(
            g_down, len(t_down)))
