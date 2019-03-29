import attr
import pytest
from navmazing import NavigateToAttribute
from wait_for import wait_for


from usmqe.web import tools
from usmqe.web.application.entities import BaseCollection, BaseEntity
from usmqe.web.application.implementations.web_ui import TendrlNavigateStep, ViaWebUI
from usmqe.web.application.views.brick import HostBricksView
from usmqe.web.application.views.grafana import GrafanaHostDashboard
from usmqe.web.application.entities.bricks import HostBricksCollection

LOGGER = pytest.get_logger('hosts', module=True)


@attr.s
class Host(BaseEntity):
    """
    Host object is an item of a Cluster's HostsCollection.
    Each host has its own collection of Bricks.
    """
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
        tools.close_extra_windows(view.browser)
        return dashboard_values


@attr.s
class HostsCollection(BaseCollection):
    ENTITY = Host

    def get_hosts(self):
        """
        Return the list of instantiated Host objects, their attributes read from Hosts page.
        """
        view = ViaWebUI.navigate_to(self.parent, "Hosts")
        wait_for(lambda: view.is_displayed,
                 timeout=10,
                 delay=3,
                 message="HostsView wasn't displayed\n" +
                 "Visible text: {}".format(view.browser.elements("*")[0].text))
        hosts_list = []
        for hostname in view.all_hostnames:
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
    """
    Navigate to each Host's grafana dashboard by clicking Dashboard button.
    """
    VIEW = GrafanaHostDashboard
    prerequisite = NavigateToAttribute("parent.parent", "Hosts")

    def step(self):
        self.parent.hosts(self.obj.hostname).dashboard_button.click()
        self.view.browser.selenium.switch_to.window(self.view.browser.selenium.window_handles[1])


@ViaWebUI.register_destination_for(Host, "Bricks")
class HostBricks(TendrlNavigateStep):
    """
    Navigate to each Host's list of bricks by clicking on host name.
    """
    VIEW = HostBricksView
    prerequisite = NavigateToAttribute("parent.parent", "Hosts")

    def step(self):
        self.parent.hosts(self.obj.hostname).host_name.click()
