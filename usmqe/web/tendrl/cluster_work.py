"""
Description: Simple cluster auxiliary methods

Author: ltrilety
"""

import pytest

from webstr.selenium.ui.support import WebDriverUtils
from webstr.selenium.ui.exceptions import InitPageValidationError

from usmqe.web.tendrl.mainpage.navpage.pages import NavMenuBars
from usmqe.web.tendrl.mainpage.clusters.cluster_list.pages import\
    ClustersList, ClustersMenu
from usmqe.web.tendrl.landing_page.pages import get_landing_page
from usmqe.web.tendrl.auxiliary.pages import UpperMenu
from usmqe.web.tendrl.mainpage.clusters.import_cluster_wizard.pages\
    import ImportCluster
from usmqe.web.tendrl.mainpage.clusters.cluster.pages import ClusterMenu
from usmqe.web.tendrl.mainpage.clusters.pages import ViewTaskPage
from usmqe.web.tendrl.mainpage.tasks.pages import TaskDetails
from usmqe.web.tendrl.task_wait import task_wait
from usmqe.web.tendrl.mainpage.clusters.pages import check_hosts

IMPORT_TIMEOUT = 3600


def cluster_job_wait(driver):
    """
    wait till the import/create cluster task is finished

    Parameters:
        driver: selenium driver
        ttl (int): how long it waits till the tasks is finished
                   in seconds

    Returns:
        task id
    """
    # Wait till the cluster is imported/created
    task_details = TaskDetails(driver)
    task_id = task_details.name_id.split(':')[1].lstrip()

    task_wait(driver, ttl=IMPORT_TIMEOUT)

    return task_id


def initial_pre_check(init_object):
    """
    initial cluster workflow pre-check

    NOTE: There has to be no cluster in tendrl

    Parameters:
        init_object: WebstrPage instance of page which is loaded after log in
    """
    pytest.check(init_object._label == 'home page',
                 'Tendrl should route to home page'
                 ' if there is no cluster present',
                 hard=True)


def next_pre_check(init_object):
    """
    next cluster workflow pre-check

    NOTE: Some cluster has to be already present in the list

    Parameters:
        init_object: WebstrPage instance of page which is loaded after log in
    """
    pytest.check(init_object._label == 'main page - menu bar',
                 'Tendrl should route to dashboard page',
                 hard=True)


def post_check(driver, cluster_name, hosts, clusters_nr, login_page=None):
    """
    cluster workflow post-check

    Parameters:
        driver: selenium driver
        cluster_name (str): cluster name
        hosts (list): list of dictionaries
                      {'hostname': <hostname>, 'release': <release>, ...
                      for check only
        clusters_nr (int): previous number of clusters in clusters list
        login_page: LoginPage instance
    """
    try:
        NavMenuBars(driver).open_clusters(click_only=True)

        # TODO remove following sleep
        # sleep a while because of https://github.com/Tendrl/api/issues/159
        WebDriverUtils.wait_a_while(90, driver)

        cluster_list = ClustersList(driver)
        return cluster_list
        # Check that cluster is present in the list
        pytest.check(len(cluster_list) == clusters_nr + 1,
                     'There should be one additional cluster in tendrl')
        # open cluster details for the imported cluster
        present = False
        for cluster in cluster_list:
            if cluster_name.lower() in cluster.name.lower():
                cluster.open_details()
                present = True
                break
        pytest.check(
            present,
            'The imported cluster should be present in the cluster list')

        # check hosts
        if present:
            page_hosts_list = ClusterMenu(driver).open_hosts()
            check_hosts(hosts, page_hosts_list)
    except InitPageValidationError:
        # workaround for missing menu after cluster creation
        pass

    # Note next steps are done only for initial import/create
    if login_page:
        # log out and log in again
        upper_menu = UpperMenu(driver)
        upper_menu.open_user_menu().logout()
        login_page.login_user(
            pytest.config.getini("usm_username"),
            pytest.config.getini("usm_password"))
        # or just go to the default URL
        # driver.get(pytest.config.getini("usm_web_url"))
        home_page = get_landing_page(driver)

        pytest.check(home_page._label == 'main page - menu bar',
                     'Tendrl should not route to home page any more',
                     hard=True)

        # Check that cluster is present in the list
        NavMenuBars(driver).open_clusters(click_only=True)
        clusters_list = ClustersList(driver)

        pytest.check(len(clusters_list) == 1,
                     'There should be exactly one cluster in tendrl')
        present = False
        for cluster in clusters_list:
            if cluster_name.lower() in cluster.name.lower():
                present = True
                cluster.open_details()
                break
        pytest.check(present,
                     "The cluster '{}' should be present in the "
                     "cluster list".format(cluster_name))

        # check hosts
        if present:
            page_hosts_list = ClusterMenu(driver).open_hosts()
            check_hosts(hosts, page_hosts_list)


def choose_cluster(driver, cluster_type=None):
    """
    select a cluster which should be imported

    Parameters:
        driver: selenium driver
        cluster_type (str): which type of cluster should be imported
                                'ceph' or 'gluster'
                            None means that cluster type doesn't matter

    Returns:
        ImportCluster instance
    """
    # Choose which cluster should be imported
    import_page = ImportCluster(driver)
    if cluster_type is None:
        pytest.check(len(import_page.avail_clusters) > 0,
                     'There should be some cluster available',
                     hard=True)
    elif cluster_type.lower() == 'gluster':
        # Select first gluster cluster in the list of available clusters
        for cluster in import_page.avail_clusters:
            cluster.click()
            release = import_page.storage_service.lower()
            if 'gluster' in release:
                break
            pytest.check('gluster' in release,
                         'There should be some gluster cluster available',
                         hard=True)
    elif cluster_type.lower() == 'ceph':
        # Select first ceph cluster in the list of available clusters
        for cluster in import_page.avail_clusters:
            cluster.click()
            release = import_page.storage_service.lower()
            if 'ceph' in release:
                break
        pytest.check('ceph' in release,
                     'There should be some ceph cluster available',
                     hard=True)
    else:
        pytest.check(False, 'Unknown cluster type - {}'.format(cluster_type),
                     hard=True)

    return import_page


def initial_import_cluster(driver, init_object, login_page,
                           cluster_type=None):
    """
    positive import cluster workflow

    NOTE: 1. There has to be no cluster in tendrl
          2. There has to be at least one cluster which could be imported

    Parameters:
        driver: selenium driver
        init_object: WebstrPage instance of page which is loaded after log in
        login_page: LoginPage instance
        cluster_type (str): which type of cluster should be imported
                                'ceph' or 'gluster'
                            None means that cluster type doesn't matter
    """
    initial_pre_check(init_object)

    init_object.start_import_cluster()

    import_page = choose_cluster(driver, cluster_type)

    (cluster_ident, hosts_list) = import_page.import_cluster()

    cluster_job_wait(driver)

    post_check(driver, cluster_ident, hosts_list, 0, login_page)


def next_import_cluster(driver, init_object, cluster_type=None):
    """
    positive import cluster workflow

    NOTE: 1. Some cluster has to be already present in the list
          2. There has to be at least one cluster which could be imported

    Parameters:
        driver: selenium driver
        init_object: WebstrPage instance of page which is loaded after log in
        cluster_type (str): which type of cluster should be imported
                                'ceph' or 'gluster'
                            None means that cluster type doesn't matter
    """
    pre_check(init_object)

    clusters_list = init_object.open_clusters()
    cluster_menu = ClustersMenu(driver)

    # TODO
    #cluster_menu.start_import_cluster()

    cluster_ident = choose_cluster(driver, cluster_type)

    # TODO
    hosts_list = import_page.import_cluster()

    cluster_job_wait(driver)

    post_check(driver, cluster_ident, hosts_list)
