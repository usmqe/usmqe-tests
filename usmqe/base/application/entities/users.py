import attr
from navmazing import NavigateToAttribute, NavigateToSibling
from wait_for import wait_for

from usmqe.base.application.entities import BaseCollection, BaseEntity
from usmqe.base.application.views.user import UsersView
from usmqe.base.application.views.common import DeleteConfirmationView, MySettingsView
from usmqe.base.application.views.adduser import AddUserView
from usmqe.base.application.views.edituser import EditUserView
from usmqe.base.application.implementations.web_ui import TendrlNavigateStep, ViaWebUI
from usmqe.base.application.implementations.web_ui import ViaWebUI


@attr.s
class User(BaseEntity):
    user_id = attr.ib()
    name = attr.ib()
    email = attr.ib()
    notifications_on = attr.ib()
    password = attr.ib()
    role = attr.ib()

    def delete(self, cancel=False):
        view = ViaWebUI.navigate_to(self.parent, "All")
        for row in view.users:
            if row["User ID"].text == self.user_id:
                row[6].widget.select("Delete User", close=False)
                view = self.application.web_ui.create_view(DeleteConfirmationView)
                wait_for(lambda: view.is_displayed, timeout=3)
                view.delete.click()
                # TODO this is a UI bug
                view.browser.refresh()
                #view = ViaWebUI.navigate_to(self.parent, "All")
                break

    def edit(self, new_values_dict, cancel=False):
        view = ViaWebUI.navigate_to(self.parent, "All")
        for row in view.users:
            if row["User ID"].text == self.user_id:
                row[5].click()
                view = self.application.web_ui.create_view(EditUserView)
                view.fill(new_values_dict)
                view.save_button.click()
                break

    @property
    def exists(self):
        view = ViaWebUI.navigate_to(self.parent, "All")
        return bool(list(view.users.rows(user_id=self.user_id, 
                                         name=self.name,
                                         email=self.email,
                                         # can't use role=self.role
                                         # it's 'Read-Only' instead of 'Limited' in the table
                                         )))


@attr.s
class UsersCollection(BaseCollection):
    ENTITY = User

    def create(self, user_id, name, email, notifications_on, password, role):
        view = ViaWebUI.navigate_to(self, "Add")
        view.fill({
            "user_id": user_id,
            "users_name": name,
            "email": email,
            "notifications_on": notifications_on,
            "password": password,
            "confirm_password": password,
            "role": role
        })
        view.save_button.click()
        return self.instantiate(user_id, name, email, notifications_on, password, role)

    def edit_logged_in_user(self, 
                            user_id, new_values_dict):
        view = ViaWebUI.navigate_to(self, "MySettings")
        view.fill(new_values_dict)
        view.save_button.click()


@ViaWebUI.register_destination_for(UsersCollection, "All")
class UsersAll(TendrlNavigateStep):
    VIEW = UsersView
    prerequisite = NavigateToAttribute("application.web_ui", "LoggedIn")

    def step(self):
        self.parent.navbar.usermanagement.select_item("Users")


@ViaWebUI.register_destination_for(UsersCollection, "Add")
class UsersAdd(TendrlNavigateStep):
    VIEW = AddUserView
    prerequisite = NavigateToSibling("All")

    def step(self):
        self.parent.adduser.click()


@ViaWebUI.register_destination_for(UsersCollection, "MySettings")
class UsersSettings(TendrlNavigateStep):
    VIEW = MySettingsView
    prerequisite = NavigateToAttribute("application.web_ui", "LoggedIn")

    def step(self):
        self.parent.navbar.usermenu.select_item("My Settings")
