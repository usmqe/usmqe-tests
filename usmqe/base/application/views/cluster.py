from widgetastic.widget import (Text, TextInput)

from usmqe.base.application.views.common import BaseLoggedInView
# from usmqe.base.application.widgets import Kebab
from usmqe.base.application.widgets import ListGroup
# from taretto.ui.patternfly import Button
from taretto.ui.patternfly import Dropdown


class ClustersView(BaseLoggedInView):
    # TODO: fix dropdown. If clicked, dropdown changes its name and won't be found anymore
    pagename = Text(".//h1")
    filter_type = Dropdown("Name")
    user_filter = TextInput(placeholder='Filter by Name')
    # TODO: use new widget
    # users = Table(".//table", column_widgets={5: Button("Edit"), 6: Kebab()})
    # temporary hack to import cluster
    # import_button = Button("Import")
    clusters = ListGroup('//div[@class="list-group list-view-pf list-view-pf-view ng-scope"]')

    @property
    def is_displayed(self):
        return self.pagename.text == "Clusters"
