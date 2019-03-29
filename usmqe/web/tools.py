# -*- coding: utf8 -*-
import pytest


LOGGER = pytest.get_logger('web_testing_tools', module=True)


def close_extra_windows(view):
    """
    Close all windows/tabs except for the very first one.
    """
    while len(view.browser.selenium.window_handles) > 1:
        view.browser.selenium.close()
        view.browser.selenium.switch_to.window(view.browser.selenium.window_handles[-1])


def bricks_displayed(view, bricks_count, part_id):
    """
    Return True if parent's bricks_count attribute equals "0"
    or the first brick's health is visible. Return False otherwise.
    column_number should be 0 for host bricks view and 1 for volume bricks view.
    """
    if bricks_count == "0":
        return True
    elif part_id is None:
        return len(view.bricks.row()[0].browser.elements(".//span[@uib-tooltip]")) == 1
    else:
        return len(view.volume_parts(part_id).bricks.row()[1].
                   browser.elements(".//span[@uib-tooltip]")) == 1


def choose_cluster(clusters_list, cluster_id, cluster_name):
    """
    Choose cluster with the correct identifier from clusters_list
    If the cluster has a name, use it as identifier, else use cluster_id
    """
    LOGGER.debug("Name provided: {}".format(cluster_name))
    if not cluster_name:
        identifier = cluster_id
    else:
        identifier = cluster_name
        LOGGER.debug("Cluster identified by name: {}".format(identifier))
    LOGGER.debug("Target cluster id: {}".format(cluster_id))
    for cluster in clusters_list:
        LOGGER.debug("Current cluster id: {}".format(cluster.cluster_id))
        LOGGER.debug("Current cluster name: {}".format(cluster.name))
        LOGGER.debug("Identifier: {}".format(identifier))
        if cluster.name == identifier:
            LOGGER.debug("Found cluster {}".format(cluster_id))
            cluster.cluster_id = cluster_id
            return cluster
