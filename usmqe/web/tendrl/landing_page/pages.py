"""
Page objects for navigation bars (both top and left menu bars).

* popup menus
* menubars

Author: ltrilety
"""


import copy
import time

from usmqe.web.tendrl.auxiliary.pages import UpperMenu
import usmqe.web.tendrl.landing_page.models as m_landing_page
from usmqe.web.tendrl.mainpage.navpage.pages import NavMenuBars
from usmqe.web.tendrl.mainpage.clusters.pages import ClustersWorkBase


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
    if 'dashboard' in driver.current_url:
        return NavMenuBars(driver)
    elif 'home' in driver.current_url:
        return Home(driver)
    else:
        raise LandingException('Not expected landing page')


class Home(UpperMenu, ClustersWorkBase):
    """
    Common page object for navigation bars:

    - left navigation menu bar (with links to other pages)
    - top navigation menu bar (with icons for popup menus)

    Atributes:
        _model - page model
        _label - human readable description of this *page object*
        _required_elems - web elements to be checked
    """
    _model = m_landing_page.HomeModel
    _label = 'home page'
    _required_elems = copy.deepcopy(UpperMenu._required_elems)
    _required_elems.extend([
        'welcome_message',
        'import_btn'
    ])
