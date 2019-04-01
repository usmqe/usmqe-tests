import atexit

from cached_property import cached_property
from datetime import datetime
from selenium.common.exceptions import NoSuchElementException
from taretto.navigate import Navigate, NavigateStep, NavigateToSibling
from taretto.ui import Browser
from webdriver_kaifuku import BrowserManager
from wait_for import wait_for, TimedOutError
from navmazing import NavigationTriesExceeded

from usmqe.web.application.implementations import TendrlImplementationContext, Implementation
from usmqe.web.application.views.common import BaseLoggedInView, LoginPage


class TendrlNavigateStep(NavigateStep):
    VIEW = None

    @cached_property
    def view(self):
        if self.VIEW is None:
            raise AttributeError(
                "{} does not have VIEW specified".format(type(self).__name__)
            )
        return self.create_view(self.VIEW, additional_context={"object": self.obj})

    @property
    def application(self):
        return self.obj.application

    def create_view(self, *args, **kwargs):
        return self.application.web_ui.create_view(*args, **kwargs)

    def am_i_here(self):
        try:
            return self.view.is_displayed
        except (AttributeError, NoSuchElementException):
            return False

    def check_for_badness(self, fn, _tries, nav_args, *args, **kwargs):
        go_kwargs = kwargs.copy()
        go_kwargs.update(nav_args)
        self.log_message(
            "Invoking {}, with {} and {}".format(fn.__name__, args, kwargs),
            level="debug",
        )

        try:
            return fn(*args, **kwargs)
        except Exception as e:
            self.log_message(e)
            self.go(_tries, *args, **go_kwargs)

    def go(self, _tries=3, *args, **kwargs):
        """Wrapper around :meth:`navmazing.NavigateStep.go` which returns
        instance of view after successful navigation flow.
        :return: view instance if class attribute ``VIEW`` is set or ``None``
            otherwise
        """
        try:
            super(TendrlNavigateStep, self).go(_tries=_tries, *args, **kwargs)
        except NavigationTriesExceeded:
            now = datetime.strftime(datetime.now(), "%y_%m_%d_%H:%M")
            self.view.browser.selenium.get_screenshot_as_file("screenshots/pre_nav" + now + ".png")
            raise NavigationTriesExceeded(self.view)
        view = self.view if self.VIEW is not None else None
        if view:
            try:
                wait_for(
                    self.am_i_here, num_sec=10,
                    message="Waiting for view [{}] to display".format(view.__class__.__name__)
                )
            except TimedOutError:
                now = datetime.strftime(datetime.now(), "%y_%m_%d_%H:%M")
                view.browser.selenium.get_screenshot_as_file("screenshots/step" + now + ".png")
                raise TimedOutError
        return view


class ViaWebUI(Implementation):
    """UI implementation using the normal ux"""

    navigator = Navigate()
    navigate_to = navigator.navigate
    register_destination_for = navigator.register
    register_method_for = TendrlImplementationContext.external_for
    name = "ViaWebUI"

    def __init__(self, owner):
        super(ViaWebUI, self).__init__(owner)
        self.browser_manager = BrowserManager.from_conf({
            "webdriver": "Chrome"
        })

    def create_view(self, view_class, additional_context=None):
        """Method that is used to instantiate a Widgetastic View.
        Views may define ``LOCATION`` on them, that implies a :py:meth:`force_navigate` call with
        ``LOCATION`` as parameter.
        Args:
            view_class: A view class, subclass of ``widgetastic.widget.View``
            additional_context: Additional informations passed to the view (user name, VM name, ...)
                which is also passed to the :py:meth:`force_navigate` in case when navigation is
                requested.
        Returns:
            An instance of the ``view_class``
        """
        additional_context = additional_context or {}
        view = view_class(self.widgetastic_browser, additional_context=additional_context)
        return view

    def _reset_cache(self):
        try:
            del self.widgetastic_browser
        except AttributeError:
            pass

    @cached_property
    def widgetastic_browser(self):
        """This gives us a widgetastic browser."""
        selenium_browser = self.browser_manager.ensure_open()
        selenium_browser.get(self.application.address)
        self.browser_manager.add_cleanup(self._reset_cache)
        atexit.register(self.browser_manager.quit)
        return Browser(selenium_browser)

    def open_login_page(self):
        self.widgetastic_browser.url = self.application.address

    def do_login(self, view):
        view.fill({
            "username": self.application.username,
            "password": self.application.password,
        })
        view.log_in.click()

    def logout(self, view):
        view.navbar.usermenu.select_item("Logout")


@ViaWebUI.register_destination_for(ViaWebUI)
class LoginScreen(TendrlNavigateStep):
    VIEW = LoginPage

    def step(self):
        self.obj.open_login_page()


@ViaWebUI.register_destination_for(ViaWebUI)
class LoggedIn(TendrlNavigateStep):
    VIEW = BaseLoggedInView
    prerequisite = NavigateToSibling("LoginScreen")

    def step(self):
        self.obj.do_login(self.parent)
