import attr
import pytest
from navmazing import NavigateToAttribute
from wait_for import wait_for

from usmqe.base.application.entities import BaseCollection, BaseEntity
from usmqe.base.application.views.user import UsersView
from usmqe.base.application.views.adduser import AddUserView
from usmqe.base.application.implementations.web_ui import TendrlNavigateStep, ViaWebUI

LOGGER = pytest.get_logger('ui_users_testing', module=True)


@attr.s
class User(BaseEntity):
    user_id = attr.ib()
    name = attr.ib()
    email = attr.ib()
    notifications_on = attr.ib()
    password = attr.ib()
    role = attr.ib()


    def delete(self):
        view = ViaWebUI.navigate_to(UsersCollection, "All")
        wait_for(lambda: view.is_displayed, timeout=5)
        for row in view.users:
            LOGGER.debug("Current User ID: ".format(row[0]))
            if row[0] == self.user_id:
                row["6"].select("Delete User", close=False)
                wait_for(lambda: view.is_displayed, timeout=5)


@attr.s
class UsersCollection(BaseCollection):
    ENTITY = User

    def adduser(self, user_id, name, email, notifications_on, password, role):
        view = ViaWebUI.navigate_to(self, "All")
        wait_for(lambda: view.is_displayed, timeout=5)
        view.adduser.click()
        view = self.application.web_ui.create_view(AddUserView)
        changed = view.fill({"user_id": user_id,
                             "users_name": name,
                             "email": email,
                             "notifications_on": notifications_on,
                             "password": password,
                             "confirm_password": password,
                             "role": role})
        view.save_button.click()
        user = self.instantiate(user_id, name, email, notifications_on, password, role)
        return user


@ViaWebUI.register_destination_for(UsersCollection, "All")
class UsersAll(TendrlNavigateStep):
    VIEW = UsersView
    prerequisite = NavigateToAttribute("application.web_ui", "LoggedIn")

    def step(self):
        self.parent.navbar.usermanagement.select_item("Users")
