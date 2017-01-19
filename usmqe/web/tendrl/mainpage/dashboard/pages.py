"""
Page objects for dashboard

Author: ltrilety
"""


from webstr.core import WebstrPage

from usmqe.web.tendrl.mainpage.dashboard import models as m_dashboard


class Dashboard(WebstrPage):
    """
    Page object for dashboard:

    Atributes:
        _model - page model
        _label - human readable description of this *page object*
        TBD _required_elems - web elements to be checked
    """
    _model = m_dashboard.DashboardModel
    _label = 'main page - dashboard'
