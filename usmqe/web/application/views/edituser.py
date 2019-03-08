from widgetastic.widget import Text, TextInput
from usmqe.web.application.views.common import BaseLoggedInView
from usmqe.web.application.widgets import BootstrapSwitch, RadioGroup
from taretto.ui.patternfly import Button, BreadCrumb


class EditUserView(BaseLoggedInView):
    """View for user editing page"""
    page_breadcrumb = BreadCrumb()
    user_id = Text(".//p[@class='ng-binding']")
    name = TextInput(name="name")
    email = TextInput(name="userEmail")
    notifications_on = BootstrapSwitch(ngmodel="editUserCntrl.user.notification")
    password = TextInput(name="password")
    confirm_password = TextInput(name="confirmPassword")
    role = RadioGroup(".//div[./label[@for='role']]")
    save_button = Button("Save")
    cancel_button = Button("Cancel")

    @property
    def is_displayed(self):
        return len(self.user_id.text) > 3
