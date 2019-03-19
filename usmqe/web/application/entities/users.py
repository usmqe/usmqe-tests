import attr
from navmazing import NavigateToAttribute, NavigateToSibling
from wait_for import wait_for

from usmqe.web.application.entities import BaseCollection, BaseEntity
from usmqe.web.application.views.user import UsersView
from usmqe.web.application.views.common import DeleteConfirmationView, MySettingsView
from usmqe.web.application.views.adduser import AddUserView
from usmqe.web.application.views.edituser import EditUserView
from usmqe.web.application.implementations.web_ui import TendrlNavigateStep, ViaWebUI


@attr.s
class User(BaseEntity):
    """
    User object.
    """
    user_id = attr.ib()
    name = attr.ib()
    email = attr.ib()
    notifications_on = attr.ib()
    password = attr.ib()
    role = attr.ib()

    def delete(self, cancel=False):
        """
        Delete the user by choosing 'Delete User' option of Actions kebab.
        """
        view = ViaWebUI.navigate_to(self.parent, "All")
        wait_for(lambda: view.is_displayed,
                 timeout=5,
                 message="Users page hasn't been displayed in time")
        for row in view.users:
            if row["User ID"].text == self.user_id:
                row[6].widget.select("Delete User", close=False)
                view = self.application.web_ui.create_view(DeleteConfirmationView)
                wait_for(lambda: view.is_displayed,
                         timeout=5,
                         message="DeleteConfirmationView hasn't been displayed in time")
                view.delete.click()
                # this is a UI bug
                view.browser.refresh()
                # view = ViaWebUI.navigate_to(self.parent, "All")
                break

    def edit(self, new_values_dict, cancel=False):
        """
        Edit user.
        """
        view = ViaWebUI.navigate_to(self.parent, "All")
        wait_for(lambda: view.is_displayed,
                 timeout=5,
                 message="Users page hasn't been displayed in time")
        for row in view.users:
            if row["User ID"].text == self.user_id:
                row[5].click()
                view = self.application.web_ui.create_view(EditUserView)
                wait_for(lambda: view.is_displayed,
                         timeout=5,
                         message="EditUserView hasn't been displayed in time")
                view.fill(new_values_dict)
                view.save_button.click()
                break
        for key, value in new_values_dict.items():
            setattr(self, key, value)

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
        wait_for(lambda: view.is_displayed,
                 timeout=5,
                 message="AddUserView hasn't been displayed in time")
        view.fill({
            "user_id": user_id,
            "name": name,
            "email": email,
            "notifications_on": notifications_on,
            "password": password,
            "confirm_password": password,
            "role": role
        })
        view.save_button.click()
        return self.instantiate(user_id, name, email, notifications_on, password, role)

    def edit_logged_in_user(self, new_values_dict):
        view = ViaWebUI.navigate_to(self, "MySettings")
        wait_for(lambda: view.is_displayed,
                 timeout=5,
                 message="MySettingsView hasn't been displayed in time")
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
