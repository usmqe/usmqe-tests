# -*- coding: utf8 -*-
"""
Tests related to functionality of usmqe.api.grafanaapi module
"""

import pytest
from usmqe.api.grafanaapi import grafanaapi


@pytest.mark.parametrize("grafana_target,expected_targets", [
    ("tendrl.names.$cluster_id.nodes.status",
        [["tendrl.names.cluster-id.nodes.status"]]),
    ("alias(keepLastValue(consolidateBy(maxSeries(tendrl.names." +
        "$cluster_id.nodes.brick_count.total), \"max\")),\"Total\")",
        [["tendrl.names.cluster-id.nodes.brick_count.total"]]),
    ("aliasSub(groupByNode(tendrl.names.$cluster_id.cpu.{percent-user," +
        "percent-system}, 6, 'sum'), 'percent-', ' ')",
        [[
            "tendrl.names.cluster-id.cpu.percent-user",
            "tendrl.names.cluster-id.cpu.percent-system"]])])
def test_get_targets(grafana_target, expected_targets):
    """
    For given module, return list of full module path names for all submodules
    recursively.
    """
    grafana = grafanaapi.GrafanaApi()

    panel = {
        "targets": [
            {"target": grafana_target}],
        "title": "Test panel"}
    targets = grafana.get_panel_chart_targets(panel, "cluster-id")
    assert targets == expected_targets
