from widgetastic.widget import Text, Table

from usmqe.web.application.views.common import BaseClusterSpecifiedView
from taretto.ui.patternfly import Button
from widgetastic.widget import ParametrizedLocator, ParametrizedView
from usmqe.web import tools


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
                self.hostname.text == self.context["object"].hostname and
                len(self.results.text) > 3 and
                tools.bricks_displayed(self, self.context["object"].bricks_count, None))


class VolumeBricksView(BaseClusterSpecifiedView):
    """
    View for Brick details of a volume.
    Each volume part (replica set or subvolume) has its own bricks table.
    """
    pagename = Text(".//h1")
    volume_name = Text(".//ul[@class='breadcrumb custom-breadcrumb']/li[@class='ng-binding']")
    expand_all = Text(".//a[@ng-click='vm.expandAll()']")
    collapse_all = Text(".//a[@ng-click='vm.collapseAll()']")

    @ParametrizedView.nested
    class volume_parts(ParametrizedView):
        """
        Nested view for each volume part.
        """
        PARAMETERS = ("part_id",)
        ROOT = ParametrizedLocator("(.//div[@class='list-group list-view-pf list-view-pf-view"
                                   " ng-scope'])[position() = {part_id|quote}]")
        bricks = Table(".//table", column_widgets={5: Button("Dashboard")})
        part_name = Text(".//div[@class='list-group-item-heading "
                         "bold-text sub-volume ng-binding']")
        brick_count = Text(".//div[@class='list-view-pf-additional-info-item ng-binding']")
        utilization = Text(".//utilisation-chart")

        @classmethod
        def all(cls, browser):
            return [browser.text(e) for e in browser.elements(cls.ALL_VOLUMES)
                    if browser.text(e) is not None and browser.text(e) != '']

        @property
        def is_expanded(self):
            return self.browser.elements("div")[0].get_attribute("class").find("expand"
                                                                               "-active") > 0

    ALL_VOLUME_PARTS = ".//div[@class='list-group list-view-pf list-view-pf-view ng-scope']"

    @property
    def all_part_ids(self):
        """
        Returns the list of all subvolume/replica set IDs.
        They will be used as XPATH indeces, so they should be strings and start with 1.
        """
        return [str(i + 1) for i in range(len(self.browser.elements(self.ALL_VOLUME_PARTS)))]

    @property
    def is_displayed(self):
        return (self.pagename.text == "Brick Details" and
                self.volume_name.text == self.context["object"].volname and
                len(self.results.text) > 3)
