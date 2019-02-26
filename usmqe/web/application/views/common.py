from taretto.ui.patternfly import Button
from widgetastic.widget import Checkbox
from widgetastic.widget import Text, TextInput, View, Select
from widgetastic_patternfly import AboutModal
from widgetastic.widget import ParametrizedLocator, ParametrizedView

from usmqe.web.application.widgets import NavDropdown


class LoginPage(View):
    """
    View for login page
    """
    username = TextInput(id="username")
    password = TextInput(id="password")
    log_in = Button("Log In")

    @property
    def is_displayed(self):
        return self.log_in.is_displayed


class Navbar(View):
    """
    Navigation bar on top of every page except the login page.
    usermanagement is only available to admins
    """
    ROOT = ".//nav[contains(@class,'navbar-pf-contextselector tendrl-header-container')]"
    title = Text(".//a[@class='navbar-brand']")
    clusters = Select(".//select[contains(@ng-change, 'goToClusterPage')]")
    modal = NavDropdown(".//button[@id='aboutModalDropdown']/parent::li")
    usermanagement = NavDropdown(".//a[@id='usermanagement']/parent::li")
    alerts = NavDropdown(".//a[@id='notifications']/parent::li")
    usermenu = NavDropdown(".//a[@id='usermenu']/parent::li")


class VerticalNavbar(View):
    """
    Vertical navigation bar for views where cluster is specified.
    Can't use VerticalNavigation widget because Tasks item never gets attribute 'active'
    """
    ROOT = ".//nav[@class='nav-pf-vertical nav-pf-vertical-with-secondary-nav hidden-icons-pf']"
    hosts = Text(".//li[@data-target='#Hosts']")
    volumes = Text(".//li[@data-target='#Volumes']")
    tasks = Text(".//li[@data-target='#Tasks']")
    events = Text(".//li[@data-target='#Events']")


class BaseLoggedInView(View):
    """
    Base view so that every page will inherit navbar and about modal
    """
    navbar = View.nested(Navbar)
    modal = AboutModal(id='aboutModal')

    @property
    def is_displayed(self):
        return self.logged_in

    @property
    def logged_in(self):
        return self.navbar.is_displayed

    def log_out(self):
        """
        Log out the current user.
        """
        self.parent.navbar.usermenu.select_item("Logout")

    def get_detail(self, field):
        """
        Open the about modal and fetch the value for one of the fields
        Raises KeyError if the field isn't in the about modal
        :param field: string label for the detail field
        :return: string value from the requested field

        """
        self.navbar.modal.click()
        try:
            return self.modal.items()[field]
        except KeyError:
            raise KeyError('No field named {} found in "About" modal.'.format(field))
        finally:
            # close since its a blocking modal and will break further navigation
            self.modal.close()


class BaseClusterSpecifiedView(BaseLoggedInView):
    """
    Base view for pages where cluster is specified: Hosts, Volumes, Tasks, Events
    """
    vertical_navbar = View.nested(VerticalNavbar)
    cluster_name = Text(".//div[@class='nav contextselector-pf']/div/button/span")


class DeleteConfirmationView(View):
    """
    View for delete confirmation modal
    """
    ROOT = ".//pf-modal-overlay-content"
    alert_name = Text(".//h4")
    cancel = Button("Cancel")
    delete = Button("Delete")


class MySettingsView(View):
    """
    View for My Settings modal
    """
    ROOT = ".//div[@id='userSettingModal']"
    popup_name = Text(".//h4[@id='modalTitle']")
    users_name = TextInput(name="name")
    password = TextInput(name="password")
    confirm_password = TextInput(name="confirmPassword")
    email = TextInput(name="userEmail")
    notifications_on = Checkbox(
        locator=".//input[@ng-model='$ctrl.modalBodyScope.user.email_notifications']")
    save_button = Button("Save")
    cancel_button = Button("Cancel")

    @property
    def is_displayed(self):
        return self.popup_name.text == "My Settings"


class AlertsContainer(View):
    ROOT = ".//div[@ng-if='header.showAlerts']"
    container_name = Text(".//div[@class='alert-title text-center col-md-11']")

    @ParametrizedView.nested
    class alerts(ParametrizedView):
        PARAMETERS = ("alert_id",)
        ROOT = ParametrizedLocator("(.//div[@class='list-group-item'])"
                                   "[position() = {alert_id|quote}]")
        description = Text(".//p[@class='ng-binding']")
        date = Text(".//p[@class='ng-binding']/following-sibling::div")

        @classmethod
        def all(cls, browser):
            return [browser.text(e) for e in browser.elements(cls.ALL_VOLUMES)
                    if browser.text(e) is not None and browser.text(e) != '']

        @property
        def severity(self):
            return self.browser.elements(".//i[@data-toggle]")[0].get_attribute("title")

    ALL_ALERTS = ".//div[@class='list-group-item']"

    @property
    def all_alert_ids(self):
        """
        Returns the list of alerts.
        They will be used as XPATH indeces, so they should be strings and start with 1.
        """
        return [str(i + 1) for i in range(len(self.browser.elements(self.ALL_ALERTS)))]


class AlertsView(BaseLoggedInView):
    alerts = View.nested(AlertsContainer)

    @property
    def is_displayed(self):
        return self.alerts.container_name.text == "Alerts"
