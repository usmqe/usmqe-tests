# TODO
# update when it will work
"""
Page objects for Volumes page
"""


from webstr.core import WebstrPage

from usmqe.web.tendrl.details.volumes import models as m_volumes


class Volumes(WebstrPage):
    """
    Page object for Volumes page

    Atributes:
        _model - page model
        _label - human readable description of this *page object*
        TBD _required_elems - web elements to be checked
    """
    _model = m_volumes.VolumesModel
    _label = 'Volumes page'
# TODO
# add _required_elems when possible
