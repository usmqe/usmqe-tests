"""
REST API test suite - Grafana dashboard host-dashboard
"""

import pytest
import time
from usmqe.api.grafanaapi import grafanaapi
from usmqe.api.graphiteapi import graphiteapi
from usmqe.usmqeconfig import UsmConfig


LOGGER = pytest.get_logger('host_dashboard', module=True)
CONF = UsmConfig()


@pytest.mark.testready
@pytest.mark.author("fbalak@redhat.com")
def test_host_dashboard_layout():
    """
    Check that layout of dashboard is according to specification:
    ``https://github.com/Tendrl/specifications/issues/222``
    """
    grafana = grafanaapi.GrafanaApi()

    """
    :step:
      Send **GET** request to:
      ``GRAFANA/dashboards/db/host-dashboard`` and get layout structure.
      Compare structure of panels and rows as defined in specification:
      ``https://github.com/Tendrl/specifications/issues/222``
    :result:
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
            'Top Bricks by Capacity Percent Utilized',
            'Top Bricks by Total Capacity',
            'Top Bricks by Capacity Utilized',
            'Disk Throughput',
            'Disk IOPS',
            'Disk IO Latency']}
    grafana.compare_structure(structure_defined, "host-dashboard")


@pytest.mark.testready
@pytest.mark.author("fbalak@redhat.com")
@pytest.mark.ansible_playbook_setup('test_setup.graphite_access.yml')
@pytest.mark.ansible_playbook_teardown('test_teardown.graphite_access.yml')
def test_cpu_utilization(
        ansible_playbook, workload_cpu_utilization, cluster_reuse):
    """
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

    """
    :step:
      Send **GET** request to ``GRAPHITE/render?target=[target]&format=json``
      where [target] is part of uri obtained from previous GRAFANA call.
      There should be target for CPU utilization of a host.
      Compare number of hosts from Graphite with value retrieved from
      ``workload_cpu_utilization`` fixture.
    :result:
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


@pytest.mark.testready
@pytest.mark.author("fbalak@redhat.com")
@pytest.mark.ansible_playbook_setup('test_setup.graphite_access.yml')
@pytest.mark.ansible_playbook_teardown('test_teardown.graphite_access.yml')
def test_memory_utilization(
        ansible_playbook, workload_memory_utilization, cluster_reuse):
    """
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

    """
    :step:
      Send **GET** request to ``GRAPHITE/render?target=[target]&format=json``
      where [target] is part of uri obtained from previous GRAFANA call.
      There should be target for memory utilization of a host.
      Compare number of hosts from Graphite with value retrieved from
      ``workload_memory_utilization`` fixture.
    :result:
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


@pytest.mark.author("fbalak@redhat.com")
@pytest.mark.ansible_playbook_setup('test_setup.graphite_access.yml')
@pytest.mark.ansible_playbook_teardown('test_teardown.graphite_access.yml')
def test_swap_free(
        ansible_playbook, workload_swap_utilization, cluster_reuse):
    """
    Check that Grafana panel *Swap Free* is showing correct values.
    """
    if cluster_reuse["short_name"]:
        cluster_identifier = cluster_reuse["short_name"]
    else:
        cluster_identifier = cluster_reuse["integration_id"]

    grafana = grafanaapi.GrafanaApi()
    graphite = graphiteapi.GraphiteApi()

    swap_panel = grafana.get_panel(
        "Swap Free",
        row_title="At-a-Glance",
        dashboard="host-dashboard")

    """
    :step:
      Send **GET** request to ``GRAPHITE/render?target=[target]&format=json``
      where [target] is part of uri obtained from previous GRAFANA call.
      There should be target for swap utilization of a host.
      Compare number of hosts from Graphite with value retrieved from
      ``workload_swap_utilization`` fixture.
    :result:
      JSON structure containing data related to swap utilization is similar
      to values set by ``workload_swap_utilization`` fixture in given time.
    """
    # get graphite target pointing at data containing number of host
    targets = grafana.get_panel_chart_targets(swap_panel, cluster_identifier)
    target_used = targets[0][0]
    target_expected = 'swap.percent-free'
    pytest.check(
        target_used.endswith(target_expected),
        "There is used target that ends with `{}`".format(target_expected))
    # make sure that all data in graphite are saved
    time.sleep(2)
    graphite.compare_data_mean(
        100 - int(workload_swap_utilization["result"]),
        (target_used,),
        workload_swap_utilization["start"],
        workload_swap_utilization["end"],
        divergence=15)


@pytest.mark.author("fbalak@redhat.com")
@pytest.mark.ansible_playbook_setup('test_setup.graphite_access.yml')
@pytest.mark.ansible_playbook_teardown('test_teardown.graphite_access.yml')
def test_swap_utilization(
        ansible_playbook, workload_swap_utilization, cluster_reuse):
    """
    Check that Grafana panel *Swap Utilization* is showing correct values.
    """
    if cluster_reuse["short_name"]:
        cluster_identifier = cluster_reuse["short_name"]
    else:
        cluster_identifier = cluster_reuse["integration_id"]

    grafana = grafanaapi.GrafanaApi()
    graphite = graphiteapi.GraphiteApi()

    swap_panel = grafana.get_panel(
        "Swap Utilization",
        row_title="At-a-Glance",
        dashboard="host-dashboard")

    """
    :step:
      Send **GET** request to ``GRAPHITE/render?target=[target]&format=json``
      where [target] is part of uri obtained from previous GRAFANA call.
      There should be target for swap utilization of a host.
      Compare number of hosts from Graphite with value retrieved from
      ``workload_swap_utilization`` fixture.
    :result:
      JSON structure containing data related to swap utilization is similar
      to values set by ``workload_swap_utilization`` fixture in given time.
    """
    # get graphite target pointing at data containing number of host
    targets = grafana.get_panel_chart_targets(swap_panel, cluster_identifier)
    target_used = targets[0][0]
    target_expected = 'swap.percent-used'
    pytest.check(
        target_used.endswith(target_expected),
        "There is used target that ends with `{}`".format(target_expected))
    # make sure that all data in graphite are saved
    time.sleep(2)
    graphite.compare_data_mean(
        workload_swap_utilization["result"],
        (target_used,),
        workload_swap_utilization["start"],
        workload_swap_utilization["end"],
        divergence=15)
