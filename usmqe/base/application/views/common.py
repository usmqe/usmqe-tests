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
    ROOT = ".//nav[@class='navbar-pf-vertical tendrl-header-container']"
    title = Text(".//a[@class='navbar-brand']")
    clusters = Select(".//select[@id='repeatSelect']")
    #TODO: navbar for normal user is smaller
    usermanagement = NavDropdown(".//a[@id='usermanagement']/parent::li")
    alerts = NavDropdown(".//a[@id='notifications']/parent::li")
    usermenu = NavDropdown(".//a[@id='usermenu']/parent::li")


#class AdminNavbar(Navbar):
#    usermanagement = NavDropdown(".//a[@id='usermanagement']")


class BaseLoggedInView(View):
    navbar = View.nested(Navbar)

    @property
    def is_displayed(self):
        return self.logged_in

    @property
    def logged_in(self):
        return self.navbar.is_displayed
