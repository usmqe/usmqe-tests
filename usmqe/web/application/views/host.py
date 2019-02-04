from widgetastic.widget import Text

from usmqe.web.application.views.common import BaseClusterSpecifiedView
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
        host_name = Text(".//div[@class='ft-column ft-main host-name bold-text']/a")
        gluster_version = Text(".//div[text() = 'Gluster Version']/following-sibling::div")
        managed = Text(".//div[text() = 'Managed']/following-sibling::div")
        role = Text(".//div[text() = 'Role']/following-sibling::div")
        bricks = Text(".//div[text() = 'Bricks']/following-sibling::div")
        alerts = Text(".//div[text() = 'Alerts']/following-sibling::div")
        dashboard_button = Button("Dashboard")

        @property
        def health(self):
            return self.browser.elements(".//div[@class='ft-column ft-icon']"
                                         "/i")[0].get_attribute("uib-tooltip-html").strip("'")

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
