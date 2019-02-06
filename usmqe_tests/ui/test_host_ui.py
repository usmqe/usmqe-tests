import pytest


@pytest.mark.testready
@pytest.mark.author("ebondare@redhat.com")
@pytest.mark.happypath
def test_host_attributes(application):
    """
    Test that all hosts are listed on cluster's Hosts page.
    Check all common host attributes
    """
    """
    :step:
      Log in to Web UI and get the first cluster from the cluster list.
      Get the list of its hosts.
    :result:
      Host objects are initiated and their attributes are read from the page
    """
    clusters = application.collections.clusters.get_clusters()
    test_cluster = clusters[0]
    hosts = test_cluster.hosts.get_hosts()
    pytest.check(len(hosts) == 6)
    """
    :step:
      Check common host attributes
    :result:
      Common host attributes have expected values
    """
    for host in hosts:
        pytest.check(host.gluster_version == "3.4")
        pytest.check(host.managed == "Yes")
        pytest.check(host.role == "Gluster Peer")
        pytest.check(int(host.alerts) < 1000)
        pytest.check(host.cluster_name == test_cluster.name)


@pytest.mark.testready
@pytest.mark.author("ebondare@redhat.com")
@pytest.mark.happypath
def test_host_bricks(application):
    """
    Test that all hosts are listed on cluster's Hosts page.
    Check all common host attributes
    """
    """
    :step:
      Log in to Web UI and get the first cluster from the cluster list.
      Get the list of its hosts.
    :result:
      Host objects are initiated and their attributes are read from the page
    """
    clusters = application.collections.clusters.get_clusters()
    test_cluster = clusters[0]
    hosts = test_cluster.hosts.get_hosts()
    pytest.check(hosts != [])
    for host in hosts:
        """
        :step:
          For each host, get the list of its bricks.
          Check that it has the correct number of bricks
        :result:
          Brick objects are initiated and their attributes are read from the page
        """
        bricks = host.bricks.get_bricks()
        pytest.check(len(bricks) == int(host.bricks_count))
        for brick in bricks:
            """
            :step:
              For all bricks of each host, check common host attributes
            :result:
              Common brick attributes have expected values
            """
            assert brick.brick_path.find('/mnt/brick') == 0
            pytest.check(brick.hostname == host.hostname)
            pytest.check(brick.volume_name.split('_')[4] == 'plus')
            pytest.check(brick.utilization.find('% U') > 0)
            pytest.check(brick.disk_device_path.split('/')[1] == 'dev')
            pytest.check(int(brick.port) > 1000)


@pytest.mark.testready
@pytest.mark.author("ebondare@redhat.com")
@pytest.mark.happypath
def test_host_dashboard(application):
    """
    Test each host's Dashboard button
    """
    """
    :step:
      Log in to Web UI and get the first cluster from the cluster list.
      Get the list of its hosts.
    :result:
      Host objects are initiated and their attributes are read from the page
    """

    clusters = application.collections.clusters.get_clusters()
    test_cluster = clusters[0]
    hosts = test_cluster.hosts.get_hosts()
    """
    :step:
      For each host, click its Dashboard button.
      Check that the correct Grafana dashboard appears
      and that it shows expected values of host health and brick count.
    :result:
      Grafana dashboard is opened, checked for its values and closed.
    """
    for host in hosts:
        host.check_dashboard()
