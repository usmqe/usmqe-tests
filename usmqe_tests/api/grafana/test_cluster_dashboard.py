"""
REST API test suite - Grafana dashboard cluster-dashboard
"""

import pytest
import time
from usmqe.api.grafanaapi import grafanaapi
from usmqe.api.graphiteapi import graphiteapi
from usmqe.gluster.gluster import GlusterCommon
from usmqe.usmqeconfig import UsmConfig


LOGGER = pytest.get_logger('cluster_dashboard', module=True)
CONF = UsmConfig()


@pytest.mark.testready
@pytest.mark.author("fbalak@redhat.com")
def test_cluster_dashboard_layout():
    """
    Check that layout of dashboard is according to specification:
    ``https://github.com/Tendrl/specifications/issues/222``
    """
    grafana = grafanaapi.GrafanaApi()

    """
    :step:
      Send **GET** request to:
      ``GRAFANA/dashboards/db/cluster-dashboard`` and get layout structure.
      Compare structure of panels and rows as defined in specification:
      ``https://github.com/Tendrl/specifications/issues/222``
    :result:
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


@pytest.mark.testready
@pytest.mark.author("fbalak@redhat.com")
@pytest.mark.ansible_playbook_setup('test_setup.graphite_access.yml')
@pytest.mark.ansible_playbook_teardown('test_teardown.graphite_access.yml')
def test_hosts_panel_status(ansible_playbook, managed_cluster):
    """
    Check that Grafana panel *Hosts* is showing correct values.
    """
    if managed_cluster["short_name"]:
        cluster_identifier = managed_cluster["short_name"]
    else:
        cluster_identifier = managed_cluster["integration_id"]
    gluster = GlusterCommon()
    states = gluster.get_cluster_hosts_connection_states(
        CONF.config["usmqe"]["cluster_member"])
    grafana = grafanaapi.GrafanaApi()
    graphite = graphiteapi.GraphiteApi()
    """
    :step:
      Send **GET** request to:
      ``GRAFANA/dashboards/db/cluster-dashboard``.
    :result:
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
    :step:
      Send **GET** request to ``GRAPHITE/render?target=[target]&format=json``
      where [target] is part of uri obtained from previous GRAFANA call.
      There should be target for Total number of hosts.
      Compare number of hosts from Graphite with value retrieved from gluster
      command.
    :result:
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
    :step:
      Send **GET** request to ``GRAPHITE/render?target=[target]&format=json``
      where [target] is part of uri obtained from previous GRAFANA call.
      There should be target for number of hosts that are Up.
      Compare number of hosts from Graphite with value retrieved from gluster
      command.
    :result:
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
    :step:
      Send **GET** request to ``GRAPHITE/render?target=[target]&format=json``
      where [target] is part of uri obtained from previous GRAFANA call.
      There should be target for number of hosts that are Down.
      Compare number of hosts from Graphite with value retrieved from gluster
      command.
    :result:
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


@pytest.mark.testready
@pytest.mark.ansible_playbook_setup("test_setup.tendrl_services_stopped_on_nodes.yml")
@pytest.mark.ansible_playbook_setup('test_setup.graphite_access.yml')
@pytest.mark.ansible_playbook_teardown("test_teardown.tendrl_services_stopped_on_nodes.yml")
@pytest.mark.author("fbalak@redhat.com")
def test_hosts(ansible_playbook, workload_stop_nodes, managed_cluster):
    """
    Check that Grafana panel *Hosts* is showing correct values.
    """
    if managed_cluster["short_name"]:
        cluster_identifier = managed_cluster["short_name"]
    else:
        cluster_identifier = managed_cluster["integration_id"]

    grafana = grafanaapi.GrafanaApi()
    graphite = graphiteapi.GraphiteApi()

    hosts_panel = grafana.get_panel(
        "Hosts",
        row_title="At-a-glance",
        dashboard="cluster-dashboard")

    """
    :step:
      Send **GET** request to ``GRAPHITE/render?target=[target]&format=json``
      where [target] is part of uri obtained from previous GRAFANA call.
      There should be target for statuses of a hosts.
      Compare number of hosts from Graphite with value retrieved from
      ``workload_stop_nodes`` fixture.
    :result:
      JSON structure containing data related to hosts status is similar
      to values set by ``workload_stop_nodes`` fixture in given time.
    """
    # get graphite target pointing at data containing numbers of hosts
    targets = grafana.get_panel_chart_targets(hosts_panel, cluster_identifier)
    targets_used = (targets[0][0], targets[1][0], targets[2][0])
    targets_expected = ('nodes_count.total', 'nodes_count.up', 'nodes_count.down')
    for idx, target in enumerate(targets_used):
        pytest.check(
            target.endswith(targets_expected[idx]),
            "There is used target that ends with `{}`".format(
                targets_expected[idx]))
    # make sure that all data in graphite are saved
    time.sleep(3)
    # check value *Total* of hosts
    graphite.compare_data_mean(
        workload_stop_nodes["result"],
        (targets_used[0],),
        workload_stop_nodes["start"],
        workload_stop_nodes["end"],
        divergence=1,
        issue="https://bugzilla.redhat.com/show_bug.cgi?id=1687333")
    # check value *Up* of hosts
    graphite.compare_data_mean(
        0.0,
        (targets_used[1],),
        workload_stop_nodes["start"],
        workload_stop_nodes["end"],
        divergence=1,
        issue="https://bugzilla.redhat.com/show_bug.cgi?id=1687333")
    # check value *Down* of hosts
    graphite.compare_data_mean(
        workload_stop_nodes["result"],
        (targets_used[2],),
        workload_stop_nodes["start"],
        workload_stop_nodes["end"],
        divergence=1,
        issue="https://bugzilla.redhat.com/show_bug.cgi?id=1687333")
