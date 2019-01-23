import pytest


def test_host_attributes(application):
    clusters = application.collections.clusters.get_clusters()
    test_cluster = clusters[0]
    hosts = test_cluster.hosts.get_hosts()
    pytest.check(len(hosts) == 6)
    for host in hosts:
        pytest.check(host.gluster_version == "3.4")
        pytest.check(host.managed == "Yes")
        pytest.check(host.role == "Gluster Peer")
        # brick count depends on volume type
        # pytest.check(host.bricks_count == "5")
        pytest.check(int(host.alerts) < 1000)
        pytest.check(host.cluster_name == test_cluster.name)


def test_host_bricks(application):
    clusters = application.collections.clusters.get_clusters()
    test_cluster = clusters[0]
    hosts = test_cluster.hosts.get_hosts()
    pytest.check(hosts != [])
    for host in hosts:
        bricks = host.bricks.get_bricks()
        pytest.check(bricks != [])
        pytest.check(len(bricks) == int(host.bricks_count))
        for brick in bricks:
            assert brick.brick_path.find('/mnt/brick') == 0
            pytest.check(brick.hostname == host.hostname)
            pytest.check(brick.volume_name.split('_')[4] == 'plus')
            pytest.check(brick.utilization.find('% U') > 0)
            pytest.check(brick.disk_device_path.split('/')[1] == 'dev')
            pytest.check(int(brick.port) > 1000)


'''
def test_host_dashboard(application):
    clusters = application.collections.clusters.get_clusters()
    test_cluster = clusters[0]
    hosts = test_cluster.hosts.get_hosts()
    test_host = hosts[3]
    test_host.check_dashboard()'''
