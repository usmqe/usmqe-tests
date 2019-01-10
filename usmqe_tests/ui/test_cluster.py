import pytest
# from usmqe.base.application.implementations.web_ui import ViaWebUI
# LOGGER = pytest.get_logger('ui_user_testing', module=True)
# import time

from usmqe.api.tendrlapi import glusterapi
from usmqe.gluster import gluster


def test_cluster_import(application, valid_session_credentials):
    clusters = application.collections.clusters.get_clusters()
    test_cluster = clusters[0]
    pytest.check(test_cluster.managed == "No")
    tendrl_api = glusterapi.TendrlApiGluster(auth=valid_session_credentials)
    api_cluster = tendrl_api.get_cluster(test_cluster.name)
    pytest.check(
        api_cluster["is_managed"] == "no",
        "is_managed: {}\nThere should be ``no``.".format(api_cluster["is_managed"]))
    test_cluster.cluster_import()
    api_cluster = tendrl_api.get_cluster(test_cluster.name)
    pytest.check(
        api_cluster["is_managed"] == "yes",
        "is_managed: {}\nThere should be ``yes``.".format(api_cluster["is_managed"]))


def test_cluster_disable_profiling(application):
    clusters = application.collections.clusters.get_clusters()
    test_cluster = clusters[0]
    gluster_cluster = gluster.GlusterVolume()
    pytest.check(gluster_cluster.get_clusterwide_profiling() == "enabled")
    test_cluster.disable_profiling()
    pytest.check(gluster_cluster.get_clusterwide_profiling() == "disabled")


def test_cluster_enable_profiling(application):
    clusters = application.collections.clusters.get_clusters()
    test_cluster = clusters[0]
    gluster_cluster = gluster.GlusterVolume()
    pytest.check(gluster_cluster.get_clusterwide_profiling() == "disabled")
    test_cluster.enable_profiling()
    pytest.check(gluster_cluster.get_clusterwide_profiling() == "enabled")


def test_cluster_unmanage(application, valid_session_credentials):
    clusters = application.collections.clusters.get_clusters()
    test_cluster = clusters[0]
    tendrl_api = glusterapi.TendrlApiGluster(auth=valid_session_credentials)
    api_cluster = tendrl_api.get_cluster(test_cluster.name)
    pytest.check(
        api_cluster["is_managed"] == "yes",
        "is_managed: {}\nThere should be ``yes``.".format(api_cluster["is_managed"]))
    test_cluster.unmanage()
    api_cluster = tendrl_api.get_cluster(test_cluster.name)
    pytest.check(
        api_cluster["is_managed"] == "no",
        "is_managed: {}\nThere should be ``no``.".format(api_cluster["is_managed"]))


def test_cluster_import_naming(application):
    clusters = application.collections.clusters.get_clusters()
    test_cluster = clusters[0]
    original_id = test_cluster.name
    test_cluster.cluster_import(cluster_name="TestClusterName")
    test_cluster.unmanage(original_id=original_id)
