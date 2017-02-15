# TODO
# update when it will work
"""
Page objects for tasks
"""


from webstr.core import WebstrPage

from usmqe.web.tendrl.mainpage.admin.tasks import models as m_tasks


class Tasks(WebstrPage):
    """
    Page object for Tasks

    Atributes:
        _model - page model
        _label - human readable description of this *page object*
        TBD _required_elems - web elements to be checked
    """
    _model = m_tasks.TasksModel
    _label = 'admin page - tasks'
# TODO
# add _required_elems when possible
