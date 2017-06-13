"""
Description: Simple import cluster tests

Author: ltrilety
"""

import pytest

from usmqe.web.tendrl.mainpage.navpage.pages import NavMenuBars
from usmqe.web.tendrl.mainpage.clusters.cluster_list.pages import\
    ClustersList, ClustersMenu
from usmqe.web.tendrl.landing_page.pages import get_landing_page
from usmqe.web.tendrl.auxiliary.pages import UpperMenu
from usmqe.web.tendrl.mainpage.clusters.import_cluster_wizard.pages\
    import ImportCluster
from usmqe.web.tendrl import cluster_work


@pytest.fixture
def initial_import_cluster(valid_credentials):
    """
    positive import cluster test

    NOTE: 1. No cluster has to be imported
          2. There has to be at least one cluster which could be imported
    """
    home_page = valid_credentials.init_object
    pytest.check(home_page._label == 'home page',
                 'Tendrl should route to home page'
                 ' if there is no cluster present',
                 hard=True)

    yield valid_credentials

    import_page = ImportCluster(valid_credentials.driver)
    cluster_ident = cluster_work.import_cluster(valid_credentials.driver,
                                                import_page)

    # log out and log in again
    upper_menu = UpperMenu(valid_credentials.driver)
    upper_menu.open_user_menu().logout()
    valid_credentials.loginpage.login_user(
        pytest.config.getini("usm_username"),
        pytest.config.getini("usm_password"))
    # or just go to the default URL
    # valid_credentials.driver.get(pytest.config.getini("usm_web_url"))
    home_page = get_landing_page(valid_credentials.driver)

    pytest.check(home_page._label == 'main page - menu bar',
                 'Tendrl should not route to home page any more',
                 hard=True)

    # Check that cluster is present in the list
    NavMenuBars(valid_credentials.driver).open_clusters(click_only=True)
    clusters_list = ClustersList(valid_credentials.driver)

    pytest.check(len(clusters_list) == 1,
                 'There should be exactly one cluster in tendrl')
    present = False
    for cluster in clusters_list:
        if cluster_ident.lower() in cluster.name.lower():
            present = True
            break
    pytest.check(present,
                 'The imported cluster should be present in the cluster list')


@pytest.fixture
def import_cluster(valid_credentials):
    """
    positive import cluster test

    NOTE: 1. Some cluster has to be already present in the list
          2. There has to be at least one cluster which could be imported
    """
    nav_page = valid_credentials.init_object
    pytest.check(nav_page._label == 'main page - menu bar',
                 'Tendrl should route to dashboard page',
                 hard=True)
    clusters_list = nav_page.open_clusters()
    clusters_nr = len(clusters_list)
    valid_credentials.init_object = ClustersMenu(valid_credentials.driver)

    yield valid_credentials

    import_page = ImportCluster(valid_credentials.driver)
    import_cluster(valid_credentials.driver, import_page, clusters_nr)


def aux_import_gluster_cluster(driver, import_init_page):
    """
    auxiliary function for import gluster cluster
    choose first available gluster cluster

    Parameters:
        driver: selenium driver
        import_init_page: WebstrPage instance of page where import
                          button is present
    """
    initial_import_cluster.init_object.start_import_cluster()

    # Choose which cluster should be imported
    # Select first gluster cluster in the list of available clusters
    import_page = ImportCluster(driver)
    for cluster in import_page.avail_clusters:
        cluster.click()
        release = import_page.storage_service.lower()
        if 'gluster' in release:
            break
    pytest.check('gluster' in release,
                 'There should be some gluster cluster available',
                 hard=True)


def aux_import_ceph_cluster(driver, import_init_page):
    """
    auxiliary function for import ceph cluster
    choose first available ceph cluster

    Parameters:
        driver: selenium driver
        import_init_page: WebstrPage instance of page where import
                          button is present
    """
    initial_import_cluster.init_object.start_import_cluster()

    # Choose which cluster should be imported
    # Select first ceph cluster in the list of available clusters
    import_page = ImportCluster(driver)
    for cluster in import_page.avail_clusters:
        cluster.click()
        release = import_page.storage_service.lower()
        if 'ceph' in release:
            break
    pytest.check('ceph' in release,
                 'There should be some ceph cluster available',
                 hard=True)


def aux_import_generic_cluster(driver, import_init_page):
    """
    auxiliary function for import cluster
    choose first available cluster

    Parameters:
        driver: selenium driver
        import_init_page: WebstrPage instance of page where import
                          button is present
    """
    import_init_page.start_import_cluster()
    import_page = ImportCluster(driver)
    pytest.check(len(import_page.avail_clusters) > 0,
                 'There should be some cluster available',
                 hard=True)


@pytest.fixture
def initial_import_gluster_cluster(initial_import_cluster):
    """
    positive import gluster cluster test

    NOTE: 1. No cluster has to be imported
          2. There has to be at least one gluster cluster which could be imported
    """
# TODO: Choose specific cluster
    aux_import_gluster_cluster(initial_import_cluster.driver,
                           initial_import_cluster.init_object)


@pytest.fixture
def initial_import_ceph_cluster(initial_import_cluster):
    """
    positive import ceph cluster test

    NOTE: 1. No cluster has to be imported
          2. There has to be at least one ceph cluster which could be imported
    """
# TODO: Choose specific cluster
    aux_import_ceph_cluster(initial_import_cluster.driver,
                        initial_import_cluster.init_object)


@pytest.fixture
def initial_import_generic_cluster(initial_import_cluster):
    """
    positive import cluster test

    NOTE: 1. No cluster has to be imported
          2. There has to be at least one cluster which could be imported
    """
# TODO: Choose specific cluster
    aux_import_generic_cluster(initial_import_cluster.driver,
                           initial_import_cluster.init_object)


@pytest.fixture
def import_gluster_cluster(import_cluster):
    """
    positive import gluster cluster test

    NOTE: 1. Some cluster has to be already present in the list
          2. There has to be at least one gluster cluster which could be imported
    """
# TODO: Choose specific cluster
    aux_import_gluster_cluster(import_cluster.driver,
                           import_cluster.init_object)


@pytest.fixture
def import_ceph_cluster(import_cluster):
    """
    positive import ceph cluster test

    NOTE: 1. Some cluster has to be already present in the list
          2. There has to be at least one ceph cluster which could be imported
    """
# TODO: Choose specific cluster
    aux_import_ceph_cluster(import_cluster.driver,
                        import_cluster.init_object)


@pytest.fixture
def import_generic_cluster(import_cluster):
    """
    positive import cluster test

    NOTE: 1. Some cluster has to be already present in the list
          2. There has to be at least one cluster which could be imported
    """
# TODO: Choose specific cluster
    aux_import_generic_cluster(import_cluster.driver,
                           import_cluster.init_object)


@pytest.mark.Gluster
def test_initial_import_gluster_cluster(initial_import_gluster_cluster):
    """
    positive import gluster cluster test

    NOTE: 1. No cluster has to be imported
          2. There has to be at least one gluster cluster which could be imported
    """


@pytest.mark.Ceph
def test_initial_import_ceph_cluster(initial_import_ceph_cluster):
    """
    positive import ceph cluster test

    NOTE: 1. No cluster has to be imported
          2. There has to be at least one ceph cluster which could be imported
    """


@pytest.mark.Other
def test_initial_import_generic_cluster(initial_import_generic_cluster):
    """
    positive import cluster test

    NOTE: 1. No cluster has to be imported
          2. There has to be at least one cluster which could be imported
    """


@pytest.mark.Gluster
def test_import_gluster_cluster(import_gluster_cluster):
    """
    positive import gluster cluster test

    NOTE: 1. Some cluster has to be already present in the list
          2. There has to be at least one gluster cluster which could be imported
    """


@pytest.mark.Ceph
def test_import_ceph_cluster(import_ceph_cluster):
    """
    positive import ceph cluster test

    NOTE: 1. Some cluster has to be already present in the list
          2. There has to be at least one ceph cluster which could be imported
    """


@pytest.mark.Other
def test_import_generic_cluster(import_generic_cluster):
    """
    positive import cluster test

    NOTE: 1. Some cluster has to be already present in the list
          2. There has to be at least one cluster which could be imported
    """
