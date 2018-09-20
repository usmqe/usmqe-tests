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
    SAMPLE_RATE = 1
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
    target_user = targets[-1][0]
    # make sure that all data in graphite are saved
    time.sleep(2)
    # get data from graphite
    from_date = int(workload_cpu_utilization["start"].timestamp())
    until_date = int(workload_cpu_utilization["end"].timestamp())
    graphite_user_cpu_data = graphite.get_datapoints(
        target_user, from_date=from_date, until_date=until_date)
    graphite_user_cpu_data = [x for x in graphite_user_cpu_data if x[0]]
    # process data from graphite
    graphite_user_cpu_mean = sum(
        [x[0] for x in graphite_user_cpu_data]) / max(
            len(graphite_user_cpu_data), 1)
    workload_time_range = workload_cpu_utilization["end"] - workload_cpu_utilization["start"]
    expected_number_of_datapoints = round(workload_time_range.total_seconds() / 60) * SAMPLE_RATE
    pytest.check(
        (len(graphite_user_cpu_data) == expected_number_of_datapoints) or
        (len(graphite_user_cpu_data) == expected_number_of_datapoints - 1),
        "Number of samples of user data should be {}, is {}.".format(
            expected_number_of_datapoints, len(graphite_user_cpu_data)))
    LOGGER.debug("CPU user utilization in Graphite: {}".format(
        graphite_user_cpu_mean))
    divergence = 10
    minimal_cpu_utilization = workload_cpu_utilization["result"] - divergence
    maximal_cpu_utilization = workload_cpu_utilization["result"] + divergence
    pytest.check(
        minimal_cpu_utilization < graphite_user_cpu_mean < maximal_cpu_utilization,
        "user CPU should be {}, user CPU in Graphite is: {}, \
applicable divergence is {}".format(
            workload_cpu_utilization["result"],
            graphite_user_cpu_mean,
            divergence))
