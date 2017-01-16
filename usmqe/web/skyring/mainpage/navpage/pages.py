# vim: set tabstop=2 shiftwidth=2 softtabstop=2 colorcolumn=120:
"""
Page objects for navigation bars (both top and left menu bars).

* popup menus
* menubars

Author: ltrilety
"""


from webstr.core import WebstrPage

from usmqe.web.skyring.mainpage.navpage import models as m_navpage


class NavMenuBars(WebstrPage):
    """
    Common page object for navigation bars:

    - left navigation menu bar (with links to other pages)
    - top navigation menu bar (with icons for popup menus)

    Parameters:
        (_location - initial URL to load upon instance creation)
        _model - page model
        _label - human readable description of this *page object*
        _required_elems - web elements to be checked
    """
#    _location = m_navpage.location
    _model = m_navpage.NavMenuBarsModel
    _label = 'main page - menu bar'
    _required_elems = [
        # left part of upper navbar
        'navbar_toggle',
        'navbar_brand',
        # right part of upper navbar
        'alerts_link',
        'hosts_link',
        'progress_link',
        'user_link',
        # left navbar
        'dashboard_link',
        'clusters_link',
        'hosts_link',
        'storages_link',
        'admin_link'
    ]
