import pytest
from usmqe.gluster import gluster


LOGGER = pytest.get_logger('volume_test', module=True)


def test_volume_attributes(application, valid_session_credentials):
    clusters = application.collections.clusters.get_clusters()
    test_cluster = clusters[0]
    volumes = test_cluster.volumes.get_volumes()
    glv_cmd = gluster.GlusterVolume()
    g_volume_names = glv_cmd.get_volume_names()
    pytest.check(set([volume.volname for volume in volumes]) == set(g_volume_names))
    LOGGER.debug("UI volume names: {}".format([volume.volname for volume in volumes]))
    LOGGER.debug("Gluster command volume names: {}".format(g_volume_names))

    for volume in volumes:
        pytest.check(volume.volname.find("olume_") == 1)
        pytest.check(volume.running == "Yes")
        pytest.check(volume.rebalance == "Not Started")
        pytest.check(volume.alerts == "0")


def test_volume_profiling_switch(application):
    clusters = application.collections.clusters.get_clusters()
    test_cluster = clusters[0]
    volumes = test_cluster.volumes.get_volumes()
    pytest.check(volumes != [])
    for volume in volumes:
        glv_cmd = gluster.GlusterVolume(volume_name=volume.volname)
        pytest.check(volume.volname.find("olume_") == 1)
        volume.disable_profiling()
        pytest.check(not glv_cmd.is_profiling_enabled())
        pytest.check(volume.profiling == "Disabled")
        volume.enable_profiling()
        pytest.check(glv_cmd.is_profiling_enabled())
        pytest.check(volume.profiling == "Enabled")


'''
def test_host_dashboard(application):
    clusters = application.collections.clusters.get_clusters()
    test_cluster = clusters[0]
    hosts = test_cluster.hosts.get_hosts()
    test_host = hosts[3]
    test_host.check_dashboard()'''
