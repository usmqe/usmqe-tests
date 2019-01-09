# import pytest
# from usmqe.base.application.implementations.web_ui import ViaWebUI
# LOGGER = pytest.get_logger('ui_user_testing', module=True)
import time


def test_cluster_import(application):
    clusters = application.collections.clusters.get_clusters()
    test_cluster = clusters[0]
    test_cluster.cluster_import()


def test_cluster_disable_profiling(application):
    clusters = application.collections.clusters.get_clusters()
    test_cluster = clusters[0]
    test_cluster.disable_profiling()


def test_cluster_enable_profiling(application):
    clusters = application.collections.clusters.get_clusters()
    test_cluster = clusters[0]
    test_cluster.enable_profiling()


def test_cluster_unmanage(application):
    clusters = application.collections.clusters.get_clusters()
    test_cluster = clusters[0]
    test_cluster.unmanage()
    time.sleep(20)


def test_cluster_import_naming(application):
    clusters = application.collections.clusters.get_clusters()
    test_cluster = clusters[0]
    original_id = test_cluster.name
    test_cluster.cluster_import(cluster_name="TestClusterName")
    test_cluster.unmanage(original_id=original_id)

