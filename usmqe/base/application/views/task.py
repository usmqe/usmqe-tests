from widgetastic.widget import Text
# from widgetastic.widget import View
from widgetastic.widget import ParametrizedLocator, ParametrizedView

from usmqe.base.application.views.common import BaseLoggedInView


class TaskProgressView(BaseLoggedInView):
    """View for task progress."""
    table_heading = Text("div[@class='row bold-text table-heading']")
    status = Text(".//form/div/label[text()[normalize-space(.)]='Status:']"
                  "/following-sibling::label")
    cluster_details = Text("a[@ng-click='glbTaskDetailCntrl.goToClusterDetail()']")

    @ParametrizedView.nested
    class events(ParametrizedView):
        """Nested view for each event during the task completion"""
        PARAMETERS = ("event_id",)
        ALL_IDS = 'div[@class="row list-group-item logs ng-scope"]/@id'
        ROOT = ParametrizedLocator('.//div[@id={event_id|quote}]')
        event_type = Text(".//div[@class='col-md-1 ng-binding']")
        event_text = Text(".//div[@class='col-md-6 ng-binding']")
        event_date = Text(".//div[@class='col-md-2 ng-binding']")

    @property
    def is_displayed(self):
        return self.table_heading.text == "Events"
