import attr
import pytest
import time
from navmazing import NavigateToAttribute

from usmqe.web.application.entities import BaseCollection, BaseEntity
from usmqe.web.application.implementations.web_ui import TendrlNavigateStep, ViaWebUI
from usmqe.web.application.views.host import ClusterHostsView
from usmqe.web.application.views.brick import HostBricksView
from usmqe.web.application.views.grafana import GrafanaHostDashboard
from usmqe.web.application.entities.bricks import HostBricksCollection

LOGGER = pytest.get_logger('hosts', module=True)


@attr.s
class Host(BaseEntity):
    hostname = attr.ib()
    health = attr.ib()
    gluster_version = attr.ib()
    managed = attr.ib()
    role = attr.ib()
    bricks_count = attr.ib()
    alerts = attr.ib()
    cluster_name = attr.ib()

    _collections = {'bricks': HostBricksCollection}

    @property
    def bricks(self):
        return self.collections.bricks

    def get_values_from_dashboard(self):
        """
        Click Dashboard button, read the selected data from Grafana dashboard,
        close the window with Grafana dashboard and return to main UI
        """
        view = ViaWebUI.navigate_to(self, "Dashboard")
        dashboard_values = {
            "cluster_name": view.cluster_name.text,
            "host_name": view.host_name.text,
            "brick_count": view.bricks_total.text.split(" ")[-1],
            "host_health": view.host_health.text.lower()}
        view.browser.selenium.close()
        view.browser.selenium.switch_to.window(view.browser.selenium.window_handles[0])
        return dashboard_values


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
                view.hosts(hostname).health,
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
        time.sleep(1)
        self.view.browser.selenium.switch_to.window(self.view.browser.selenium.window_handles[1])
        time.sleep(1)


@ViaWebUI.register_destination_for(Host, "Bricks")
class HostBricks(TendrlNavigateStep):
    VIEW = HostBricksView
    prerequisite = NavigateToAttribute("parent.parent", "Hosts")

    def step(self):
        time.sleep(1)
        self.parent.hosts(self.obj.hostname).host_name.click()
