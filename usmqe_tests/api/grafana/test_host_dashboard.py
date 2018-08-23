"""
REST API test suite - Grafana dashboard host-dashboard
"""

import pytest
from usmqe.api.grafanaapi import grafanaapi
from usmqe.api.graphiteapi import graphiteapi
from usmqe.gluster.gluster import GlusterCommon


LOGGER = pytest.get_logger('host_dashboard', module=True)
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

        Send **GET** request to:
        ``GRAFANA/dashboards/db/host-dashboard``.

    .. test_result:: 1

        JSON structure containing data related to layout is returned.
    """
    layout = api.get_dashboard("host-dashboard")
    pytest.check(
        len(layout) > 0,
        "cluster-dashboard layout should not be empty")

    """@pylatest grafana/layout
    .. test_step:: 2

        Compare structure of panels and rows as defined in specification:
        ``https://github.com/Tendrl/specifications/issues/222``

    .. test_result:: 2

        Defined structure and structure from Grafana API are equivalent.
    """
    structure_defined = {
        'Network': [
            'Throughput',
            'Dropped Packets Per Second',
            'Errors Per Second'],
        'At-a-Glance': [
            'Health',
            'Bricks',
            'Brick Status',
            'Memory Available',
            'Memory Utilization',
            'Swap Free',
            'Swap Utilization',
            'CPU Utilization',
            'Brick IOPS'],
        'Capacity & Disk Load': [
            'Total Brick Capacity Utilization',
            'Total Brick Capacity Utilization',
            'Total Brick Capacity Available',
            'Weekly Growth Rate',
            'Weeks Remaining',
            'Top Bricks by Capacity Percent Utilized',
            'Top Bricks by Total Capacity',
            'Top Bricks by Capacity Utilized',
            'Disk Throughput',
            'Disk IOPS',
            'Disk IO Latency']}
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


def test_cpu_utilization(measured_cpu_utilization, cluster_reuse):
    """@pylatest grafana/cpu_utilization
    API-grafana: cpu_utilization
    *******************

    .. test_metadata:: author fbalak@redhat.com

    Description
    ===========

    Check that Grafana panel *CPU Utilization* is showing correct values.
    """
    if cluster_reuse["short_name"]:
        cluster_identifier = cluster_reuse["short_name"]
    else:
        cluster_identifier = cluster_reuse["integration_id"]
    print(measured_cpu_utilization)
    grafana = grafanaapi.GrafanaApi()
    graphite = graphiteapi.GraphiteApi()
    """@pylatest grafana/hosts
    .. test_step:: 1
        Send **GET** request to:
        ``GRAFANA/dashboards/db/host-dashboard``.
    .. test_result:: 1
        JSON structure containing data related to layout is returned.
    """

    layout = grafana.get_dashboard("host-dashboard")
    assert len(layout) > 0
    dashboard_rows = layout["dashboard"]["rows"]

    # get CPU Utilization panel from first row
    panels = dashboard_rows[0]["panels"]
    panel = [
        panel for panel in panels
        if "title" in panel
            and panel["title"] == "CPU Utilization"]

    """@pylatest grafana/cpu_utilization
    .. test_step:: 2
        Send **GET** request to ``GRAPHITE/render?target=[target]&format=json``
        where [target] is part of uri obtained from previous GRAFANA call.
        There should be target for CPU utilization of a host.
        Compare number of hosts from Graphite with value retrieved from
        ``measured_cpu_utilization`` fixture.
    .. test_result:: 2
        JSON structure containing data related to CPU utilization is similar
        to values set by ``measured_cpu_utilization`` fixture in given time.
    """
    # get graphite target pointing at data containing number of host
    target = panel[0]["targets"][0]["target"]
    target = target.replace("$cluster_id", cluster_identifier)
    target = target.replace("$host_name", pytest.config.getini(
        "usm_cluster_member").replace(".", "_"))
    target = target.strip("aliasSub(groupByNode(")
    target = target.split("},", 1)[0]
    target_base, target_options = target.rsplit(".{", 1)
    target_options = target_options
    LOGGER.debug("target: {}".format(target))
    LOGGER.debug("target_base: {}".format(target_base))
    LOGGER.debug("target_options: {}".format(target_options))
    pytest.check(
        target_options == "percent-user,percent-system",
        "The panel CPU Utilization is composed of user and system parts")
    target_user, target_system = [target_base + x for x
        in target_options.split(",")]
    LOGGER.debug("CPU user utilization target: {}".format(target_user))
    LOGGER.debug("CPU system utilization target: {}".format(target_system))
    graphite_user_cpu = graphite.get_datapoints(target_user)[-1][0]
    graphite_system_cpu = graphite.get_datapoints(target_system)[-1][0]
