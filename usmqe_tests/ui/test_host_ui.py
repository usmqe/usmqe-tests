import pytest

LOGGER = pytest.get_logger('hosts', module=True)


@pytest.mark.testready
@pytest.mark.author("ebondare@redhat.com")
@pytest.mark.happypath
def test_host_attributes(application, imported_cluster_reuse):
    """
    Test that all hosts are listed on cluster's Hosts page.
    Check all common host attributes
    """
    """
    :step:
      Log in to Web UI and get the cluster identified by cluster_member.
      Get the list of its hosts.
    :result:
      Host objects are initiated and their attributes are read from the page
    """
    clusters = application.collections.clusters.get_clusters()
    for cluster in clusters:
        if cluster.cluster_id == imported_cluster_reuse["cluster_id"]:
            test_cluster = cluster
    hosts = test_cluster.hosts.get_hosts()
    """
    :step:
       Compare the set of hostnames in UI to set of nodes in API
    :result:
       UI shows the correct set of hostnames.
    """
    ui_hostnames = [host.hostname for host in hosts]
    api_hostnames = [node["fqdn"] for node in imported_cluster_reuse["nodes"]]
    LOGGER.debug("API cluster nodes: {}".format(api_hostnames))
    LOGGER.debug("UI cluster nodes: {}".format(ui_hostnames))
    pytest.check(set(ui_hostnames) == set(api_hostnames))
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
        for node in imported_cluster_reuse["nodes"]:
            if node["fqdn"] == host.hostname:
                pytest.check(node["status"] == host.health)


@pytest.mark.testready
@pytest.mark.author("ebondare@redhat.com")
@pytest.mark.happypath
def test_host_bricks(application, imported_cluster_reuse):
    """
    Test that all hosts are listed on cluster's Hosts page.
    Check all common brick attributes
    """
    """
    :step:
      Log in to Web UI and get the cluster identified by cluster_member.
      Get the list of its hosts.
    :result:
      Host objects are initiated and their attributes are read from the page
    """
    clusters = application.collections.clusters.get_clusters()
    for cluster in clusters:
        if cluster.cluster_id == imported_cluster_reuse["cluster_id"]:
            test_cluster = cluster
    volume_bricks = []
    for volume in test_cluster.volumes.get_volumes():
        for part in volume.parts.get_parts():
            volume_bricks += part.bricks.get_bricks()
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
        """
        :step:
          Check that bricks on the host's Brick details page are the same as
          all this host's bricks on all volume brick details pages combined together.
        :result:
          Volume details and host details show the same set of bricks
        """
        bricks_from_volumes = [brick.brick_path for brick in volume_bricks
                               if brick.hostname == host.hostname]
        bricks_from_host = [brick.brick_path for brick in bricks]
        LOGGER.debug("Host's bricks from volumes: {}".format(bricks_from_volumes))
        LOGGER.debug("Host's bricks: {}".format(bricks_from_host))
        pytest.check(set(bricks_from_host) == set(bricks_from_volumes))
        for brick in bricks:
            """
            :step:
              For all bricks of each host, check common host attributes
            :result:
              Common brick attributes have expected values
            """
            pytest.check(brick.brick_path.find('/mnt/brick') == 0)
            pytest.check(brick.hostname == host.hostname)
            pytest.check(brick.volume_name.split('_')[0] == 'volume')
            pytest.check(brick.utilization.find('% U') > 0)
            pytest.check(brick.disk_device_path.split('/')[1] == 'dev')
            pytest.check(int(brick.port) > 1000)


@pytest.mark.testready
@pytest.mark.author("ebondare@redhat.com")
@pytest.mark.happypath
def test_host_dashboard(application, imported_cluster_reuse):
    """
    Test each host's Dashboard button
    """
    """
    :step:
      Log in to Web UI and get the cluster identified by cluster_member.
      Get the list of its hosts.
    :result:
      Host objects are initiated and their attributes are read from the page
    """
    clusters = application.collections.clusters.get_clusters()
    for cluster in clusters:
        if cluster.cluster_id == imported_cluster_reuse["cluster_id"]:
            test_cluster = cluster
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
        dashboard_values = host.get_values_from_dashboard()
        pytest.check(dashboard_values["cluster_name"] == host.cluster_name)
        LOGGER.debug("Cluster name in grafana: {}".format(dashboard_values["cluster_name"]))
        LOGGER.debug("Cluster name in main UI: {}".format(host.cluster_name))
        pytest.check(dashboard_values["host_name"] == host.hostname.replace(".", "_"))
        LOGGER.debug("Hostname in grafana: {}".format(dashboard_values["host_name"]))
        LOGGER.debug("Hostname in main UI "
                     "after dot replacement: '{}'".format(host.hostname.replace(".", "_")))
        pytest.check(dashboard_values["brick_count"] == host.bricks_count)
        LOGGER.debug("Brick count in grafana: {}".format(dashboard_values["brick_count"]))
        LOGGER.debug("Brick count in main UI: {}".format(host.bricks_count))
        pytest.check(dashboard_values["host_health"] == host.health.lower())
        LOGGER.debug("Host health in grafana: '{}'".format(dashboard_values["host_health"]))
        LOGGER.debug("Host health in main UI: '{}'".format(host.health.lower()))


def test_brick_dashboard(application, imported_cluster_reuse):
    """
    Test Dashboard button of each brick of each host
    """
    """
    :step:
      Log in to Web UI and get the cluster identified by cluster_member.
      Get the list of its hosts.
    :result:
      Host objects are initiated and their attributes are read from the page
    """
    clusters = application.collections.clusters.get_clusters()
    for cluster in clusters:
        if cluster.cluster_id == imported_cluster_reuse["cluster_id"]:
            test_cluster = cluster
    hosts = test_cluster.hosts.get_hosts()
    """
    :step:
      For each host, get the list of its bricks.
      For each brick, click its Dashboard button.
      Check that the correct Grafana dashboard appears
      and that it shows expected value of brick status.
    :result:
      Grafana dashboard is opened, checked for its values and closed.
      Status check fails due to https://bugzilla.redhat.com/show_bug.cgi?id=1668900
    """
    for host in hosts:
        bricks = host.bricks.get_bricks()
        for brick in bricks:
            dashboard_values = brick.get_values_from_dashboard()
            brick_status = brick.status
            LOGGER.debug("Cluster name in grafana: {}".format(dashboard_values["cluster_name"]))
            LOGGER.debug("Cluster name in main UI: {}".format(brick.cluster_name))
            pytest.check(dashboard_values["cluster_name"] == brick.cluster_name)
            pytest.check(dashboard_values["host_name"] == brick.hostname.replace(".", "_"))
            LOGGER.debug("Hostname in main UI "
                         "after dot replacement: '{}'".format(brick.hostname.replace(".", "_")))
            pytest.check(dashboard_values["brick_path"] == brick.brick_path.replace("/", ":"))
            LOGGER.debug("Brick path in grafana: {}".format(dashboard_values["brick_path"]))
            LOGGER.debug("Brick path in main UI "
                         "after slash replacement: {}".format(brick.brick_path.replace("/", ":")))
            pytest.check(dashboard_values["brick_status"] == brick_status)
            LOGGER.debug("Brick status in grafana: '{}'".format(dashboard_values["brick_status"]))
            LOGGER.debug("Brick status in main UI: '{}'".format(brick_status))
