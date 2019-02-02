from widgetastic.widget import Text, Table

from usmqe.base.application.views.common import BaseClusterSpecifiedView
from taretto.ui.patternfly import Button
from widgetastic.widget import ParametrizedLocator, ParametrizedView


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


class VolumeBricksView(BaseClusterSpecifiedView):
    pagename = Text(".//h1")
    volume_name = Text(".//ul[@class='breadcrumb custom-breadcrumb']/li[@class='ng-binding']")
    expand_all = Text(".//a[@ng-click='vm.expandAll()']")
    collapse_all = Text(".//a[@ng-click='vm.collapseAll()']")

    @ParametrizedView.nested
    class volume_parts(ParametrizedView):
        PARAMETERS = ("part_id",)
        ROOT = ParametrizedLocator("(.//div[@class='list-group list-view-pf list-view-pf-view"
                                   " ng-scope'])[position() = {part_id|quote}]")
        bricks = Table(".//table", column_widgets={5: Button("Dashboard")})

        @classmethod
        def all(cls, browser):
            return [browser.text(e) for e in browser.elements(cls.ALL_VOLUMES)
                    if browser.text(e) is not None and browser.text(e) != '']

    ALL_VOLUME_PARTS = ".//div[@class='list-group list-view-pf list-view-pf-view ng-scope']"

    @property
    def all_part_ids(self):
        """
        Returns the list of all subvolume/replica set IDs.
        They will be used as XPATH indeces, so they should start with 1.
        """
        return [str(i + 1) for i in range(len(self.browser.elements(self.ALL_VOLUME_PARTS)))]

    @property
    def is_displayed(self):
        return (self.pagename.text == "Brick Details" and
                self.volume_name.text == self.context["object"].volname)
