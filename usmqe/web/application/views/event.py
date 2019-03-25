from widgetastic.widget import Text

from usmqe.web.application.views.common import BaseClusterSpecifiedView
from widgetastic.widget import ParametrizedLocator, ParametrizedView


class ClusterEventsView(BaseClusterSpecifiedView):
    """
    List of events of the given cluster
    """
    @ParametrizedView.nested
    class events(ParametrizedView):
        """Nested view for each event"""
        PARAMETERS = ("event_id",)
        ROOT = ParametrizedLocator("(.//div[@class='ft-row list-group-item'])"
                                   "[position() = {event_id|quote}]")
        description = Text(".//div[@class='ft-column ft-main event-desc']/div")
        date = Text(".//div[@class='ft-column']/div")

        @classmethod
        def all(cls, browser):
            return [browser.text(e) for e in browser.elements(cls.ALL_VOLUMES)
                    if browser.text(e) is not None and browser.text(e) != '']

    ALL_EVENTS = ".//div[@class='ft-row list-group-item']"

    pagename = Text(".//h1")

    @property
    def all_event_ids(self):
        """
        Returns the list of all event IDs from the Tasks page.
        They will be used as XPATH indeces, so they should start with 1.
        """
        return [str(i + 1) for i in range(len(self.browser.elements(self.ALL_EVENTS)))]

    @property
    def is_displayed(self):
        return (self.pagename.text == "Events" and
                len(self.results.text) > 3 and
                self.results.text[0] != '0')
