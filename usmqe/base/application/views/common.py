from taretto.ui.core import TextInput, View
from taretto.ui.patternfly import Button
from widgetastic.widget import Checkbox, GenericLocatorWidget
from widgetastic.widget import Text, TextInput, View, Select
from taretto.ui.patternfly import NavDropdown

class LoginPage(View):
    username = TextInput(id="username")
    password = TextInput(id="password")
    log_in = Button("Log In")


class Navbar(View):
    ROOT = ".//nav[@class='navbar-pf-vertical tendrl-header-container']"
    title = Text(".//a[@class='navbar-brand']")
    clusters = Select(".//select[@id='repeatSelect']")
    # TODO: navbar for normal user is smaller
    usermanagement = NavDropdown(".//a[@id='usermanagement']")
    alerts = NavDropdown(".//a[@id='notifications']")
    usermenu = NavDropdown(".//a[@id='usermenu']")


class BaseLoggedInView(View):
    navbar = View.nested(Navbar)

    @property
    def logged_in(self):
        return len(self.navbar.clusters.text) > 2
