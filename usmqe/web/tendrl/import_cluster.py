"""
Description: Simple import cluster auxiliary methods

Author: ltrilety
"""

import pytest

from webstr.selenium.ui.support import WebDriverUtils
from usmqe.web.tendrl.mainpage.navpage.pages import NavMenuBars
from usmqe.web.tendrl.mainpage.clusters.cluster_list.pages import\
    ClustersList, check_hosts
from usmqe.web.tendrl.mainpage.tasks.pages import TaskDetails
from usmqe.web.tendrl.mainpage.hosts.pages import HostsList
from usmqe.web.tendrl.task_wait import task_wait


IMPORT_TIMEOUT = 3600


def import_cluster_wait(driver, import_task_details):
    """
    wait till the import cluster task is finished

    Parameters:
        driver: selenium driver
        import_task_details: webstr page object with import_cluster method
                       landing_page-HomePage or cluster_list-ClustersMenu
        ttl (int): how long it waits till the tasks is finished
                   in seconds

    Returns:
        list of cluster objects
    """
    # Wait till the cluster is imported
    task_wait(import_task_details, ttl=IMPORT_TIMEOUT)

    NavMenuBars(driver).open_clusters(click_only=True)

    # TODO remove following sleep
    # sleep a while because of https://github.com/Tendrl/api/issues/159
    WebDriverUtils.wait_a_while(90, driver)

    cluster_list = ClustersList(driver)
    return cluster_list


def import_cluster(driver, import_page, clusters_nr=0, cluster_name=None,
                   cluster_ident=None, hosts=None):
    """
    import cluster

    Parameters:
        driver: selenium driver
        import_page: page object where the import button is present
        clusters_nr (int): number of clusters in clusters list
        cluster_name (str): name of the cluster
                            TODO: Not used for now
                                  https://github.com/Tendrl/api/issues/70
        cluster_ident: cluster identificator
        hosts (list): list of dictionaries
                      {'hostname': <hostname>, 'release': <release>, ...
                      for check only

    Returns:
        cluster name or id
    """
# TODO: Import specific cluster
    (cluster_ident, hosts_list) = import_page.import_cluster(
        cluster_ident=cluster_ident, name=cluster_name, hosts=hosts)
    import_task_details = TaskDetails(driver)

    cluster_list = import_cluster_wait(driver, import_task_details)

    # Check that cluster is present in the list
    pytest.check(len(cluster_list) == clusters_nr + 1,
                 'There should be one additional cluster in tendrl')
    # open cluster details for the imported cluster
    present = False
    for cluster in cluster_list:
        if cluster_ident.lower() in cluster.name.lower():
            cluster.open_details()
            present = True
            break
    pytest.check(present,
                 'The imported cluster should be present in the cluster list')

    # check hosts
    if present:
        page_hosts_list = HostsList(driver)
        check_hosts(hosts_list, page_hosts_list)
    return cluster_ident
