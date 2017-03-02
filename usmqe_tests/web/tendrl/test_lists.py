"""
Description: Simple tests for lists pages

Author: ltrilety
"""


import pytest

import usmqe.inventory
from usmqe.web.tendrl.mainpage.clusters.cluster_list.pages import ClustersMenu
from usmqe.web.tendrl.mainpage.hosts.pages import HostsMenu


def test_hosts_list(log_in, testcase_end):
    """
    very simple test which checks the list of hosts on Hosts page

    NOTE: a cluster must already exists in etcd
    """
    navMenuBar = log_in.init_object
    hosts_list = navMenuBar.open_hosts()
    inventory_hosts = usmqe.inventory.role2hosts('usm_nodes')
    pytest.check(
        len(hosts_list) == len(inventory_hosts),
        'There should be exactly {} hosts'.format(len(inventory_hosts)))
    HostsMenu(log_in.driver)
    for host in hosts_list:
        # the check is extra, it's not needed, there could be just pass
        pytest.check(host.is_present,
                     'Any host (line in Hosts list) should have some elements')
        host_name = host.name
        pytest.check(host_name in inventory_hosts,
                     'host {} present in the list'.format(host_name))
        del(inventory_hosts[inventory_hosts.index(host_name)])


@pytest.mark.parametrize("sds_name", ["gluster"])
def test_cluster_list(log_in, testcase_end, sds_name):
    """
    very simple test which checks the list of clusters on Clusters page

    NOTE: a 'gluster' cluster must already exists in etcd
    """
    navMenuBar = log_in.init_object
    clusters_list = navMenuBar.open_clusters()
    pytest.check(len(clusters_list) > 0, 'Cluster list should not be empty')
    ClustersMenu(log_in.driver)
    inventory_hosts = usmqe.inventory.role2hosts(sds_name)
    for cluster in clusters_list:
        # the check is extra, it's not needed, there could be just pass
        pytest.check(
            cluster.is_present,
            'Any cluster (line in Clusters list) should have some elements')
        pytest.check(
            int(cluster.hosts_nr) == len(inventory_hosts),
            'The hosts number should correspond to the number of {} hosts: {}'.
            format(sds_name, len(inventory_hosts)))
