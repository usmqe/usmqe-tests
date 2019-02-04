from widgetastic.widget import Text
from widgetastic.widget import ParametrizedLocator, ParametrizedView

from usmqe.web.application.views.common import BaseLoggedInView
from usmqe.web.application.views.common import BaseClusterSpecifiedView


class ClusterTasksView(BaseClusterSpecifiedView):
    """
    List of tasks of the given cluster
    """
    @ParametrizedView.nested
    class tasks(ParametrizedView):
        """
        Nested view for each task
        """
        PARAMETERS = ("task_id",)
        ROOT = ParametrizedLocator(
            ".//p[contains(text(), {task_id|quote})]/ancestor-or-self::"
            "div[@class='ft-row list-group-item']")
        task_name = Text(".//a[@class='bold-text name ng-binding']")
        submitted_date = Text(".//div[text() = 'Submitted']/following-sibling::div")
        status = Text(".//div[@class='bold-text ng-binding']")
        changed_date = Text(".//div[@class='bold-text ng-binding']/following-sibling::div")

        @classmethod
        def all(cls, browser):
            return [e.text.split(" ")[2] for e in browser.elements(cls.ALL_IDS)
                    if browser.text(e) is not None and browser.text(e) != '']

    ALL_IDS = ".//a[@class='bold-text name ng-binding']/following-sibling::p"

    pagename = Text(".//h1")

    @property
    def all_task_ids(self):
        """
        Returns the list of all task IDs from the Tasks page
        """
        return [e.text.split(" ")[2] for e in self.browser.elements(self.ALL_IDS)]

    @property
    def is_displayed(self):
        return self.pagename.text == "Tasks"


class BaseEventsView(BaseLoggedInView):
    """
    Base view for task progress. Is used in TaskEventsView and MainTaskEventsView.
    """
    table_heading = Text(".//div[@class='row bold-text table-heading']")
    status = Text(".//form/div/label[text()[normalize-space(.)]='Status:']"
                  "/following-sibling::label")
    cluster_details = Text(".//a[@ng-click='glbTaskDetailCntrl.goToClusterDetail()']")
    task_name_and_id = Text(".//ul[@class='breadcrumb custom-breadcrumb ng-scope']"
                            "/li[@class='ng-binding']")

    @ParametrizedView.nested
    class events(ParametrizedView):
        """
        Nested view for each event during the task completion
        """
        PARAMETERS = ("event_id",)
        ALL_IDS = './/div[@class="row list-group-item logs ng-scope"]'
        ROOT = ParametrizedLocator('.//div[@id={event_id|quote}]')
        event_type = Text(".//div[@class='col-md-1 ng-binding']")
        description = Text(".//div[@class='col-md-6 ng-binding']")
        date = Text(".//div[@class='col-md-2 ng-binding']")

        @classmethod
        def all(cls, browser):
            return [e.text.split(" ")[2] for e in browser.elements(cls.ALL_IDS)
                    if browser.text(e) is not None and browser.text(e) != '']

    ALL_EVENTS = ".//div[@class='row list-group-item logs ng-scope']"

    @property
    def all_event_ids(self):
        return [e.get_attribute("id") for e in self.browser.elements(self.ALL_EVENTS)]


class TaskEventsView(BaseEventsView):
    """
    View for task progress of each task on the Tasks page.
    """
    @property
    def is_displayed(self):
        return (self.table_heading.text == "Events" and
                self.task_name_and_id.text.find(self.context["object"].task_id) > 0)


class MainTaskEventsView(BaseEventsView):
    """
    View for import and unmanage progress events.
    cluster_details link is only available after cluster import is complete
    """
    import_status = Text(".//label[@class='col-sm-4 col-md-1 status-value ng-binding']")
    cluster_details = Text(".//a[@ng-click='glbTaskDetailCntrl.goToClusterDetail()']")

    @property
    def is_displayed(self):
        return (self.table_heading.text == "Events")
