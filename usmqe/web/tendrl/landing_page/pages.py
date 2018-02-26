"""
Page objects for landing page

Author: ltrilety
"""


import time

from usmqe.web.tendrl.mainpage.clusters.cluster_list.pages import ClustersList


class LandingException(Exception):
    """
    unexpected landing page exception
    """


def get_landing_page(driver, timeout=10):
    """
    this function decides which landing age is active and returns proper object

    Parameters:
        driver: selenium web driver
        timeout (int): number of seconds,
                       which we wait till the final landing-page is displayed

    Returns:
        instance of
            landing_page.LandingPage OR
            clusters.clusterlist.ClustersList
    """
    wait_time = 0
    while 'landing-page' in driver.current_url and wait_time <= timeout:
        time.sleep(1)
        wait_time += 1
    if wait_time > timeout:
        raise LandingException('There should not remain landing-page in URL '
                               'longer than {} seconds'.format(timeout))
    if 'clusters' in driver.current_url:
        return ClustersList(driver)
    else:
        raise LandingException('Not expected landing page')
