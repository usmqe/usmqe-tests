from widgetastic.widget import TextInput

from usmqe.web.application.views.common import BaseLoggedInView
from usmqe.web.application.widgets import BootstrapSwitch, RadioGroup

from taretto.ui.patternfly import Button, BreadCrumb


class AddUserView(BaseLoggedInView):
    """View for the page where the new user's information is filled """
    page_breadcrumb = BreadCrumb()
    user_id = TextInput(name="username")
    name = TextInput(name="name")
    email = TextInput(name="userEmail")
    notifications_on = BootstrapSwitch(ngmodel="addUserCntrl.user.notification")
    password = TextInput(name="password")
    confirm_password = TextInput(name="confirmPassword")
    role = RadioGroup(".//div[./label[@for='role']]")
    save_button = Button("Save")
    cancel_button = Button("Cancel")

    @property
    def is_displayed(self):
        return self.logged_in and self.page_breadcrumb.locations == ["Users", "Add User"]
