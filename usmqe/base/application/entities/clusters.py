import attr
import time
from navmazing import NavigateToAttribute
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
    hosts_number = attr.ib()
    status = attr.ib()
    # attributes below are not defined until cluster is imported
    # volumes = attr.ib()
    # alerts = attr.ib()
    # profiling = attr.ib()

    def cluster_import(self, cluster_name=None):
        view = ViaWebUI.navigate_to(self, "Import")
        if cluster_name is not None:
            view.fill({"cluster_name": cluster_name})
            self.name = cluster_name
        view.confirm_import.click()
        # TODO: update cluster attributes

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


@attr.s
class ClustersCollection(BaseCollection):
    ENTITY = Cluster

    def get_all_cluster_ids(self):
        view = ViaWebUI.navigate_to(self, "All")
        return view.all_ids

    def get_clusters(self):
        view = ViaWebUI.navigate_to(self, "All")
        clusters_list = []
        for cluster_id in self.get_all_cluster_ids():
            cluster = self.instantiate(
                cluster_id,
                view.clusters(cluster_id).cluster_version.text,
                view.clusters(cluster_id).managed.text,
                view.clusters(cluster_id).hosts.text,
                view.clusters(cluster_id).status.text)
            clusters_list.append(cluster)
        return clusters_list


@ViaWebUI.register_destination_for(ClustersCollection, "All")
class ClustersAll(TendrlNavigateStep):
    VIEW = ClustersView
    prerequisite = NavigateToAttribute("application.web_ui", "LoggedIn")

    def step(self):
        time.sleep(1)
        self.parent.navbar.clusters.select_item("All Clusters")


@ViaWebUI.register_destination_for(Cluster, "Import")
class ClusterImport(TendrlNavigateStep):
    VIEW = ImportClusterView
    prerequisite = NavigateToAttribute("parent", "All")

    def step(self):
        time.sleep(1)
        self.parent.clusters(self.obj.name).import_button.click()
