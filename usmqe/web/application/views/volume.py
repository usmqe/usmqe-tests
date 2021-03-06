from widgetastic.widget import Text

from usmqe.web.application.views.common import BaseClusterSpecifiedView
from taretto.ui.patternfly import Button
from widgetastic.widget import ParametrizedLocator, ParametrizedView


class ClusterVolumesView(BaseClusterSpecifiedView):
    """List of volumes of the given cluster
    """
    @ParametrizedView.nested
    class volumes(ParametrizedView):
        """Nested view for each volume"""
        PARAMETERS = ("volume_name",)
        ROOT = ParametrizedLocator(
            ".//div/a[text()[normalize-space(.)]={volume_name|quote}]/ancestor-or-self::"
            "div[@class='ft-row list-group-item ng-scope']")
        volname = Text(".//div[@class='bold-text long-volume-name']/a")
        volume_type = Text(".//div[@class='pull-left vol-type ng-binding']")
        bricks = Text(".//div[text() = 'Bricks']/following-sibling::div")
        running = Text(".//div[text() = 'Running']/following-sibling::div")
        rebalance = Text(".//div[text() = 'Rebalance']/following-sibling::div")
        profiling = Text(".//div[text() = 'Volume Profiling']/following-sibling::div")
        alerts = Text(".//div[text() = 'Alerts']/following-sibling::div")
        enable_profiling = Button("Enable Profiling")
        disable_profiling = Button("Disable Profiling")
        dashboard_button = Button("Dashboard")

        @property
        def health(self):
            """
            Returns the corresponding expected value of Grafana Health panel
            TODO: find out the icon for state 'Failed'
            """
            health = self.browser.elements(".//div[@class='ft-column ft-icon']"
                                           "/i")[0].get_attribute("class")
            if health == "pficon pficon-ok":
                return "Up"
            elif health == "pficon pficon-degraded icon-orange":
                return "Up(Degraded)"
            elif health == "pficon pficon-degraded icon-red":
                return "Up(Partial)"
            elif health == "fa ffont fa-arrow-circle-o-down":
                return "Down"
            elif health == "fa ffont fa-question":
                return "Unknown"
            else:
                return "Unexpected state"

        @classmethod
        def all(cls, browser):
            return [browser.text(e) for e in browser.elements(cls.ALL_VOLUMES)
                    if browser.text(e) is not None and browser.text(e) != '']

    ALL_VOLUMES = ".//a[contains(@class,'volume-name')]"

    pagename = Text(".//h1")

    @property
    def all_volnames(self):
        """Returns the list of all volumes on the Volumes page"""
        return [self.browser.text(e) for e in self.browser.elements(self.ALL_VOLUMES)
                if self.browser.text(e) is not None and self.browser.text(e) != '']

    @property
    def is_displayed(self):
        return self.pagename.text == "Volumes" and len(self.results.text) > 3
