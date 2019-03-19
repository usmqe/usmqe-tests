import attr
import pytest
from navmazing import NavigateToAttribute
from wait_for import wait_for

from usmqe.web.application.entities import BaseCollection, BaseEntity
from usmqe.web.application.implementations.web_ui import ViaWebUI, TendrlNavigateStep
from usmqe.web.application.views.grafana import GrafanaVolumeDashboard
from usmqe.web.application.views.volume import ClusterVolumesView
from usmqe.web.application.views.brick import VolumeBricksView
from usmqe.web.application.entities.volume_parts import VolumePartsCollection
from usmqe.web import tools

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
        return (self.health,
                self.bricks_count,
                self.running,
                self.rebalance,
                self.profiling,
                self.alerts)

    def enable_profiling(self):
        """
        Click Enable Profiling button and wait for Volume Profiling attribute to change to Enabled
        """
        view = self.application.web_ui.create_view(ClusterVolumesView)
        view.volumes(self.volname).enable_profiling.click()
        wait_for(lambda: self.update()[4] == "Enabled",
                 timeout=300,
                 delay=5,
                 message="Volume's profiling hasn't changed to Enabled in 300 seconds")
        LOGGER.debug("Volume {} profiling value: {}".format(self.volname, self.profiling))
        pytest.check(self.profiling == "Enabled")

    def disable_profiling(self):
        """
        Click Disable Profiling button and wait for Volume Profiling to change to Disabled
        """
        view = self.application.web_ui.create_view(ClusterVolumesView)
        view.volumes(self.volname).disable_profiling.click()
        wait_for(lambda: self.update()[4] == "Disabled",
                 timeout=300,
                 delay=5,
                 message="Volume's profiling hasn't changed to Enabled in 300 seconds")
        LOGGER.debug("Volume {} profiling value: {}".format(self.volname, self.profiling))
        pytest.check(self.profiling == "Disabled")

    def get_values_from_dashboard(self):
        """
        Click Dashboard button, read the selected data from Grafana dashboard,
        close the window with Grafana dashboard and return to main UI
        """
        view = ViaWebUI.navigate_to(self, "Dashboard")
        wait_for(lambda: view.is_displayed,
                 timeout=10,
                 delay=3,
                 message="Volume Dashboard wasn't displayed in time")
        dashboard_values = {
            "cluster_name": view.cluster_name.text,
            "volume_name": view.volume_name.text,
            "brick_count": view.bricks_total.text.split(" ")[-1],
            "volume_health": view.volume_health.text}
        tools.close_extra_windows(view)
        return dashboard_values


@attr.s
class VolumesCollection(BaseCollection):
    ENTITY = Volume

    def get_volumes(self):
        """
        Return the list of instantiated Volume objects, their attributes read from Volumes page.
        """
        view = ViaWebUI.navigate_to(self.parent, "Volumes")
        volumes_list = []
        LOGGER.debug("Volume names are: {}".format(view.all_volnames))
        for volname in view.all_volnames:
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
        self.parent.volumes(self.obj.volname).dashboard_button.click()
        self.view.browser.selenium.switch_to.window(self.view.browser.selenium.window_handles[1])


@ViaWebUI.register_destination_for(Volume, "Bricks")
class VolumeBricks(TendrlNavigateStep):
    """
    Navigate to each Volumes's list of subvolumes/replica sets and bricks
    by clicking on volume name.
    """
    VIEW = VolumeBricksView
    prerequisite = NavigateToAttribute("parent.parent", "Volumes")

    def step(self):
        self.parent.volumes(self.obj.volname).volname.click()
