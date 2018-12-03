from widgetastic.widget import (GenericLocatorWidget, ParametrizedLocator, ParametrizedView, Text,
                                TextInput, Table, BaseInput)

from usmqe.base.application.views.common import BaseLoggedInView
from usmqe.base.application.widgets import BootstrapSwitch, Kebab, RadioGroup

from taretto.ui.patternfly import Button, Dropdown, BreadCrumb


class EditUserView(BaseLoggedInView):
    page_breadcrumb = BreadCrumb()
    user_id = Text(".//p[class='ng-binding']")
    users_name = TextInput(name="name")
    email = TextInput(name="userEmail")
    notifications_on = BootstrapSwitch(ngmodel="editUserCntrl.user.notification")
    password = TextInput(name="password")
    confirm_password = TextInput(name="confirmPassword")
    role = RadioGroup(".//div[./label[@for='role']]")
    save_button = Button("Save")
    cancel_button = Button("Cancel")

    @property
    def is_displayed(self):
        return False
