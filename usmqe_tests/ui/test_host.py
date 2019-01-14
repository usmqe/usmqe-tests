import pytest


def test_host_attributes(application):
    clusters = application.collections.clusters.get_clusters()
    test_cluster = clusters[0]
    hosts = test_cluster.hosts.get_hosts()
    for host in hosts:
        pytest.check(host.gluster_version == "3.4")
        pytest.check(host.managed == "Yes")
        pytest.check(host.role == "Gluster Peer")
        # brick count depends on volume type
        # pytest.check(host.bricks == "5")
        pytest.check(host.alerts == "0")


def test_host_dashboard(application):
    clusters = application.collections.clusters.get_clusters()
    test_cluster = clusters[0]
    hosts = test_cluster.hosts.get_hosts()
    test_host = hosts[3]
    test_host.check_dashboard()
