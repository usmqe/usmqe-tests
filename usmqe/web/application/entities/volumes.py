import attr
import pytest
import time
from navmazing import NavigateToAttribute

from usmqe.web.application.entities import BaseCollection, BaseEntity
from usmqe.web.application.implementations.web_ui import ViaWebUI, TendrlNavigateStep
from usmqe.web.application.views.grafana import GrafanaVolumeDashboard
from usmqe.web.application.views.volume import ClusterVolumesView
from usmqe.web.application.views.brick import VolumeBricksView
from usmqe.web.application.entities.volume_parts import VolumePartsCollection

LOGGER = pytest.get_logger('volumes', module=True)


@attr.s
class Volume(BaseEntity):
    """
    Volume object is an item of a Cluster's VolumesCollection.
    Each volume has its collection of VolumeParts that can be either replica sets or subvolumes.
    """
    volname = attr.ib()
    health = attr.ib()
    volume_type = attr.ib()
    bricks_count = attr.ib()
    running = attr.ib()
    rebalance = attr.ib()
    profiling = attr.ib()
    alerts = attr.ib()
    cluster_name = attr.ib()

    _collections = {'parts': VolumePartsCollection}

    @property
    def parts(self):
        return self.collections.parts

    def update(self):
        """
        Update volume attributes by reading them form Volumes page
        """
        view = self.application.web_ui.create_view(ClusterVolumesView)
        self.health = view.volumes(self.volname).health
        self.bricks_count = view.volumes(self.volname).bricks.text
        self.running = view.volumes(self.volname).running.text
        self.rebalance = view.volumes(self.volname).rebalance.text
        self.profiling = view.volumes(self.volname).profiling.text
        self.alerts = view.volumes(self.volname).alerts.text

    def enable_profiling(self):
        """
        Click Enable Profiling button and wait for Volume Profiling attribute to change to Enabled
        """
        view = self.application.web_ui.create_view(ClusterVolumesView)
        view.volumes(self.volname).enable_profiling.click()
        time.sleep(40)
        for _ in range(40):
            self.update()
            if self.profiling == "Enabled":
                break
            else:
                time.sleep(5)
        LOGGER.debug("Volume {} profiling value: {}".format(self.volname, self.profiling))
        pytest.check(self.profiling == "Enabled")

    def disable_profiling(self):
        """
        Click Disable Profiling button and wait for Volume Profiling to change to Disabled
        """
        view = self.application.web_ui.create_view(ClusterVolumesView)
        view.volumes(self.volname).disable_profiling.click()
        time.sleep(40)
        for _ in range(40):
            self.update()
            if self.profiling == "Disabled":
                break
            else:
                time.sleep(5)
        LOGGER.debug("Volume {} profiling value: {}".format(self.volname, self.profiling))
        pytest.check(self.profiling == "Disabled")

    def get_values_from_dashboard(self):
        """
        Click Dashboard button, read the selected data from Grafana dashboard,
        close the window with Grafana dashboard and return to main UI
        """
        view = ViaWebUI.navigate_to(self, "Dashboard")
        time.sleep(10)
        dashboard_values = {
            "cluster_name": view.cluster_name.text,
            "volume_name": view.volume_name.text,
            "brick_count": view.bricks_total.text.split(" ")[-1],
            "volume_health": view.volume_health.text}
        view.browser.selenium.close()
        view.browser.selenium.switch_to.window(view.browser.selenium.window_handles[0])
        return dashboard_values


@attr.s
class VolumesCollection(BaseCollection):
    ENTITY = Volume

    def get_all_volnames(self):
        """
        Return the list of all volume names of this collection.
        """
        view = self.application.web_ui.create_view(ClusterVolumesView)
        time.sleep(2)
        volume_names = view.all_volnames
        LOGGER.debug("Volume names are: {}".format(volume_names))
        return volume_names

    def get_volumes(self):
        """
        Return the list of instantiated Volume objects, their attributes read from Volumes page.
        """
        view = ViaWebUI.navigate_to(self.parent, "Volumes")
        volumes_list = []
        for volname in self.get_all_volnames():
            volume = self.instantiate(
                volname,
                view.volumes(volname).health,
                view.volumes(volname).volume_type.text,
                view.volumes(volname).bricks.text,
                view.volumes(volname).running.text,
                view.volumes(volname).rebalance.text,
                view.volumes(volname).profiling.text,
                view.volumes(volname).alerts.text,
                view.cluster_name.text)
            volumes_list.append(volume)
        return volumes_list


@ViaWebUI.register_destination_for(Volume, "Dashboard")
class VolumeDashboard(TendrlNavigateStep):
    """
    Navigate to each Volume's grafana dashboard by clicking Dashboard button.
    """
    VIEW = GrafanaVolumeDashboard
    prerequisite = NavigateToAttribute("parent.parent", "Volumes")

    def step(self):
        time.sleep(1)
        self.parent.volumes(self.obj.volname).dashboard_button.click()
        time.sleep(3)
        self.view.browser.selenium.switch_to.window(self.view.browser.selenium.window_handles[1])
        time.sleep(3)


@ViaWebUI.register_destination_for(Volume, "Bricks")
class VolumeBricks(TendrlNavigateStep):
    """
    Navigate to each Volumes's list of subvolumes/replica sets and bricks
    by clicking on volume name.
    """
    VIEW = VolumeBricksView
    prerequisite = NavigateToAttribute("parent.parent", "Volumes")

    def step(self):
        time.sleep(1)
        self.parent.volumes(self.obj.volname).volname.click()
        time.sleep(4)
