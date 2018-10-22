import attr
from navmazing import NavigateToAttribute

from usmqe.base.application.entities import BaseCollection, BaseEntity
from usmqe.base.application.views.user import UsersView
from usmqe.base.application.implementations.web_ui import TendrlNavigateStep, ViaWebUI


@attr.s
class User(BaseEntity):
    pass


@attr.s
class UsersCollection(BaseCollection):
    ENTITY = User


@ViaWebUI.register_destination_for(UsersCollection, "All")
class UsersAll(TendrlNavigateStep):
    VIEW = UsersView
    prerequisite = NavigateToAttribute("application.web_ui", "LoggedIn")

    def step(self):
        self.parent.navbar.usermanagement.select_item("Users")
