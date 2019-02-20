import attr
import time
import pytest
from navmazing import NavigateToAttribute

from usmqe.web.application.entities import BaseCollection, BaseEntity
from usmqe.web.application.implementations.web_ui import TendrlNavigateStep, ViaWebUI
from usmqe.web.application.views.grafana import GrafanaBrickDashboard
from usmqe.web.application.views.brick import HostBricksView
from usmqe.web.application.views.brick import VolumeBricksView

LOGGER = pytest.get_logger('bricks', module=True)


@attr.s
class Brick(BaseEntity):
    """
    Base Brick object for bricks that are part of HostBricksCollection or VolumeBricksCollection.
    """
    brick_path = attr.ib()
    hostname = attr.ib()
    volume_name = attr.ib()
    utilization = attr.ib()
    disk_device_path = attr.ib()
    port = attr.ib()
    cluster_name = attr.ib()

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
class HostBrick(Brick):
    """
    Brick object that is part of HostBricksCollection.
    """
    @property
    def status(self):
        """
        Return 'uib-tooltip' attribute of Brick's status icon.
        It should be either 'Started' or 'Stopped'.
        """
        view = self.application.web_ui.create_view(HostBricksView)
        time.sleep(1)
        for row in view.bricks:
            if row["Brick Path"].text == self.brick_path:
                return row[0].browser.elements(".//span[@uib-tooltip"
                                               "]")[0].get_attribute("uib-tooltip")


@attr.s
class HostBricksCollection(BaseCollection):
    ENTITY = HostBrick

    def get_bricks(self):
        """
        Navigate to Host's Brick list by clicking on hostname.
        Return the list of initiated Brick objects.
        """
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
class VolumeBrick(Brick):
    """
    Brick object that is part of VolumeBricksCollection.
    """
    part_id = attr.ib()

    @property
    def status(self):
        """
        Return 'uib-tooltip' attribute of Brick's status icon.
        It should be either 'Started' or 'Stopped'.
        """
        view = self.application.web_ui.create_view(VolumeBricksView)
        time.sleep(1)
        if not view.volume_parts(self.part_id).is_expanded:
            view.volume_parts(self.part_id).expand()
        time.sleep(1)
        for row in view.volume_parts(self.part_id).bricks:
            if (row["Brick Path"].text == self.brick_path and
                    row["Host Name"].text == self.hostname):
                return row[1].browser.elements(".//span[@uib-tooltip"
                                               "]")[0].get_attribute("uib-tooltip")


@attr.s
class VolumeBricksCollection(BaseCollection):
    """
    Collection of Volume's Bricks.
    """
    ENTITY = VolumeBrick

    def get_bricks(self):
        """
        Navigate to Volume's Brick list by clicking on volume name.
        Return the list of initiated Brick objects.
        """
        view = ViaWebUI.navigate_to(self.parent.parent.parent, "Bricks")
        if not self.parent.is_expanded:
            self.parent.expand_or_collapse()
        bricks = view.volume_parts(self.parent.part_id).bricks
        brick_list = []
        for row in bricks:
            brick = self.instantiate(
                row[1].text,
                row[0].text,
                view.volume_name.text,
                row[2].text,
                row[3].text,
                row[4].text,
                view.cluster_name.text,
                self.parent.part_id)
            brick_list.append(brick)
        return brick_list


@ViaWebUI.register_destination_for(HostBrick, "Dashboard")
class BrickDashboard(TendrlNavigateStep):
    """
    Navigate to each Host Brick's grafana dashboard by clicking Dashboard button.
    """
    VIEW = GrafanaBrickDashboard
    prerequisite = NavigateToAttribute("parent.parent", "Bricks")

    def step(self):
        time.sleep(1)
        for row in self.parent.bricks:
            if row["Brick Path"].text == self.obj.brick_path:
                row[5].click()
                break
        time.sleep(3)
        self.view.browser.selenium.switch_to.window(self.view.browser.selenium.window_handles[1])
        time.sleep(3)


@ViaWebUI.register_destination_for(VolumeBrick, "Dashboard")
class VolumeBrickDashboard(TendrlNavigateStep):
    """
    Navigate to each Volume Brick's grafana dashboard by clicking Dashboard button.
    """
    VIEW = GrafanaBrickDashboard
    prerequisite = NavigateToAttribute("parent.parent.parent.parent", "Bricks")

    def step(self):
        time.sleep(1)
        self.parent.expand_all.click()
        time.sleep(1)
        for row in self.parent.volume_parts(self.obj.part_id).bricks.rows():
            if (row["Brick Path"].text == self.obj.brick_path and
                    row["Host Name"].text == self.obj.hostname):
                row[5].click()
                break
        time.sleep(3)
        self.view.browser.selenium.switch_to.window(self.view.browser.selenium.window_handles[1])
        time.sleep(3)
