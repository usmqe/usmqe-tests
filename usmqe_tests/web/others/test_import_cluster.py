"""
Description: Simple import cluster tests

Author: ltrilety
"""

import pytest

from usmqe.web.tendrl import cluster_work


@pytest.mark.skipif(pytest.config.getini('skip_invalid'),
                    reason='not valid for ci testing')
@pytest.mark.other
def test_initial_import_cluster(valid_credentials):
    """
    positive import cluster test

    NOTE: 1. No cluster has to be imported
          2. There has to be at least one cluster which could be imported
    """
# TODO: Choose specific cluster
    cluster_work.initial_import_cluster(
        valid_credentials.driver,
        valid_credentials.init_object,
        valid_credentials.loginpage)


@pytest.mark.skipif(pytest.config.getini('skip_invalid'),
                    reason='not valid for ci testing')
@pytest.mark.other
def test_next_import_cluster(valid_credentials):
    """
    positive import cluster test

    NOTE: 1. Some cluster has to be already present in the list
          2. There has to be at least one cluster which could be imported
    """
# TODO: Choose specific cluster
    cluster_work.next_import_cluster(
        valid_credentials.driver,
        valid_credentials.init_object)


@pytest.mark.skipif(pytest.config.getini('skip_invalid'),
                    reason='not valid for ci testing')
@pytest.mark.other
def test_import_cluster(valid_credentials):
    """
    positive import cluster test

    NOTE: There has to be at least one cluster which could be imported
    """
# TODO: Choose specific cluster
    cluster_work.import_cluster(
        valid_credentials.driver,
        valid_credentials.init_object,
        valid_credentials.loginpage)
