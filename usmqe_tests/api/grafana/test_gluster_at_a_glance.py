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
``PREFIX`` for this file is either *tendrl* or *webadmin* based on os
distribution.

"""

"""@pylatest default
Teardown
========
"""


def test_layout(os_distro):
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
    print(type(os_distro))
    if os_distro == "Red Hat Enterprise Linux Server":
        prefix = "webadmin"
    else:
        prefix = "tendrl"
    """@pylatest grafana/layout
    .. test_step:: 1

        Send **GET** request to ``GRAFANA/dashboards/db/PREFIX-gluster-at-a-glance``.

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
