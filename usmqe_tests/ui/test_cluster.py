# import pytest
# from usmqe.base.application.implementations.web_ui import ViaWebUI
# LOGGER = pytest.get_logger('ui_user_testing', module=True)
import time


def test_cluster_import(application):
    clusters = application.collections.clusters.get_clusters()
    test_cluster = clusters[0]
    test_cluster.cluster_import()
    time.sleep(5)
