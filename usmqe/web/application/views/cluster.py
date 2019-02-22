from widgetastic.widget import Text, View
# from widgetastic.widget import TextInput

from usmqe.web.application.views.common import BaseLoggedInView
from usmqe.web.application.widgets import Kebab
from taretto.ui.patternfly import Button, Dropdown
from widgetastic.widget import ParametrizedLocator, ParametrizedView


class ClustersView(BaseLoggedInView):
    """
    List of clusters
    There's no list-group widget, so it had to be a parametrized view.
    """

    @ParametrizedView.nested
    class clusters(ParametrizedView):
        """
        Nested view for each cluster
        """
        PARAMETERS = ("cluster_id",)
        ALL_CLUSTERS = ".//div[@class='list-group-item']"
        ALL_CLUSTER_IDS = ".//div[@class='list-view-pf-description']/descendant-or-self::*/text()"
        ROOT = ParametrizedLocator(
            "//div/*[text()[normalize-space(.)]={cluster_id|quote}]/ancestor-or-self::"
            "div[@class='list-group-item']")
        cluster_version = Text(".//div[text() = 'Cluster Version']/following-sibling::h5")
        managed = Text(".//div[text() = 'Managed']/following-sibling::h5")
        hosts = Text(".//div[text() = 'Hosts']/following-sibling::h5")
        volumes = Text(".//div[text() = 'Volumes']/following-sibling::h5")
        alerts = Text(".//div[text() = 'Alerts']/following-sibling::h5")
        profiling = Text(".//div[text() = 'Volume Profiling']/following-sibling::h5")
        status = Text(".//div[@class='list-view-pf-additional-info-item cluster-text']")
        import_button = Button("contains", "Import")
        dashboard_button = Button("Dashboard")
        actions = Kebab()

        @property
        def health(self):
            return self.browser.elements(".//div[@class='list-view-pf-left']"
                                         "/i")[0].get_attribute("uib-tooltip")

        @classmethod
        def all(cls, browser):
            return [browser.text(e) for e in browser.elements(cls.ALL_CLUSTER_IDS)
                    if browser.text(e) is not None and browser.text(e) != '']

    ALL_CLUSTER_IDS = ".//div[@class='list-view-pf-description']"

    # TODO: fix dropdown. If clicked, dropdown changes its name and won't be found anymore
    pagename = Text(".//h1")
    filter_type = Dropdown("Name")
    # TextInput can't be defined by placeholder
    # user_filter = TextInput(placeholder='Filter by Name')

    @property
    def all_ids(self):
        """Returns the list of all cluster ids in the clusters list """
        return [self.browser.text(e) for e in self.browser.elements(self.ALL_CLUSTER_IDS)
                if self.browser.text(e) is not None and self.browser.text(e) != '']

    @property
    def is_displayed(self):
        return self.pagename.text == "Clusters"


class ConfirmationView(View):
    """
    Base view for all confirmation modals
    """
    ROOT = ".//pf-modal-overlay-content"
    alert_name = Text(".//h4")
    cancel = Button("Cancel")


class UnmanageConfirmationView(ConfirmationView):
    """
    View for cluster unmanage confirmation modal
    """
    unmanage = Button("Unmanage")


class ExpandConfirmationView(ConfirmationView):
    """
    View for cluster expansion confirmation modal
    """
    expand = Button("Expand")


class UnmanageTaskSubmittedView(View):
    """
    View for "Unmanage Task submitted" modal.
    """
    ROOT = ".//pf-modal-overlay-content"
    CLOSE_LOC = './/div[@class="modal-header"]/button[@class="close ng-scope"]'
    view_progress = Button("contains", "View Task Progress")

    def close(self):
        """Close the modal"""
        self.browser.click(self.CLOSE_LOC, parent=self)
