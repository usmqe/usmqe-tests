import attr
import pytest
import time
from navmazing import NavigateToAttribute

from usmqe.base.application.entities import BaseCollection, BaseEntity
from usmqe.base.application.implementations.web_ui import TendrlNavigateStep, ViaWebUI
from usmqe.base.application.views.host import ClusterHostsView, GrafanaHostDashboard
from usmqe.base.application.views.brick import HostBricksView
from usmqe.base.application.entities.bricks import HostBricksCollection

LOGGER = pytest.get_logger('hosts', module=True)


@attr.s
class Host(BaseEntity):
    hostname = attr.ib()
    gluster_version = attr.ib()
    managed = attr.ib()
    role = attr.ib()
    bricks_count = attr.ib()
    alerts = attr.ib()
    cluster_name = attr.ib()
    # add host status

    _collections = {'bricks': HostBricksCollection}

    @property
    def bricks(self):
        return self.collections.bricks

    def check_dashboard(self):
        view = ViaWebUI.navigate_to(self, "Dashboard")
        pytest.check(view.cluster_name == self.custer_name)
        pytest.check(view.host_name == self.hostname)
        pytest.check(view.bricks_total.split(" ")[-1] == self.bricks_count)
        # check host status


@attr.s
class HostsCollection(BaseCollection):
    ENTITY = Host

    def get_all_hostnames(self):
        view = self.application.web_ui.create_view(ClusterHostsView)
        return view.all_hostnames

    def get_hosts(self):
        view = ViaWebUI.navigate_to(self.parent, "Hosts")
        time.sleep(4)
        hosts_list = []
        for hostname in self.get_all_hostnames():
            host = self.instantiate(
                hostname,
                view.hosts(hostname).gluster_version.text,
                view.hosts(hostname).managed.text,
                view.hosts(hostname).role.text,
                view.hosts(hostname).bricks.text,
                view.hosts(hostname).alerts.text,
                view.cluster_name.text)
            hosts_list.append(host)
        return hosts_list


@ViaWebUI.register_destination_for(Host, "Dashboard")
class HostDashboard(TendrlNavigateStep):
    VIEW = GrafanaHostDashboard
    prerequisite = NavigateToAttribute("parent.parent", "Hosts")

    def step(self):
        time.sleep(1)
        self.parent.hosts(self.obj.hostname).dashboard_button.click()


@ViaWebUI.register_destination_for(Host, "Bricks")
class HostBricks(TendrlNavigateStep):
    VIEW = HostBricksView
    prerequisite = NavigateToAttribute("parent.parent", "Hosts")

    def step(self):
        time.sleep(1)
        self.parent.hosts(self.obj.hostname).host_name.click()
