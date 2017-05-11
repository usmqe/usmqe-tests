"""
Description: Simple import cluster tests

Author: ltrilety
"""

import pytest

from usmqe.web.tendrl.import_cluster import import_cluster
from usmqe.web.tendrl.mainpage.navpage.pages import NavMenuBars
from usmqe.web.tendrl.mainpage.clusters.cluster_list.pages import\
    ClustersList, ClustersMenu
from usmqe.web.tendrl.landing_page.pages import get_landing_page
from usmqe.web.tendrl.auxiliary.pages import UpperMenu


def test_initial_import_cluster(valid_credentials):
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

# TODO: Import specific cluster
    cluster_ident = import_cluster(valid_credentials.driver, home_page)

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


def test_import_cluster(valid_credentials):
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
    clusters_menu = ClustersMenu(valid_credentials.driver)

# TODO: Import specific cluster
    import_cluster(valid_credentials.driver, clusters_menu, clusters_nr)
