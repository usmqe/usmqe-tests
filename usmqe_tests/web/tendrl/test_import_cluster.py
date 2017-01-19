"""
Description: Simple log in test

Author: ltrilety
"""


import pytest

from usmqe.web.tendrl.mainpage.navpage.pages import NavMenuBars
from usmqe.web.tendrl.mainpage.clusters.cluster_list.pages import ClusterList
from usmqe.web.tendrl.mainpage.landing_page.pages import get_landing_page


def test_initial_import_cluster(log_in, testcase_end):
    """ positive import cluster test
    """
    home_page = log_in.init_object
    pytest.check(home_page._label == 'home page',
                 'Tendrl should route to home page'
                 ' if there is no cluster present',
                 hard=True)
    import_cluster_page = home_page.import_cluster()
# TODO: Check hosts list
    import_cluster_page.import_click()
# TODO: Wait till the cluster is imported, check task
#       When finished, remove following line(s)
    import time
    time.sleep(60)
    log_in.driver.get(pytest.config.getini("usm_web_url"))
    home_page = get_landing_page(log_in.driver)

    pytest.check(home_page._label == 'main page - menu bar',
                 'Tendrl should not route to home page any more',
                 hard=True)
    NavMenuBars(log_in.driver).open_clusters(click_only=True)
    cluster_list = ClusterList(log_in.driver)
# TODO: Check that correct cluster is present in the list
    pytest.check(len(cluster_list) == 1,
                 'There should be exactly one cluster ion tendrl')
