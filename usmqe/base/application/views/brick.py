from widgetastic.widget import Text, Table

from usmqe.base.application.views.common import BaseClusterSpecifiedView
from taretto.ui.patternfly import Button


class HostBricksView(BaseClusterSpecifiedView):
    """
    View for Brick details of a host.
    """
    pagename = Text(".//h1")
    hostname = Text(".//ul[@class='breadcrumb custom-breadcrumb']/li[@class='ng-binding']")
    bricks = Table(".//table", column_widgets={5: Button("Dashboard")})

    @property
    def is_displayed(self):
        return (self.pagename.text == "Brick Details" and
                self.hostname.text == self.context["object"].hostname)
