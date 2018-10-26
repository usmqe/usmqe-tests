import attr
from navmazing import NavigateToAttribute

from usmqe.base.application.entities import BaseCollection, BaseEntity
from usmqe.base.application.views.user import UsersView
from usmqe.base.application.views.adduser import AddUserView
from usmqe.base.application.implementations.web_ui import TendrlNavigateStep, ViaWebUI


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
                row[6].widget.select("Delete User", close=False, handle_alert=not cancel)
                break

    @property
    def exists(self):
        view = ViaWebUI.navigate_to(self.parent, "All")
        return bool(list(view.users.rows(user_id=self.user_id)))


@attr.s
class UsersCollection(BaseCollection):
    ENTITY = User

    def create(self, user_id, name, email, notifications_on, password, role):
        view = ViaWebUI.navigate_to(self, "All")
        view.adduser.click()
        view = self.application.web_ui.create_view(AddUserView)
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


@ViaWebUI.register_destination_for(UsersCollection, "All")
class UsersAll(TendrlNavigateStep):
    VIEW = UsersView
    prerequisite = NavigateToAttribute("application.web_ui", "LoggedIn")

    def step(self):
        self.parent.navbar.usermanagement.select_item("Users")
