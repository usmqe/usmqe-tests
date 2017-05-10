"""
Description: Simple import cluster auxiliary methods

Author: ltrilety
"""

import time
import datetime
import pytest

from usmqe.web.tendrl.mainpage.navpage.pages import NavMenuBars
from usmqe.web.tendrl.mainpage.clusters.cluster_list.pages import\
    ClustersList, check_hosts
from usmqe.web.tendrl.mainpage.tasks.pages import TaskDetails
from usmqe.web.tendrl.mainpage.hosts.pages import HostsList


def import_cluster_wait(driver, import_task_details, ttl=3600):
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
    # Wait till the cluster is imported, check task
    # status_text should be New, later changed to Processing
    # finally Finished and status icon should have the same state
    status_str = import_task_details.status_text
    # No status icon presented till the end
    # status = import_task_details.status
    start_time = datetime.datetime.now()
    # one hour timeout for the job to finish
    timeout = datetime.timedelta(0, ttl, 0)
    while status_str != 'Processing' and\
            datetime.datetime.now() - start_time <= timeout/4:
        pytest.check(
            status_str == 'New',
            'import cluster status should be New, it is {}'.format(status_str))
        time.sleep(5)
        status_str = import_task_details.status_text
    pytest.check(
        datetime.datetime.now() - start_time <= timeout/4,
        'Timeout check: The state of import cluster task should not remain in '
        'New state too long, longer than {} seconds'.format(ttl/4),
        hard=True)
    while status_str == 'Processing' and\
            datetime.datetime.now() - start_time <= timeout:
        time.sleep(5)
        status_str = import_task_details.status_text
    pytest.check(
        datetime.datetime.now() - start_time <= timeout,
        'Timeout check: The state of import cluster task should not remain in '
        'Processing state too long, longer than {} seconds'.format(ttl),
        hard=True)
    pytest.check(
        status_str == 'Finished',
        'import cluster status should be Finished, '
        'it is {}'.format(status_str))
    pytest.check(
        import_task_details.status == 'finished',
        'import cluster status icon should be in finished state, '
        'it is in {} state'.format(import_task_details.status))

    # TODO remove following sleep
    # sleep a while because of https://github.com/Tendrl/api/issues/159
    time.sleep(30)

    NavMenuBars(driver).open_clusters(click_only=True)
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
        if cluster_ident in cluster.name:
            cluster.open_details()
            present = True
            break
    pytest.check(present,
                 'The imported cluster is present in the cluster list')
    page_hosts_list = HostsList(driver)
    check_hosts(hosts_list, page_hosts_list)
    return cluster_ident
