import pytest
from usmqe.gluster import gluster


LOGGER = pytest.get_logger('volume_test', module=True)


@pytest.mark.author("ebondare@redhat.com")
@pytest.mark.happypath
@pytest.mark.testready
def test_volume_attributes(application, valid_session_credentials):
    """
    Test that all volumes are listed on cluster's Volumes page.
    Check all common volume attributes
    """
    """
    :step:
      Log in to Web UI and get the first cluster from the cluster list.
      Get the list of its volumes.
    :result:
      Volume objects are initiated and their attributes are read from the page
    """
    clusters = application.collections.clusters.get_clusters()
    test_cluster = clusters[0]
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
        pytest.check(volume.alerts == "0")


@pytest.mark.testready
@pytest.mark.author("ebondare@redhat.com")
@pytest.mark.happypath
def test_volume_dashboard(application):
    """
    Check that dashboard button opens correct volume dashboard with correct data on bricks
    """
    """
    :step:
      Log in to Web UI and get the first cluster from the cluster list.
      Get the list of its volumes.
    :result:
      Volume objects are initiated and their attributes are read from the page.
    """
    clusters = application.collections.clusters.get_clusters()
    test_cluster = clusters[0]
    volumes = test_cluster.volumes.get_volumes()
    """
    :step:
      For each volume in the volume list, click its Dashboard button and check
      cluster name, volume name and bricks count
    :result:
      Volume dashboard shows the correct information
    """
    for volume in volumes:
        volume.check_dashboard()


@pytest.mark.author("ebondare@redhat.com")
@pytest.mark.happypath
@pytest.mark.testready
def test_volume_profiling_switch(application):
    """
    Test disabling and enabling volume profiling in UI
    """
    """
    :step:
      Log in to Web UI and get the first cluster from the cluster list.
      Get the list of its volumes.
    :result:
      Volume objects are initiated and their attributes are read from the page.
    """
    clusters = application.collections.clusters.get_clusters()
    test_cluster = clusters[0]
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
