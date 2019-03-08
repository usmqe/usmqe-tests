from widgetastic.widget import Text, TextInput, Table
# from widgetastic.exceptions import NoSuchElementException
# from widgetastic.widget import GenericLocatorWidget, ParametrizedLocator, ParametrizedView

from usmqe.web.application.views.common import BaseLoggedInView
from usmqe.web.application.widgets import Kebab
from taretto.ui.patternfly import Button, Dropdown


class UsersView(BaseLoggedInView):
    """
    View for Users page. Available to admin only
    """
    # TODO: fix dropdown. If clicked, dropdown changes its name and won't be found anymore
    pagename = Text(".//h1")
    filter_type = Dropdown("User ID")
    user_filter = TextInput(locator=".//input[@placeholder='Filter by User ID']")
    adduser = Button("Add")
    users = Table(".//table", column_widgets={5: Button("Edit"), 6: Kebab()})

    @property
    def is_displayed(self):
        return self.pagename.text == "Users" and len(self.users.row()[0].text) > 2
