"""
Description: Simple tests for lists pages

Author: ltrilety
"""


import pytest

import usmqe.inventory
from usmqe.web.tendrl.mainpage.clusters.cluster_list.pages import ClustersMenu
from usmqe.web.tendrl.details.hosts.pages import HostsMenu


def test_hosts_list(valid_credentials):
    """
    very simple test which checks the list of hosts on Hosts page

    NOTE: a cluster must already exists in etcd
    """
    navMenuBar = valid_credentials.init_object
    hosts_list = navMenuBar.open_hosts()
    inventory_hosts = usmqe.inventory.role2hosts('usm_nodes')
    inventory_hosts.append(usmqe.inventory.role2hosts('usm_server')[0])
    gluster_hosts = usmqe.inventory.role2hosts(pytest.config.getini("usm_gluster_role")) or []
    ceph_mon_hosts = usmqe.inventory.role2hosts('ceph_mon') or []
    ceph_osd_hosts = usmqe.inventory.role2hosts('ceph_osd') or []
    # there should be all storage nodes plus tendrl machine in the list
    pytest.check(
        len(hosts_list) == len(inventory_hosts),
        'There should be exactly {} hosts'.format(len(inventory_hosts)))
    HostsMenu(valid_credentials.driver)
    for host in hosts_list:
        # the host.is_present check is extra, it's not needed
        pytest.check(host.is_present,
                     'Any host (line in Hosts list) should have some elements')
        host_name = host.name
        host_role = host.role
        pytest.check(host_name in inventory_hosts,
                     'host {} present in the list'.format(host_name))
        del(inventory_hosts[inventory_hosts.index(host_name)])
        if host_name in gluster_hosts:
            pytest.check(host_role == 'Peer',
                         "Gluster host should have a 'Peer' role"
                         ", it has '{}'".format(host_role))
        elif host_name in ceph_osd_hosts:
            pytest.check('OSD Host' in host_role,
                         "host should have OSD role"
                         ", it has '{}'".format(host_role))
        elif host_name in ceph_mon_hosts:
            pytest.check('Monitor' in host_role,
                         "host should have Monitor role"
                         ", it has '{}'".format(host_role))
    # TODO check other fields - cpu, memory etc.
    #       or maybe create a new test for that


@pytest.mark.parametrize("sds_name", ["gluster"])
def test_cluster_list(valid_credentials, sds_name):
    """
    very simple test which checks the list of clusters on Clusters page

    NOTE: a 'gluster' cluster must already exists in etcd
    """
    navMenuBar = valid_credentials.init_object
    clusters_list = navMenuBar.open_clusters()
    pytest.check(len(clusters_list) > 0, 'Cluster list should not be empty')
    ClustersMenu(valid_credentials.driver)
    if sds_name == 'ceph':
        inventory_hosts = usmqe.inventory.role2hosts('ceph_mon')
        inventory_hosts.extend(usmqe.inventory.role2hosts('ceph_osd'))
        # remove duplicates
        inventory_hosts = list(set(inventory_hosts))
    else:
        inventory_hosts = usmqe.inventory.role2hosts(sds_name)
    for cluster in clusters_list:
        # the cluster.is_present check is extra, it's not needed
        pytest.check(
            cluster.is_present,
            'Any cluster (line in Clusters list) should have some elements')
        pytest.check(
            int(cluster.hosts_nr) == len(inventory_hosts),
            'The hosts number should correspond to the number of {} hosts: {}'.
            format(sds_name, len(inventory_hosts)))
