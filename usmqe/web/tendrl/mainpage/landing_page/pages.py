"""
Page objects for navigation bars (both top and left menu bars).

* popup menus
* menubars

Author: ltrilety
"""


from webstr.core import WebstrPage

import usmqe.web.tendrl.mainpage.landing_page.models as m_landing_page
from usmqe.web.tendrl.mainpage.navpage.pages import NavMenuBars
from usmqe.web.tendrl.mainpage.clusters.import_cluster_wizard.pages\
    import ImportCluster


class LandingException(Exception):
    """
    unexpected landing page exception
    """


def get_landing_page(driver):
    """
    this function decides which landing age is active and returns proper object

    Parameters:
        driver: selenium web driver
    Returns:
        instance of
            landing_page.LandingPage OR
            clusters.clusterlist.ClusterList
    """
    if 'cluster' in driver.current_url:
        return NavMenuBars(driver)
    elif 'home' in driver.current_url:
        return Home(driver)
    else:
        raise LandingException('Not expected landing page')


class Home(WebstrPage):
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
    _required_elems = [
        'welcome_message',
        'import_btn'
    ]

    def import_cluster(self, click_only=False):
        """
        Opens import cluster dialog.

        Parameters:
            click_only (bool): just click on the link and return None

        Returns:
            Instance of ImportClusterConfigure from
            clusters.import_cluster_wizard.pages
        """
        self._model.import_btn.click()
        if click_only:
            return None
        return ImportCluster(self.driver)
