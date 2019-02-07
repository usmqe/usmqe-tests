import attr
import time
import pytest
from navmazing import NavigateToAttribute

from usmqe.web.application.entities import BaseCollection, BaseEntity
from usmqe.web.application.implementations.web_ui import TendrlNavigateStep, ViaWebUI
from usmqe.web.application.views.grafana import GrafanaBrickDashboard
from usmqe.web.application.views.brick import HostBricksView

LOGGER = pytest.get_logger('hosts', module=True)


@attr.s
class Brick(BaseEntity):
    brick_path = attr.ib()
    hostname = attr.ib()
    volume_name = attr.ib()
    utilization = attr.ib()
    disk_device_path = attr.ib()
    port = attr.ib()
    cluster_name = attr.ib()

    @property
    def status(self):
        view = self.application.web_ui.create_view(HostBricksView)
        for row in view.bricks:
            if row["Brick Path"].text == self.brick_path:
                return row[0].browser.elements(".//span[contains(@class, 'pficon')"
                                               "]")[0].get_attribute("uib-tooltip")

    def get_values_from_dashboard(self):
        """
        Click Dashboard button, read the selected data from Grafana dashboard,
        close the window with Grafana dashboard and return to main UI
        """
        view = ViaWebUI.navigate_to(self, "Dashboard")
        dashboard_values = {
            "cluster_name": view.cluster_name.text,
            "host_name": view.host_name.text,
            "brick_path": view.path.text,
            "brick_status": view.status.text}
        view.browser.selenium.close()
        view.browser.selenium.switch_to.window(view.browser.selenium.window_handles[0])
        return dashboard_values


@attr.s
class HostBricksCollection(BaseCollection):
    ENTITY = Brick

    def get_bricks(self):
        view = ViaWebUI.navigate_to(self.parent, "Bricks")
        time.sleep(4)
        brick_list = []
        for row in view.bricks:
            brick = self.instantiate(
                row[0].text,
                view.hostname.text,
                row[1].text,
                row[2].text,
                row[3].text,
                row[4].text,
                view.cluster_name.text)
            brick_list.append(brick)
        return brick_list


@attr.s
class VolumeBricksCollection(BaseCollection):
    ENTITY = Brick

    def get_bricks(self):
        view = ViaWebUI.navigate_to(self.parent.parent.parent, "Bricks")
        if not self.parent.is_expanded:
            self.parent.expand_or_collapse()
        bricks = view.volume_parts(self.parent.part_id).bricks
        assert bricks != []
        brick_list = []
        for row in bricks:
            brick = self.instantiate(
                row[1].text,
                row[0].text,
                view.volume_name.text,
                row[2].text,
                row[3].text,
                row[4].text,
                view.cluster_name.text)
            brick_list.append(brick)
        return brick_list


@ViaWebUI.register_destination_for(Brick, "Dashboard")
class BrickDashboard(TendrlNavigateStep):
    VIEW = GrafanaBrickDashboard
    prerequisite = NavigateToAttribute("parent.parent", "Bricks")

    def step(self):
        time.sleep(1)
        for row in self.parent.bricks:
            if row["Brick Path"].text == self.obj.brick_path:
                row[5].click()
                break
        time.sleep(1)
        self.view.browser.selenium.switch_to.window(self.view.browser.selenium.window_handles[1])
        time.sleep(1)
