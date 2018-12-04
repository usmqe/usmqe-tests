import attr
from navmazing import NavigateToAttribute, NavigateToSibling
# from wait_for import wait_for

from usmqe.base.application.entities import BaseCollection, BaseEntity
from usmqe.base.application.views.cluster import ClustersView
from usmqe.base.application.views.importcluster import ImportClusterView
from usmqe.base.application.implementations.web_ui import TendrlNavigateStep, ViaWebUI


@attr.s
class Cluster(BaseEntity):
    name = attr.ib()
    version = attr.ib()
    managed = attr.ib()
    # hosts_number = attr.ib()
    status = attr.ib()
    # attributes below are not defined until cluster is imported
    # volumes = attr.ib()
    # alerts = attr.ib()
    # profiling = attr.ib()

    # def import(self, cancel=False):
    #    pass
    # import will belong to an individual cluster when the widget is ready

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
        pass
        # view = ViaWebUI.navigate_to(self.parent, "All")
        # return bool(list(view.clusters.something(something)))


@attr.s
class ClustersCollection(BaseCollection):
    ENTITY = Cluster

    def cluster_import(self, cluster_name):
        view = ViaWebUI.navigate_to(self, "Import")
        view.fill({"cluster_name": cluster_name})
        view.save_button.click()
        return self.instantiate(cluster_name, "RHGS 3.4", "Yes", "Ready to Use")


@ViaWebUI.register_destination_for(ClustersCollection, "All")
class ClustersAll(TendrlNavigateStep):
    VIEW = ClustersView
    prerequisite = NavigateToAttribute("application.web_ui", "LoggedIn")

    def step(self):
        self.parent.navbar.clusters.select_item("All Clusters")


@ViaWebUI.register_destination_for(ClustersCollection, "Import")
class ClustersImport(TendrlNavigateStep):
    VIEW = ImportClusterView
    prerequisite = NavigateToSibling("All")

    def step(self):
        self.parent.import_button.click()
