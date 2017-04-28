"""
Description: Simple log in test

Author: ltrilety
"""


import time
import datetime
import pytest

from usmqe.web.tendrl.mainpage.navpage.pages import NavMenuBars
from usmqe.web.tendrl.mainpage.clusters.cluster_list.pages import ClustersList
from usmqe.web.tendrl.landing_page.pages import get_landing_page
from usmqe.web.tendrl.auxiliary.pages import UpperMenu


def test_initial_import_cluster(valid_credentials):
    """ positive import cluster test """
    home_page = valid_credentials.init_object
    pytest.check(home_page._label == 'home page',
                 'Tendrl should route to home page'
                 ' if there is no cluster present',
                 hard=True)

    import_task_details = home_page.import_cluster()

    # Wait till the cluster is imported, check task
    # status_text should be New, later changed to Processing
    # finally Finished and status icon should have the same state
    status_str = import_task_details.status_text
    # No status icon presented till the end
    # status = import_task_details.status
    start_time = datetime.datetime.now()
    # one hour timeout for the job to finish
    timeout = datetime.timedelta(0, 3600, 0)
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
        'New state too long',
        hard=True)
    while status_str == 'Processing' and\
            datetime.datetime.now() - start_time <= timeout:
        time.sleep(5)
        status_str = import_task_details.status_text
    pytest.check(
        datetime.datetime.now() - start_time <= timeout,
        'Timeout check: The state of import cluster task should not remain in '
        'Processing state too long',
        hard=True)
    pytest.check(
        status_str == 'Finished',
        'import cluster status should be Finished, it is {}'.format(status_str))
    pytest.check(
        import_task_details.status == 'finished',
        'import cluster status icon should be in finished state, '
        'it is in {} state'.format(import_task_details.status))

    # log out and log in again
    # TODO remove following sleep
    # sleep a while because of https://github.com/Tendrl/api/issues/159
    time.sleep(30)
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
    NavMenuBars(valid_credentials.driver).open_clusters(click_only=True)
    cluster_list = ClustersList(valid_credentials.driver)
# TODO: Check that correct cluster is present in the list
    pytest.check(len(cluster_list) == 1,
                 'There should be exactly one cluster in tendrl')
