from taretto.ui.core import TextInput, View
from taretto.ui.patternfly import Button


class LoginPage(View):
    username = TextInput(id="username")
    password = TextInput(id="password")
    log_in = Button("Log In")


class BaseLoggedInView(View):
    pass
