from taretto.ui.core import TextInput, View
from taretto.ui.patternfly import Button
from widgetastic.widget import Checkbox, GenericLocatorWidget
from widgetastic.widget import Text, TextInput, View, Select
from taretto.ui.patternfly import Dropdown
from usmqe.base.application.widgets import NavDropdown
from widgetastic_patternfly import AboutModal


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
    #maybe it's just a button?
    modal = NavDropdown(".//button[@id='aboutModalDropdown']/parent::li")
    #TODO: navbar for normal user is smaller
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
    modal = AboutModal(id='aboutModal') 

    @property
    def is_displayed(self):
        return self.logged_in

    @property
    def logged_in(self):
        return self.navbar.is_displayed

    def log_out(self):
        self.parent.navbar.usermenu.select_item("Logout")

    def get_detail(self, field):
        """
        Open the about modal and fetch the value for one of the fields
        Raises ElementOrBlockNotFound if the field isn't in the about modal
        :param field: string label for the detail field
        :return: string value from the requested field
        """
        self.navbar.modal.click()
        try:
            return self.modal.items()[field]
        except KeyError:
            raise ElementOrBlockNotFound('No field named {} found in "About" modal.'.format(field))
        finally:
            # close since its a blocking modal and will break further navigation
            self.modal.close()


class DeleteConfirmationView(View):
    ROOT = ".//pf-modal-overlay-content"
    alert_name = Text(".//h4")
    cancel = Button("Cancel")
    delete = Button("Delete")


class MySettingsView(View):
    ROOT = ".//div[@id='userSettingModal']"
    popup_name = Text(".//h4[@id='modalTitle']")
    users_name = TextInput(name="name")
    password = TextInput(name="password")
    confirm_password = TextInput(name="confirmPassword")
    email = TextInput(name="userEmail")
    # TODO: add notifications_on = Checkbox(something)
    save_button = Button("Save")
    cancel_button = Button("Cancel")

    @property
    def is_displayed(self):
        return self.popup_name.text == "My Settings"


class AboutModalView(View):
    """
    The view for the about modal
    """
    @property
    def is_displayed(self):
        return self.modal.is_open

    modal = AboutModal(id='aboutModal')


def get_detail(field):
    """
    Open the about modal and fetch the value for one of the fields
    'title' and 'trademark' fields are allowed and get the header/footer values
    Raises ElementOrBlockNotFound if the field isn't in the about modal
    :param field: string label for the detail field
    :return: string value from the requested field
    """

    view = navigate_to('About')

    try:
        if field.lower() in ['title', 'trademark']:
            return getattr(view.modal, field.lower())
        else:
            return view.modal.items()[field]
    except KeyError:
        raise ElementOrBlockNotFound('No field named {} found in "About" modal.'.format(field))
    finally:
        # close since its a blocking modal and will break further navigation
        view.modal.close()
