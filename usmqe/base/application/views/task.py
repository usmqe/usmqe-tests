from widgetastic.widget import Text
from widgetastic.widget import ParametrizedLocator, ParametrizedView

from usmqe.base.application.views.common import BaseLoggedInView
from usmqe.base.application.views.common import BaseClusterSpecifiedView


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


class TaskEventsView(BaseLoggedInView):
    """
    View for task progress.
    """
    table_heading = Text(".//div[@class='row bold-text table-heading']")
    status = Text(".//form/div/label[text()[normalize-space(.)]='Status:']"
                  "/following-sibling::label")
    cluster_details = Text(".//a[@ng-click='glbTaskDetailCntrl.goToClusterDetail()']")

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

    @property
    def is_displayed(self):
        return self.table_heading.text == "Events"
