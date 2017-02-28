"""
Description: Simple log in test

Author: ltrilety
"""


import pytest

from usmqe.web.tendrl.mainpage.clusters.cluster_list.pages import ClustersMenu
from usmqe.web.tendrl.mainpage.hosts.pages import HostsMenu


def test_hosts_list(log_in, testcase_end):
    """
    very simple test which checks the list of hosts on Hosts page

    NOTE: a cluster must already exists in etcd
    """
    navMenuBar = log_in.init_object
    hosts_list = navMenuBar.open_hosts()
    pytest.check(len(hosts_list) > 0, 'Host list should not be empty')
    HostsMenu(log_in.driver)
    for host in hosts_list:
        # the check is extra, it's not needed, there could be just pass
        pytest.check(host.is_present,
                     'Any host (line in Hosts list) should have some elements')


def test_cluster_list(log_in, testcase_end):
    """
    very simple test which checks the list of clusters on Clusters page

    NOTE: a cluster must already exists in etcd
    """
    navMenuBar = log_in.init_object
    clusters_list = navMenuBar.open_clusters()
    pytest.check(len(clusters_list) > 0, 'Cluster list should not be empty')
    ClustersMenu(log_in.driver)
    for cluster in clusters_list:
        # the check is extra, it's not needed, there could be just pass
        pytest.check(
            cluster.is_present,
            'Any cluster (line in Clusters list) should have some elements')
