from widgetastic.widget import (GenericLocatorWidget, ParametrizedLocator, ParametrizedView, Text,
                                TextInput, Table, BaseInput)

from usmqe.base.application.views.common import BaseLoggedInView
from usmqe.base.application.widgets import Kebab
from taretto.ui.patternfly import Button, Dropdown, BootstrapSwitch, BreadCrumb


class AddUserView(BaseLoggedInView):
    page_breadcrumb = BreadCrumb()
    user_id = TextInput(name="username")
    users_name = TextInput(name="name")
    email = TextInput(name="userEmail")
    notifications_on = BootstrapSwitch(id="email-notification")
    password = TextInput(name="password")
    confirm_password = TextInput(name="confirmPassword")
    is_admin = BaseInput(id="role1")
    is_normal_user = BaseInput(id="role2")
    is_limited_user = BaseInput(id="role3")
    save_button = Button("Save")
    cancel_button = Button("Cancel")
 
    @property
    def is_displayed(self):
        return (
            self.logged_in and
# TODO: check what's in the breadcrumb
            self.pagename.text == "Users")
