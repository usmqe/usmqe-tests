"""
Description: Simple cluster auxiliary methods

Author: ltrilety
"""

import pytest

from webstr.selenium.ui.support import WebDriverUtils
from webstr.selenium.ui.exceptions import InitPageValidationError

from usmqe.web.tendrl.mainpage.navpage.pages import NavMenuBars
from usmqe.web.tendrl.mainpage.clusters.cluster_list.pages import\
    ClustersList
from usmqe.web.tendrl.mainpage.clusters.import_cluster_wizard.pages\
    import ImportCluster
from usmqe.web.tendrl.mainpage.tasks.pages import TaskDetails
from usmqe.web.tendrl.task_wait import task_wait
# from usmqe.web.tendrl.mainpage.clusters.pages import check_hosts

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


def pre_check(init_object):
    """
    next cluster workflow pre-check

    Parameters:
        init_object: WebstrPage instance of page which is loaded after log in
    """
    pytest.check(init_object._label == 'main page - menu bar',
                 'Tendrl should route to page with a menu',
                 hard=True)


def post_check(driver, cluster_name, hosts, login_page=None):
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

        # Check that cluster is present in the list
        # open cluster details for the imported cluster
        present = False
        for cluster in cluster_list:
            if cluster_name.lower() in cluster.name.lower():
                pytest.check(
                    cluster.managed,
                    'cluster {} should be managed'.format(cluster.name))
                cluster.open_details()
                present = True
                break
        pytest.check(
            present,
            'The imported cluster should be present in the cluster list')

# TODO proper hosts list has to be added
#        # check hosts
#        if present:
#            page_hosts_list = ClusterMenu(driver).open_hosts()
#            check_hosts(hosts, page_hosts_list)
    except InitPageValidationError:
        # workaround for missing menu after cluster creation
        pass


def choose_cluster(driver, cluster_type=None):
    """
    select a cluster which should be imported

    NOTE: Chooses always the first cluster

    Parameters:
        driver: selenium driver
        cluster_type (str): which type of cluster should be imported
                                'ceph' or 'gluster'
                            None means that cluster type doesn't matter
                            NOTE not used for now

    Returns:
        ClustersRow instance
    """
    # Choose which cluster should be imported
    cluster_list = ClustersList(driver)
    pytest.check(len(cluster_list) > 0,
                 'There should be some cluster available',
                 hard=True)
    if cluster_type is None:
        cluster = next(iter(cluster_list))
# TODO use cluster type
#    elif cluster_type.lower() == 'gluster':
#        # Select first gluster cluster in the list of available clusters
#    elif cluster_type.lower() == 'ceph':
#        # Select first ceph cluster in the list of available clusters
#    else:
#        pytest.check(False, 'Unknown cluster type - {}'.format(cluster_type),
#                     hard=True)

    return cluster


def import_cluster(driver, init_object, cluster_type=None):
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

    init_object.open_clusters()

    cluster = choose_cluster(driver, cluster_type)

    cluster_ident = cluster.name

# TODO
# workaround for https://github.com/Tendrl/ui/issues/536
# button is not clickable, we use a javascript instead
#    cluster.click_on_import()
    driver.execute_script(
        'document.querySelector(\''
        'button[ng-click^="clusterCntrl.goToImportFlow(cluster)"]'
        '\').click()')

    import_page = ImportCluster(driver)

    hosts_list = import_page.import_cluster()

    cluster_job_wait(driver)

    post_check(driver, cluster_ident, hosts_list)
