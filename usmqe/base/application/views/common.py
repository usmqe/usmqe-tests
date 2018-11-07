from taretto.ui.core import TextInput, View
from taretto.ui.patternfly import Button
from widgetastic.widget import Checkbox, GenericLocatorWidget
from widgetastic.widget import Text, TextInput, View, Select
from taretto.ui.patternfly import Dropdown
from usmqe.base.application.widgets import NavDropdown


class LoginPage(View):
    username = TextInput(id="username")
    password = TextInput(id="password")
    log_in = Button("Log In")

    @property
    def is_displayed(self):
        return self.log_in.is_displayed


class Navbar(View):
    ROOT = ".//nav[@class='navbar navbar-pf-vertical navbar-pf-contextselector tendrl-header-container']"
    title = Text(".//a[@class='navbar-brand']")
    clusters = Select(".//select[@id='repeatSelect']")
    #TODO: navbar for normal user is smaller
    modal = NavDropdown(".//button[@id='aboutModalDropdown']/parent::li")
    usermanagement = NavDropdown(".//a[@id='usermanagement']/parent::li")
    alerts = NavDropdown(".//a[@id='notifications']/parent::li")
    usermenu = NavDropdown(".//a[@id='usermenu']/parent::li")


# TODO: AdminNavbar is different
#class AdminNavbar(Navbar):
#    usermanagement = NavDropdown(".//a[@id='usermanagement']")


# TODO: use VerticalNavigation
#class VerticalNavbar(View):
#    ROOT = ".//nav[@class='nav-pf-vertical nav-pf-vertical-with-secondary-nav hidden-icons-pf']"
    # hosts = 
    # volumes =
    # tasks =
    # events = 
    # TODO: learn how to use sub-menu


class BaseLoggedInView(View):
    navbar = View.nested(Navbar)

    @property
    def is_displayed(self):
        return self.logged_in

    @property
    def logged_in(self):
        return self.navbar.is_displayed


class DeleteConfirmationView(View):
    ROOT = ".//pf-modal-overlay-content"
    alert_name = Text(".//h4")
    cancel = Button("Cancel")
    delete = Button("Delete")


class MySettingsView(View):
    ROOT = ".//pf-modal-overlay-content"
    popup_name = Text(".//h4")
    users_name = TextInput(name="name")
    password = TextInput(name="password")
    confirm_password = TextInput(name="confirmPassword")
    email = TextInput(name="userEmail")
    # TODO: add notifications_on = Checkbox(something)
    save_button = Button("Save")
    cancel_button = Button("Cancel")
