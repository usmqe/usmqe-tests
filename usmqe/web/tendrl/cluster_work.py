"""
Description: Simple cluster auxiliary methods

Author: ltrilety
"""

import pytest

from webstr.selenium.ui.support import WebDriverUtils
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
from usmqe.web.tendrl.mainpage.clusters.create_cluster_wizard.\
    general.pages import CreateCluster
import usmqe.web.tendrl.mainpage.clusters.create_cluster_wizard.\
    gluster.pages as gluster
# import usmqe.web.tendrl.mainpage.clusters.create_cluster_wizard.\
#     gluster.ceph as ceph
from usmqe.api.tendrlapi import glusterapi

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

    task_wait(ttl=IMPORT_TIMEOUT)

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
    pytest.check(present,
                 'The imported cluster should be present in the cluster list')

    # check hosts
    if present:
        page_hosts_list = ClusterMenu(driver).open_hosts()
        check_hosts(hosts, page_hosts_list)

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
                break
        pytest.check(present,
                     "The cluster '{}' should be present in the "
                     "cluster list".format(cluster_name))


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
    next_pre_check(init_object)

    clusters_list = init_object.open_clusters()
    clusters_nr = len(clusters_list)
    cluster_menu = ClustersMenu(driver)

    cluster_menu.start_import_cluster()

    import_page = choose_cluster(driver, cluster_type)

    (cluster_ident, hosts_list) = import_page.import_cluster()

    cluster_job_wait(driver)

    post_check(driver, cluster_ident, hosts_list, clusters_nr)


def import_cluster(driver, init_object, login_page, cluster_type=None):
    """
    positive import cluster workflow

    NOTE: There has to be at least one cluster which could be imported

    Parameters:
        driver: selenium driver
        init_object: WebstrPage instance of page which is loaded after log in
        login_page: LoginPage instance
        cluster_type (str): which type of cluster should be imported
                                'ceph' or 'gluster'
                            None means that cluster type doesn't matter
    """
    if init_object._label == 'home page':
        initial_import_cluster(driver, init_object, login_page, cluster_type)
    else:
        next_import_cluster(driver, init_object, cluster_type)


def create_gluster_cluster(driver, init_object, login_page, hosts,
                           api_valid_credentials, network=None):
    """
    positive import cluster workflow

    NOTE: There has to be at least one cluster which could be imported

    Parameters:
        driver: selenium driver
        init_object: WebstrPage instance of page which is loaded after log in
        login_page: LoginPage instance
        hosts (list): list of hostnames
                      nodes which should be part of cluster
                      Note: list is enough however it could change to
                            dictionary later with some nodes parameters
        api_valid_credentials: TendrlAuth object (defines bearer token header),
                               when auth is None, requests are send without
                               athentication header
        network (string): cluster network
                          Note: It could be part of nodes parameters later
    """
    if init_object._label == 'home page':
        initial_create_gluster_cluster(
            driver, init_object, login_page, hosts,
            api_valid_credentials, network)
    else:
        next_create_gluster_cluster(
            driver, init_object, hosts, api_valid_credentials, network)


def initial_create_gluster_cluster(
        driver, init_object, login_page, hosts,
        api_valid_credentials, network=None):
    """
    create gluster cluster workflow

    NOTE: There has to be no cluster in tendrl

    Parameters:
        driver: selenium driver
        init_object: WebstrPage instance of page which is loaded after log in
        login_page: LoginPage instance
        hosts (list): list of hostnames
                      nodes which should be part of cluster
                      Note: list is enough however it could change to
                            dictionary later with some nodes parameters
        api_valid_credentials: TendrlAuth object (defines bearer token header),
                               when auth is None, requests are send without
                               athentication header
        network (string): cluster network
                          Note: It could be part of nodes parameters later
    """
    initial_pre_check(init_object)

    init_object.start_create_cluster()

    cluster_ident = aux_create_gluster_cluster(
        driver, hosts, api_valid_credentials, network)

    post_check(driver, cluster_ident, hosts, 0, login_page)


def next_create_gluster_cluster(driver, init_object, hosts,
                                api_valid_credentials, network=None):
    """
    positive create gluster cluster workflow

    NOTE: Some cluster has to be already present in the list

    Parameters:
        driver: selenium driver
        init_object: WebstrPage instance of page which is loaded after log in
        hosts (list): list of hostnames
                      nodes which should be part of cluster
                      Note: list is enough however it could change to
                            dictionary later with some nodes parameters
        api_valid_credentials: TendrlAuth object (defines bearer token header),
                               when auth is None, requests are send without
                               athentication header
        network (string): cluster network
                          Note: It could be part of nodes parameters later
    """
    next_pre_check(init_object)

    clusters_list = init_object.open_clusters()
    clusters_nr = len(clusters_list)
    cluster_menu = ClustersMenu(driver)

    cluster_menu.start_create_cluster()

    cluster_ident = aux_create_gluster_cluster(
        driver, hosts, api_valid_credentials, network)

    post_check(driver, cluster_ident, hosts, clusters_nr)


def aux_create_gluster_cluster(driver, hosts, api_valid_credentials,
                               network=None):
    """
    Create gluster cluster

    Parameters:
        driver: selenium driver
        hosts (list): list of hostnames
                      nodes which should be part of cluster
                      Note: list is enough however it could change to
                            dictionary later with some nodes parameters
        api_valid_credentials: TendrlAuth object (defines bearer token header),
                               when auth is None, requests are send without
                               athentication header
        network (string): cluster network
                          Note: It could be part of nodes parameters later

    Returns:
        tendrl cluster name
    """
    # choose to create gluster cluster
    initial_page = CreateCluster(driver)
    initial_page.choose_gluster_creation()

    step = gluster.StepGeneral(driver)
    # check service
    pytest.check(step.service == 'Gluster', "We chose to create a gluster "
                 "cluster, hence the 'Storage Service' should be 'Gluster', "
                 "it is {}".format(step.service))
    # click on next as change of name have no impact
    step.click_next()

    step = gluster.StepNetworkAndHosts(driver)

    # choose network
    if network is not None:
        step.cluster_network = network
        pytest.check(
            network in step.cluster_network,
            "Cluster networ should be {}, it is {}".format(
                network, step.cluster_network[0]))
    # TODO: check select_all, deselect_all links functionality
    #       check filter fields functionality
    # select proper nodes
    available_hosts = gluster.CreateHostsList(driver)
    for host in available_hosts:
        if host.name in hosts:
            host.select()
            # TODO: check host parameters
    # click on next
    step.click_next()

    step = gluster.StepReview(driver)
    # TODO: check cluster summary
    # check nodes
    page_hosts_list = gluster.HostsSumList(driver)
    check_hosts(hosts, page_hosts_list)
    # TODO: check nodes parameters
    # start the job
    step.create_cluster()

    # wait till it finishes
    task_page = ViewTaskPage(driver)
    task_page.view_task()
    # Get task id
    task_id = cluster_job_wait(driver)

    # Get cluster name
    # use API
    api = glusterapi.TendrlApiGluster(auth=api_valid_credentials)

    integration_id = api.get_job_attribute(
        job_id=task_id,
        attribute="TendrlContext.integration_id",
        section="parameters")

    api.get_cluster_list()
    # TODO(fbalak) remove this sleep after
    #              https://github.com/Tendrl/api/issues/159 is resolved.
    import time
    time.sleep(30)

    imported_clusters = [x for x in api.get_cluster_list()
                         if x["integration_id"] == integration_id]

    cluster_name = imported_clusters[0]["cluster_name"]

    return cluster_name


# TODO
#   def create_ceph_cluster(...
