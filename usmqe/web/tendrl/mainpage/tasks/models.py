"""
Common page model for tasks.
"""


from webstr.core import By, WebstrModel, PageElement
import webstr.patternfly.contentviews.models as contentviews
import webstr.common.form.models as form

from usmqe.web.utils import StatusIcon

LOCATION = "#/admin/tasks"


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
