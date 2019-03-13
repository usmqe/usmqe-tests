import pytest

from usmqe.gluster import gluster


LOGGER = pytest.get_logger('volume_test', module=True)


@pytest.mark.author("ebondare@redhat.com")
@pytest.mark.happypath
@pytest.mark.testready
def test_volume_attributes(application, valid_session_credentials, imported_cluster_reuse):
    """
    Test that all volumes are listed on cluster's Volumes page.
    Check all common volume attributes
    """
    """
    :step:
      Log in to Web UI and get the cluster identified by cluster_member.
      Get the list of its volumes.
    :result:
      Volume objects are initiated and their attributes are read from the page
    """
    clusters = application.collections.clusters.get_clusters()
    for cluster in clusters:
        if cluster.cluster_id == imported_cluster_reuse["cluster_id"]:
            test_cluster = cluster
    volumes = test_cluster.volumes.get_volumes()
    """
    :step:
      Get the list of volumes using Gluster command and check it's the same as in UI
    :result:
      The list of volumes in UI and in Gluster command are equal
    """
    glv_cmd = gluster.GlusterVolume()
    g_volume_names = glv_cmd.get_volume_names()
    pytest.check(set([volume.volname for volume in volumes]) == set(g_volume_names))
    LOGGER.debug("UI volume names: {}".format([volume.volname for volume in volumes]))
    LOGGER.debug("Gluster command volume names: {}".format(g_volume_names))
    """
    :step:
      Check common volume attributes
    :result:
      Common volume attributes have expected values
    """
    for volume in volumes:
        pytest.check(volume.volname.find("olume_") == 1)
        pytest.check(volume.running == "Yes")
        pytest.check(volume.rebalance == "Not Started")
        pytest.check(int(volume.alerts) >= 0)


@pytest.mark.testready
@pytest.mark.author("ebondare@redhat.com")
@pytest.mark.happypath
def test_volume_dashboard(application, imported_cluster_reuse):
    """
    Check that dashboard button opens correct volume dashboard with correct data on bricks
    """
    """
    :step:
      Log in to Web UI and get the cluster identified by cluster_member.
      Get the list of its volumes.
    :result:
      Volume objects are initiated and their attributes are read from the page.
    """
    clusters = application.collections.clusters.get_clusters()
    for cluster in clusters:
        if cluster.cluster_id == imported_cluster_reuse["cluster_id"]:
            test_cluster = cluster
    volumes = test_cluster.volumes.get_volumes()
    """
    :step:
      For each volume in the volume list, click its Dashboard button and check
      cluster name, volume name, bricks count and volume health
    :result:
      Volume dashboard shows the correct information
    """
    for volume in volumes:
        dashboard_values = volume.get_values_from_dashboard()
        LOGGER.debug("Cluster name in grafana: {}".format(dashboard_values["cluster_name"]))
        LOGGER.debug("Cluster name in main UI: {}".format(volume.cluster_name))
        pytest.check(dashboard_values["cluster_name"] == volume.cluster_name)
        LOGGER.debug("Volume name in grafana: {}".format(dashboard_values["volume_name"]))
        LOGGER.debug("Volume name in main UI: {}".format(volume.volname))
        pytest.check(dashboard_values["volume_name"] == volume.volname)
        LOGGER.debug("Bricks count in grafana: {}".format(dashboard_values["brick_count"]))
        LOGGER.debug("Bricks count in main UI: {}".format(volume.bricks_count))
        pytest.check(dashboard_values["brick_count"] == volume.bricks_count)
        LOGGER.debug("Volume health in grafana: {}".format(dashboard_values["volume_health"]))
        LOGGER.debug("Volume health in main UI: {}".format(volume.health))
        pytest.check(dashboard_values["volume_health"] == volume.health)


@pytest.mark.author("ebondare@redhat.com")
@pytest.mark.happypath
@pytest.mark.testready
def test_volume_profiling_switch(application, imported_cluster_reuse):
    """
    Test disabling and enabling volume profiling in UI
    """
    """
    :step:
      Log in to Web UI and get the cluster identified by cluster_member.
      Get the list of its volumes.
    :result:
      Volume objects are initiated and their attributes are read from the page.
    """
    clusters = application.collections.clusters.get_clusters()
    for cluster in clusters:
        if cluster.cluster_id == imported_cluster_reuse["cluster_id"]:
            test_cluster = cluster
    volumes = test_cluster.volumes.get_volumes()
    for volume in volumes:
        """
        :step:
          For each volume in the volume list, disable profiling and check its profiling status
          both in UI and using Gluster command.
        :result:
          Volume profiling is disabled.
        """
        glv_cmd = gluster.GlusterVolume(volume_name=volume.volname)
        volume.disable_profiling()
        pytest.check(not glv_cmd.is_profiling_enabled())
        pytest.check(volume.profiling == "Disabled")
        """
        :step:
          For each volume in the volume list, enable profiling and check its profiling status
          both in UI and using Gluster command.
        :result:
          Volume profiling is enabled.
        """
        volume.enable_profiling()
        pytest.check(glv_cmd.is_profiling_enabled())
        pytest.check(volume.profiling == "Enabled")


@pytest.mark.author("ebondare@redhat.com")
@pytest.mark.happypath
@pytest.mark.testready
def test_volume_parts(application, imported_cluster_reuse):
    """
    Test replica set/subvolume names and expanding/collapsing.
    """
    """
    :step:
      Log in to Web UI and get the cluster identified by cluster_member.
      Get the list of its volumes.
    :result:
      Volume objects are initiated and their attributes are read from the page.
    """
    clusters = application.collections.clusters.get_clusters()
    for cluster in clusters:
        if cluster.cluster_id == imported_cluster_reuse["cluster_id"]:
            test_cluster = cluster
    volumes = test_cluster.volumes.get_volumes()
    pytest.check(volumes != [])
    for volume in volumes:
        """
        :step:
          For each volume in the volume list, get the list of its subvolumes/replica sets.
          Check it's not empty.
        :result:
          Subvolume/replica set objects are initiated and their attributes are read from the page.
        """
        volume_parts = volume.parts.get_parts()
        pytest.check(volume_parts != [])
        """
        :step:
          Check all subvolumes/replica sets are collapsed. Expand them using Expand All option.
        :result:
          All subvolumes/replica sets are expanded.
        """
        for part in volume_parts:
            pytest.check(not part.is_expanded)
        volume.parts.expand_all()
        for part in volume_parts:
            pytest.check(part.is_expanded)
        """
        :step:
          Collapse all subvolumes/replica sets using Collapse All option.
        :result:
          All subvolumes/replica sets are collapsed.
        """
        volume.parts.collapse_all()
        for part in volume_parts:
            pytest.check(not part.is_expanded)
        """
        :step:
          Check if volume part should be called Subvolume or Replica set depending on volume type.
        :result:
          Appropriate part name is chosen.
        """
        if volume.volname.split("_")[2] in {"arbiter", "distrep"}:
            part_name = "Replica Set "
        elif volume.volname.split("_")[2] == "disperse":
            part_name = "Subvolume "
        else:
            pytest.check(False)
            LOGGER.debug("Unexpected volume type")
            part_name = ""
        for part in volume_parts:
            """
            :step:
              For each subvolume/replica set check its name is as expected.
            :result:
              All subvolume/replica set names are OK.
            """
            pytest.check(part.part_name == part_name + str(int(part.part_id) - 1))
            LOGGER.debug("Expected part name: {}".format(part_name + str(int(part.part_id) - 1)))
            LOGGER.debug("Real part name: {}".format(part.part_name))
            """
            :step:
              Expand each subvolume/replica set individually. Check it's expanded.
            :result:
              Subvolume/replica set is expanded.
            """
            part.expand()
            pytest.check(part.is_expanded)
            """
            :step:
              Collapse each subvolume/replica set individually. Check it's collapsed.
            :result:
              Subvolume/replica set is collapsed.
            """
            part.collapse()
            pytest.check(not part.is_expanded)


@pytest.mark.author("ebondare@redhat.com")
@pytest.mark.happypath
@pytest.mark.testready
def test_volume_bricks(application, imported_cluster_reuse):
    """
    Test volume brick attributes and their division into replica sets/subvolumes.
    """
    """
    :step:
      Log in to Web UI and get the cluster identified by cluster_member.
      Get the list of its volumes.
    :result:
      Volume objects are initiated and their attributes are read from the page.
    """
    clusters = application.collections.clusters.get_clusters()
    for cluster in clusters:
        if cluster.cluster_id == imported_cluster_reuse["cluster_id"]:
            test_cluster = cluster
    volumes = test_cluster.volumes.get_volumes()
    pytest.check(volumes != [])
    for volume in volumes:
        """
        :step:
          For each volume calculate the expected subvolume/replica set size
          from the volume name depending on volume type.
        :result:
          Subvolume/replica set size is calculated.
        """
        if volume.volname.split("_")[2] in {"arbiter", "disperse"}:
            part_size = int(volume.volname.split("_")[3]) + \
                        int(volume.volname.split("_")[5].split('x')[0])
        elif volume.volname.split("_")[2] == "distrep":
            part_size = int(volume.volname.split("_")[3].split('x')[1])
        else:
            pytest.check(False)
            LOGGER.debug("Unexpected volume type")
            part_size = 0
        """
        :step:
          For each volume part get its bricks.
          Check that actual brick count per subvolume/replica set is as expected.
        :result:
          Each subvolume/replica set has the expected number of bricks.
        """
        volume_parts = volume.parts.get_parts()
        pytest.check(volume_parts != [])
        all_bricks = []
        for part in volume_parts:
            bricks = part.bricks.get_bricks()
            pytest.check(len(bricks) == part_size)
            for brick in bricks:
                """
                :step:
                  Check each brick's attributes.
                :result:
                  All brick's attributes are as expected.
                """
                pytest.check(brick.brick_path.find('/mnt/brick') == 0)
                pytest.check(brick.utilization.find('% U') > 0)
                pytest.check(brick.disk_device_path.split('/')[1] == 'dev')
                pytest.check(int(brick.port) > 1000)
            all_bricks = all_bricks + bricks
        """
        :step:
          Check that the list of all bricks of the volume in UI is the same as the result
          of gluster volume info command.
        :result:
          The list of all volume's bricks in the UI is correct.
        """
        glv_cmd = gluster.GlusterVolume(volume_name=volume.volname)
        glv_cmd.info()
        LOGGER.debug("Gluster bricks: {}".format(glv_cmd.bricks))
        ui_brick_names = [b.hostname + ":" + b.brick_path for b in all_bricks]
        LOGGER.debug("UI bricks: {}".format(ui_brick_names))
        pytest.check(glv_cmd.bricks == ui_brick_names)


@pytest.mark.author("ebondare@redhat.com")
@pytest.mark.happypath
@pytest.mark.testready
def test_volume_brick_dashboards(application, imported_cluster_reuse):
    """
    Test Dashboard button of each brick of each volume
    """
    """
    :step:
      Log in to Web UI and get the cluster identified by cluster_member.
      Get the list of its volumes.
    :result:
      Volume objects are initiated and their attributes are read from the page
    """
    clusters = application.collections.clusters.get_clusters()
    for cluster in clusters:
        if cluster.cluster_id == imported_cluster_reuse["cluster_id"]:
            test_cluster = cluster
    volumes = test_cluster.volumes.get_volumes()
    """
    :step:
      For each volume, get the list of its subvolumes/replica sets.
      For each subvolume/replica set, get the list of its bricks.
      For each brick, click its Dashboard button.
      Check that the correct Grafana dashboard appears
      and that it shows expected value of brick status.
    :result:
      Grafana dashboard is opened, checked for its values and closed.
      Status check fails due to https://bugzilla.redhat.com/show_bug.cgi?id=1668900
    """
    for volume in volumes:
        volume_parts = volume.parts.get_parts()
        pytest.check(volume_parts != [])
        for part in volume_parts:
            bricks = part.bricks.get_bricks()
            for brick in bricks:
                dashboard_values = brick.get_values_from_dashboard()
                LOGGER.debug("Cluster name in grafana: {}".format(dashboard_values["cluster_name"]))
                LOGGER.debug("Cluster name in main UI: {}".format(brick.cluster_name))
                pytest.check(dashboard_values["cluster_name"] == brick.cluster_name)
                pytest.check(dashboard_values["host_name"] == brick.hostname.replace(".", "_"))
                LOGGER.debug("Hostname in grafana: {}".format(dashboard_values["host_name"]))
                LOGGER.debug("Hostname in main UI "
                             "after dot replacement: '{}'".format(brick.hostname.replace(".", "_")))
                pytest.check(dashboard_values["brick_path"] == brick.brick_path.replace("/", ":"))
                LOGGER.debug("Brick path in grafana: {}".format(dashboard_values["brick_path"]))
                LOGGER.debug("Brick path in main UI after slash "
                             "replacement: {}".format(brick.brick_path.replace("/", ":")))
                pytest.check(dashboard_values["brick_status"] == brick.status)
                assert brick.status != "None" and brick.status is not None
                LOGGER.debug("Status in grafana: '{}'".format(dashboard_values["brick_status"]))
                LOGGER.debug("Status in main UI: '{}'".format(brick.status))
