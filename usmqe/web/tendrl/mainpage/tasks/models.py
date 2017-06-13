"""
Common page model for tasks.
"""


from webstr.core import By, WebstrModel, PageElement, BaseWebElementHelper,\
    DynamicWebstrModel, RootPageElement, NameRootPageElement
import webstr.patternfly.contentviews.models as contentviews
import webstr.common.form.models as form

LOCATION = "#/admin/tasks"


class StatusIconHelper(BaseWebElementHelper):
    """
    StatusIcon helper (Selenium webelement wrapper).
    Provides basic methods for manipulation with a task status icon.
    """

    @property
    def value(self):
        """
        find status

        Returns:
            state of task
        """
        icon_class = self.get_attribute('class')
        if 'pficon-error-circle-o' in icon_class:
            return 'failed'
        elif 'pficon-ok' in icon_class:
            return 'finished'
        elif 'pficon-warning-triangle-o' in icon_class:
            return 'warning'
        elif 'fa-spinner' in icon_class:
            return 'new or processing'
        else:
            raise Exception('Unknown icon state')


class StatusIcon(PageElement):
    """
    Page element for a status icon.
    """
    _helper = StatusIconHelper


class TasksMenuModel(WebstrModel):
    """
    Tasks page top menu
    """
    header = PageElement(by=By.XPATH, locator="//h1[contains(text(),'Tasks')]")
    filter_by = form.Select(
        By.XPATH,
        '//select[contains(@ng-model, "filterBy")]')
    filter_input = form.TextInput(By.ID, 'filter')
    from_input = form.TextInput(
        By.XPATH,
        '//div[@ng-model="taskCntrl.date.fromDate"]/input')
    to_input = form.TextInput(
        By.XPATH,
        '//div[@ng-model="taskCntrl.date.toDate"]/input')


class TasksItemModel(contentviews.ListViewRowModel):
    """
    An item (row) in a Tasks list.
    """

    def _instance_identifier(self):
        """
        instance identifier: line number - 1
        """
        return self._name - 1

# Design: https://redhat.invisionapp.com/share/8N93NO7Q4
    status_icon = StatusIcon(
        by=By.XPATH,
        locator="./div/i")
    name_label = PageElement(
        by=By.XPATH,
        locator="./div[2]/a")
    name = name_label
    task_id = PageElement(
        by=By.XPATH,
        locator="./div[2]/p")
    submitted = PageElement(
        by=By.XPATH,
        locator="./div[3]/p[2]")
    status = PageElement(
        by=By.XPATH,
        locator="./div[4]/p")


class TasksListModel(contentviews.ListViewModel):
    """
    Page model for list of tasks.
    """


class TaskDetailsModel(WebstrModel):
    """ task details page model """
    tasks_link = PageElement(By.LINK_TEXT, locator="Tasks")
    name_id = PageElement(
        by=By.XPATH,
        locator="//li[./a[text()='Tasks']]/following-sibling::li/span")
    submitted = PageElement(
        by=By.XPATH,
        locator="//label[text()='Time Submitted:']/following-sibling::label")
    status = PageElement(
        by=By.XPATH,
        locator="//label[text()='Status:']/following-sibling::label")
    status_icon = StatusIcon(
        by=By.XPATH,
        locator="//label[text()='Status:']/following-sibling::label/i")
    # TODO
    # messages, not working for now


class TaskEventModel(DynamicWebstrModel):
    """
    An item (row) in a Tasks list.
    """
    _root = NameRootPageElement(
        by=By.ID,
        locator='log-list-group-item-%d')

# Design: https://redhat.invisionapp.com/share/8N93NO7Q4
    # missing status icon
    # status_icon = StatusIcon(
    #     by=By.XPATH,
    #     locator="./div/i")
    status_text = PageElement(
        by=By.XPATH,
        locator="./div[2]")
    message = PageElement(
        by=By.XPATH,
        locator="./div[3]")
    time = PageElement(
        by=By.XPATH,
        locator="./div[4]")


class TaskEventsModel(WebstrModel):
    """
    Page model for list of tasks.
    """
    LIST_XPATH = '//*[contains(concat(" ", @class, " "), '\
                 '" div-with-scroll-logs ")]'
    _root = RootPageElement(By.XPATH, LIST_XPATH)
    # header is a row too
    rows = PageElement(
        by=By.XPATH,
        locator=LIST_XPATH + "//*[contains(concat(' ', @class, ' '),"
        " ' list-group-item ')]",
        as_list=True)
