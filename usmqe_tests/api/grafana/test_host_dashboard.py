"""
REST API test suite - Grafana dashboard host-dashboard
"""

import pytest
import time
from usmqe.api.grafanaapi import grafanaapi
from usmqe.api.graphiteapi import graphiteapi


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


def test_host_dashboard_layout():
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


def test_cpu_utilization(workload_cpu_utilization, cluster_reuse):
    """@pylatest grafana/cpu_utilization
    API-grafana: cpu_utilization
    *******************

    .. test_metadata:: author fbalak@redhat.com

    Description
    ===========

    Check that Grafana panel *CPU Utilization* is showing correct values.
    """
    # TODO(fbalak): get this number dynamically
    # number of samples from graphite target per minute
    if cluster_reuse["short_name"]:
        cluster_identifier = cluster_reuse["short_name"]
    else:
        cluster_identifier = cluster_reuse["integration_id"]

    grafana = grafanaapi.GrafanaApi()
    graphite = graphiteapi.GraphiteApi()

    cpu_panel = grafana.get_panel(
        "CPU Utilization",
        row_title="At-a-Glance",
        dashboard="host-dashboard")

    """@pylatest grafana/cpu_utilization
    .. test_step:: 2
        Send **GET** request to ``GRAPHITE/render?target=[target]&format=json``
        where [target] is part of uri obtained from previous GRAFANA call.
        There should be target for CPU utilization of a host.
        Compare number of hosts from Graphite with value retrieved from
        ``workload_cpu_utilization`` fixture.
    .. test_result:: 2
        JSON structure containing data related to CPU utilization is similar
        to values set by ``workload_cpu_utilization`` fixture in given time.
    """
    # get graphite target pointing at data containing number of host
    targets = grafana.get_panel_chart_targets(cpu_panel, cluster_identifier)
    pytest.check(
        [t.split(".")[-1] for t in targets[-1]] == ["percent-user", "percent-system"],
        "The panel CPU Utilization is composed of user and system parts")
    targets_used = (targets[-1][0],)
    # make sure that all data in graphite are saved
    time.sleep(2)
    graphite.compare_data_mean(
        workload_cpu_utilization["result"],
        targets_used,
        workload_cpu_utilization["start"],
        workload_cpu_utilization["end"])


def test_memory_utilization(workload_memory_utilization, cluster_reuse):
    """@pylatest grafana/memory_utilization
    API-grafana: memory_utilization
    *******************

    .. test_metadata:: author fbalak@redhat.com

    Description
    ===========

    Check that Grafana panel *memory Utilization* is showing correct values.
    """
    # TODO(fbalak): get this number dynamically
    # number of samples from graphite target per minute
    if cluster_reuse["short_name"]:
        cluster_identifier = cluster_reuse["short_name"]
    else:
        cluster_identifier = cluster_reuse["integration_id"]

    grafana = grafanaapi.GrafanaApi()
    graphite = graphiteapi.GraphiteApi()

    memory_panel = grafana.get_panel(
        "Memory Utilization",
        row_title="At-a-Glance",
        dashboard="host-dashboard")

    """@pylatest grafana/memory_utilization
    .. test_step:: 2
        Send **GET** request to ``GRAPHITE/render?target=[target]&format=json``
        where [target] is part of uri obtained from previous GRAFANA call.
        There should be target for memory utilization of a host.
        Compare number of hosts from Graphite with value retrieved from
        ``workload_memory_utilization`` fixture.
    .. test_result:: 2
        JSON structure containing data related to memory utilization is similar
        to values set by ``workload_memory_utilization`` fixture in given time.
    """
    # get graphite target pointing at data containing number of host
    targets = grafana.get_panel_chart_targets(memory_panel, cluster_identifier)
    targets_used = (targets[0][0], targets[1][0], targets[-1][0])
    for key, target_expected in enumerate((
            "memory.percent-buffered",
            "memory.percent-cached",
            "memory.percent-used")):
        pytest.check(
            targets_used[key].endswith(target_expected),
            "There is used target that ends with `{}`".format(target_expected))
    # make sure that all data in graphite are saved
    time.sleep(2)
    graphite.compare_data_mean(
        workload_memory_utilization["result"],
        targets_used,
        workload_memory_utilization["start"],
        workload_memory_utilization["end"],
        divergence=15)
