"""
Tasks page abstraction.
"""


from selenium.webdriver.common.keys import Keys

from webstr.core import WebstrPage
from webstr.patternfly.contentviews import pages as contentviews
import webstr.common.containers.pages as containers

import usmqe.web.tendrl.mainpage.tasks.models as m_tasks


class TasksMenu(WebstrPage):
    """
    page object for tasks top menu
    """
    _model = m_tasks.TasksMenuModel
    _label = 'tasks top menu'
    _required_elems = [
        'filter_by',
        'filter_input',
        'from_input',
        'to_input'
    ]

    def set_filter(self, filter_type=None, filter_input=None):
        """
        Set filter and press ENTER key

        Parameters:
            filter_type (str) - by which type of filter tasks are filtered by
            filter_input (str) - text to be filled in the filter text field
        """
        if filter_type is not None:
            self._model.filter_by.value = filter_type
        if filter_input is not None:
            self._model.filter_input.value = filter_input
        self._model.filter_input.send_keys(Keys.RETURN)

    def set_from(self, from_input):
        """
        Set from input and press ENTER key

        Parameters:
            from_input (str) - string to be put to the 'from' field
                             - e.g. '06 Apr 2017'
        """
        self._model.from_input.value = from_input
        self._model.from_input.send_keys(Keys.RETURN)

    def set_to(self, to_input):
        """
        Set to input and press ENTER key

        Parameters:
            to_input (str) - string to be put to the 'to' field
                           - e.g. '06 Apr 2017'
        """
        self._model.to_input.value = to_input
        self._model.to_input.send_keys(Keys.RETURN)


class TasksItem(contentviews.ListViewRow):
    """
    An item (row) in a Tasks list.
    """
    _model = m_tasks.TasksItemModel
    _label = 'tasks row'
    _required_elems = [
        '_root',
        'status_icon',
        'name_label',
        'task_id',
        'submitted',
        'status']

    @property
    def status(self):
        """
        find status

        Returns:
            status_icon element title
        """
        return self._model.status_icon.value

    @property
    def name(self):
        """
        returns task name
        """
        return self._model.name.text

    def click_on(self):
        """
        open tasks details page
        click on task name
        """
        self._model.name.click()

    @property
    def status_text(self):
        """
        returns task status text
        """
        return self._model.status.text


class TasksList(contentviews.ListView):
    """
    Base page object for List of tasks.
    """
    _model = m_tasks.TasksListModel
    _label = 'main page - admin - tasks'
    _row_class = TasksItem


class TaskDetails(WebstrPage):
    """
    page object for task details page
    """
    _model = m_tasks.TaskDetailsModel
    _label = 'task details'
    _timeout = 30
    _required_elems = [
        'name_id',
        'submitted',
        'status_icon',
        'status',
    ]

    def go_to_tasks(self):
        """
        click on Tasks link
        """
        self._model.tasks_link.click()

    @property
    def name_id(self):
        """
        returns task name plus id
        e.g.  'ImportCluster: 98dc6483-3cbc-42c6-a835-4e179316937d'
        """
        return self._model.name_id.text

    @property
    def status(self):
        """
        find status

        Returns:
            status_icon element title
        """
        return self._model.status_icon.value

    @property
    def status_text(self):
        """
        returns task status text
        """
        return self._model.status.text

    # TODO
    # work with messages


class TaskEvent(containers.ContainerRowBase):
    """
    An item (row) in a Tasks list.
    """
    _model = m_tasks.TaskEventModel
    _label = 'tasks event'
    _required_elems = [
        'status_text',
        'message',
        'time']

    @property
    def status_text(self):
        """
        find status

        Returns:
            status text
        """
        return self._model.status_text.text

    @property
    def message(self):
        """
        Returns:
            event message
        """
        return self._model.message.text

    @property
    def time(self):
        """
        Returns:
            event time
        """
        return self._model.time.text


class TaskEvents(containers.ContainerBase):
    """
    Base page object for List of task events.
    """
    _model = m_tasks.TaskEventsModel
    _label = 'task events'
    _row_class = TasksItem
    _required_elems = ['_root']

    @property
    def events_nr(self):
        """
        Returns:
            number of events
        """
        return len(self._model.rows)
