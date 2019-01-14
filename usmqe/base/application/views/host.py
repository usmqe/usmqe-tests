from widgetastic.widget import Text, View

from usmqe.base.application.views.common import BaseClusterSpecifiedView
from taretto.ui.patternfly import Button
from widgetastic.widget import ParametrizedLocator, ParametrizedView


class ClusterHostsView(BaseClusterSpecifiedView):
    """List of hosts of the given cluster
    """
    @ParametrizedView.nested
    class hosts(ParametrizedView):
        """Nested view for each host"""
        PARAMETERS = ("hostname",)
        ROOT = ParametrizedLocator(
            ".//div/a[text()[normalize-space(.)]={hostname|quote}]/ancestor-or-self::"
            "div[@class='ft-row list-group-item ng-scope']")
        gluster_version = Text(".//div[text() = 'Gluster Version']/following-sibling::div")
        managed = Text(".//div[text() = 'Managed']/following-sibling::div")
        role = Text(".//div[text() = 'Role']/following-sibling::div")
        bricks = Text(".//div[text() = 'Bricks']/following-sibling::div")
        alerts = Text(".//div[text() = 'Alerts']/following-sibling::div")
        dashboard_button = Button("Dashboard")

        @classmethod
        def all(cls, browser):
            return [browser.text(e) for e in browser.elements(cls.ALL_HOSTNAMES)
                    if browser.text(e) is not None and browser.text(e) != '']

    ALL_HOSTNAMES = ".//div[@class='ft-column ft-main host-name bold-text']/a"

    pagename = Text(".//h1")

    @property
    def all_hostnames(self):
        """Returns the list of all hostnames on the Hosts page"""
        return [self.browser.text(e) for e in self.browser.elements(self.ALL_HOSTNAMES)
                if self.browser.text(e) is not None and self.browser.text(e) != '']

    @property
    def is_displayed(self):
        return self.pagename.text == "Hosts"


class GrafanaHostDashboard(View):
    dashboard_name = Text(".//a[@class='navbar-page-btn']")
    cluster_name = Text(".//label[text() = 'Cluster Name']/parent::div/value-select-dropdown")
    host_name = Text(".//label[text() = 'Host Name']/parent::div/value-select-dropdown")
    host_health = Text(".//span[text() = 'Health']/ancestor::div[@class='panel-container']"
                       "/descendant::span[@class='singlestat-panel-value']")
    # brick total looks like " - 5" instead of "5"
    bricks_total = Text(".//span[text() = 'Total']/following-sibling::span")

    @property
    def is_displayed(self):
        return self.dashboard_name.text.find("Host Dashboard") >= 0
