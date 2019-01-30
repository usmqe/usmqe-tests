import pytest
# from usmqe.base.application.implementations.web_ui import ViaWebUI
# LOGGER = pytest.get_logger('ui_user_testing', module=True)
# import time

from usmqe.api.tendrlapi import glusterapi
from usmqe.gluster import gluster


@pytest.mark.author("ebondare@redhat.com")
@pytest.mark.happypath
@pytest.mark.testready
def test_cluster_import(application, valid_session_credentials):
    """
    Check that Import button really imports the cluster
    """
    """
    :step:
      Log in to Web UI and get the first cluster from the cluster list.
      Check that it's not imported yet.
    :result:
      Cluster is in the correct state to start import
    """
    clusters = application.collections.clusters.get_clusters()
    test_cluster = clusters[0]
    pytest.check(test_cluster.managed == "No")
    """
    :step:
      Get the cluster's details via API. Check that API shows the same state
    :result:
      Cluster state in API is the same as in Web UI
    """
    tendrl_api = glusterapi.TendrlApiGluster(auth=valid_session_credentials)
    api_cluster = tendrl_api.get_cluster(test_cluster.name)
    pytest.check(
        api_cluster["is_managed"] == "no",
        "is_managed: {}\nThere should be ``no``.".format(api_cluster["is_managed"]))
    """
    :step:
      Import the cluster in Web UI and check its state has changed in both Web UI and API
    :result:
      Cluster is imported
    """
    test_cluster.cluster_import()
    api_cluster = tendrl_api.get_cluster(test_cluster.name)
    pytest.check(
        api_cluster["is_managed"] == "yes",
        "is_managed: {}\nThere should be ``yes``.".format(api_cluster["is_managed"]))


@pytest.mark.author("ebondare@redhat.com")
@pytest.mark.happypath
@pytest.mark.testready
def test_cluster_disable_profiling(application):
    """
    Disable cluster profiling in Web UI
    """
    """
    :step:
      Log in to Web UI and get the first cluster from the cluster list.
      Check that its profiling is enabled
    :result:
      Cluster is in the correct state to disable profiling
    """
    clusters = application.collections.clusters.get_clusters()
    test_cluster = clusters[0]
    gluster_cluster = gluster.GlusterVolume()
    pytest.check(gluster_cluster.get_clusterwide_profiling() == "enabled")
    """
    :step:
      Disable profiling in Web UI and check its state has changed in both Web UI and API
    :result:
      Cluster profiling has been disabled
    """
    test_cluster.disable_profiling()
    pytest.check(gluster_cluster.get_clusterwide_profiling() == "disabled")


@pytest.mark.author("ebondare@redhat.com")
@pytest.mark.happypath
@pytest.mark.testready
def test_cluster_enable_profiling(application):
    """
    Enable cluster profiling in Web UI
    """
    """
    :step:
      Log in to Web UI and get the first cluster from the cluster list.
      Check that its profiling is disabled
    :result:
      Cluster is in the correct state to enable profiling
    """
    clusters = application.collections.clusters.get_clusters()
    test_cluster = clusters[0]
    gluster_cluster = gluster.GlusterVolume()
    pytest.check(gluster_cluster.get_clusterwide_profiling() == "disabled")
    """
    :step:
      Enable profiling in Web UI and check its state has changed in both Web UI and API
    :result:
      Cluster profiling has been enabled
    """
    test_cluster.enable_profiling()
    pytest.check(gluster_cluster.get_clusterwide_profiling() == "enabled")


@pytest.mark.testready
@pytest.mark.author("ebondare@redhat.com")
@pytest.mark.happypath
def test_cluster_dashboard(application):
    """
    Check that dashboard button opens cluster dashboard with correct data on hosts and volumes
    """
    """
    :step:
      Log in to Web UI and get the first cluster from the cluster list.
      Click its Dashboard button and check cluster name, hosts and volumes count on the dashboard.
    :result:
      Cluster dashboard shows the correct information
    """
    clusters = application.collections.clusters.get_clusters()
    test_cluster = clusters[0]
    test_cluster.check_dashboard()


@pytest.mark.author("ebondare@redhat.com")
@pytest.mark.happypath
@pytest.mark.testready
def test_cluster_unmanage(application, valid_session_credentials):
    """
    Unmanage cluster in Web UI
    """
    """
    :step:
      Log in to Web UI and get the first cluster from the cluster list.
      Check that it's imported.
    :result:
      Cluster is in the correct state to start unmanage
    """
    clusters = application.collections.clusters.get_clusters()
    test_cluster = clusters[0]
    tendrl_api = glusterapi.TendrlApiGluster(auth=valid_session_credentials)
    api_cluster = tendrl_api.get_cluster(test_cluster.name)
    pytest.check(
        api_cluster["is_managed"] == "yes",
        "is_managed: {}\nThere should be ``yes``.".format(api_cluster["is_managed"]))
    """
    :step:
      Unmanage the cluster in Web UI and check its state has changed in both Web UI and API
    :result:
      Cluster is unmanaged
    """
    test_cluster.unmanage()
    api_cluster = tendrl_api.get_cluster(test_cluster.name)
    pytest.check(
        api_cluster["is_managed"] == "no",
        "is_managed: {}\nThere should be ``no``.".format(api_cluster["is_managed"]))


@pytest.mark.author("ebondare@redhat.com")
@pytest.mark.happypath
@pytest.mark.testready
def test_cluster_import_naming(application):
    """
    Import cluster and give it a custom name. Then unmanage it.
    """
    """
    :step:
      Log in to Web UI and import the first cluster from the clusters list.
      Give it custom name 'TestClusterName'
    :result:
      Cluster is imported and its name is shown in the clusters list
    """
    clusters = application.collections.clusters.get_clusters()
    test_cluster = clusters[0]
    original_id = test_cluster.name
    test_cluster.cluster_import(cluster_name="TestClusterName")
    """
    :step:
      Unmanage the cluster
    :result:
      Cluster is unmanaged and its name is no longer shown in the clusters list.
      Its id is shown instead.
    """
    test_cluster.unmanage(original_id=original_id)


@pytest.mark.author("ebondare@redhat.com")
@pytest.mark.happypath
@pytest.mark.testready
def test_cluster_import_profiling_disabled(application):
    """
    Import cluster with profiling disabled. Then unmanage it.
    """
    """
    :step:
      Log in to Web UI and import the first cluster from the clusters list.
      Set profiling to Disabled during import
    :result:
      Cluster is imported and its name is shown in the clusters list
    """
    clusters = application.collections.clusters.get_clusters()
    test_cluster = clusters[0]
    test_cluster.cluster_import(profiling="disable")
    """
    :step:
      Check that cluster profiling is disabled
    :result:
      Check fails due to BZ 1670389
    """
    pytest.check(test_cluster.profiling == "Disabled",
                 issue='https://bugzilla.redhat.com/show_bug.cgi?id=1670389')
    """
    :step:
      Unmanage the cluster
    :result:
      Cluster is unmanaged
    """
    test_cluster.unmanage()
