import attr
from navmazing import NavigateToAttribute, NavigateToSibling
from wait_for import wait_for

from usmqe.base.application.entities import BaseCollection, BaseEntity
from usmqe.base.application.views.user import UsersView
from usmqe.base.application.views.common import DeleteConfirmationView
from usmqe.base.application.views.adduser import AddUserView
from usmqe.base.application.views.edituser import EditUserView
from usmqe.base.application.implementations.web_ui import TendrlNavigateStep, ViaWebUI


@attr.s
class Cluster(BaseEntity):
    name = attr.ib()
    version = attr.ib()
    managed = attr.ib()
    hosts = attr.ib()
    status = attr.ib()
    # attributes below are not defined until cluster is imported
    volumes = attr.ib()
    alerts = attr.ib()
    profiling = attr.ib()


    def import(self, cancel=False):
        pass


    def unmanage(self, cancel=False):
        pass


    def enable_profiling(self, cancel=False):
        pass


    def disable_profiling(self, cancel=False):
        pass


    def expand(self, cancel=False):
        pass

    @property
    def exists(self):
        view = ViaWebUI.navigate_to(self.parent, "All")
        #return bool(list(view.clusters.something(something)))


@attr.s
class ClustersCollection(BaseCollection):
    ENTITY = Cluster


@ViaWebUI.register_destination_for(UsersCollection, "All")
class UsersAll(TendrlNavigateStep):
    VIEW = ClustersView
    prerequisite = NavigateToAttribute("application.web_ui", "LoggedIn")

    def step(self):
        self.parent.navbar.clusters.select_item("All Clusters")
