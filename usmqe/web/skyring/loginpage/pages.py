"""
Login page abstraction.
"""


from webstr.core import WebstrPage
from webstr.selenium.ui.support import WaitForWebstrPage

from usmqe.web.skyring.mainpage.navpage import pages as navpage
from usmqe.web.skyring.loginpage import models as m_loginpage


class LoginPage(WebstrPage):
    """
    Base page object for login page.

    Parameters:
        _model - page model
        _label - a read-able description of a class
        _required_elems - web elements to be checked
    """
# not working during import the usm_web_url does not exist
#    _location = pytest.config.getini("usm_web_url")
    _model = m_loginpage.LoginPageModel
    _label = 'login page'
    _required_elems = ['username', 'password', 'login_btn']

    def __init__(self, driver, location):
        """ init
        Note: _location has to be initialized here as it needs
            a config parameter which is not know before the actual run
            _location - initial URL to load upon instance creation

        Atributes:
            driver: web driver
            location: web URL
        """
        self._location = location
        super(self.__class__, self).__init__(driver)

    def fill_form_values(self, username, password):
        """
        Fill in the login form and submit.

        Parameters:
            username - username
            password - password

        Return:
            True - success
        """
        self._model.username.value = username
        self._model.password.value = password
        return True

    def login_user(self, username, password):
        """
        Login user - fill in the login form and wait for home page.

        Parameters:
            username - username
            password - password

        Return: <navpage.NavMenu instance>
        """
        self.fill_form_values(username=username, password=password)
        self._model.login_btn.click()
        # TODO https://github.com/skyrings/kitoon/issues/93
        WaitForWebstrPage(self, 10).to_disappear()
        return navpage.NavMenuBars(self.driver)
