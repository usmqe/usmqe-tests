# TODO
# update when it will work
"""
Page objects for Users page
"""


from webstr.core import WebstrPage

from usmqe.web.tendrl.auxiliary.users import models as m_users


class Users(WebstrPage):
    """
    Page object for Users page

    Atributes:
        _model - page model
        _label - human readable description of this *page object*
        TBD _required_elems - web elements to be checked
    """
    _model = m_users.UsersModel
    _label = 'Users page'
# TODO
# add _required_elems when possible
