# TODO
# update when it will work
"""
Page objects for Events page
"""


from webstr.core import WebstrPage

from usmqe.web.tendrl.auxiliary.events import models as m_events


class Events(WebstrPage):
    """
    Page object for Events page

    Atributes:
        _model - page model
        _label - human readable description of this *page object*
        TBD _required_elems - web elements to be checked
    """
    _model = m_events.EventsModel
    _label = 'Events page'
# TODO
# add _required_elems when possible
