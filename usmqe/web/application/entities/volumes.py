import attr
import pytest
import time
from navmazing import NavigateToAttribute

from usmqe.web.application.entities import BaseCollection, BaseEntity
from usmqe.web.application.implementations.web_ui import ViaWebUI, TendrlNavigateStep
from usmqe.web.application.views.grafana import GrafanaVolumeDashboard
from usmqe.web.application.views.volume import ClusterVolumesView
from usmqe.web.application.entities.bricks import VolumeBricksCollection
from usmqe.web.application.views.brick import VolumeBricksView


LOGGER = pytest.get_logger('volumes', module=True)


@attr.s
class Volume(BaseEntity):
    volname = attr.ib()
    # health = attr.ib()
    volume_type = attr.ib()
    bricks_count = attr.ib()
    running = attr.ib()
    rebalance = attr.ib()
    profiling = attr.ib()
    alerts = attr.ib()
    cluster_name = attr.ib()

    _collections = {'bricks': VolumeBricksCollection}

    @property
    def bricks(self):
        return self.collections.bricks

    def update(self):
        view = self.application.web_ui.create_view(ClusterVolumesView)
        self.bricks_count = view.volumes(self.volname).bricks.text
        self.running = view.volumes(self.volname).running.text
        self.rebalance = view.volumes(self.volname).rebalance.text
        self.profiling = view.volumes(self.volname).profiling.text
        self.alerts = view.volumes(self.volname).alerts.text

    def enable_profiling(self):
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

    def check_dashboard(self):
        view = ViaWebUI.navigate_to(self, "Dashboard")
        pytest.check(view.cluster_name.text == self.cluster_name)
        LOGGER.debug("Cluster name in grafana: {}".format(view.cluster_name.text))
        LOGGER.debug("Cluster name in main UI: {}".format(self.cluster_name))
        pytest.check(view.volume_name.text == self.volname)
        LOGGER.debug("Volume name in grafana: '{}'".format(view.volume_name))
        LOGGER.debug("Volume name in main UI: '{}'".format(self.volname))
        pytest.check(view.bricks_total.text.split(" ")[-1] == self.bricks_count)
        LOGGER.debug("Bricks count in grafana: {}".format(view.bricks_total.text.split(" ")[-1]))
        LOGGER.debug("Bricks count in main UI: {}".format(self.bricks_count))
        # TODO: check volume health
        view.browser.selenium.close()
        view.browser.selenium.switch_to.window(view.browser.selenium.window_handles[0])


@attr.s
class VolumesCollection(BaseCollection):
    ENTITY = Volume

    def get_all_volnames(self):
        view = self.application.web_ui.create_view(ClusterVolumesView)
        time.sleep(2)
        volume_names = view.all_volnames
        LOGGER.debug("Volume names are: {}".format(volume_names))
        return volume_names

    def get_volumes(self):
        view = ViaWebUI.navigate_to(self.parent, "Volumes")
        volumes_list = []
        for volname in self.get_all_volnames():
            volume = self.instantiate(
                volname,
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
    VIEW = GrafanaVolumeDashboard
    prerequisite = NavigateToAttribute("parent.parent", "Volumes")

    def step(self):
        time.sleep(1)
        self.parent.volumes(self.obj.volname).dashboard_button.click()
        time.sleep(1)
        self.view.browser.selenium.switch_to.window(self.view.browser.selenium.window_handles[1])
        time.sleep(1)


@ViaWebUI.register_destination_for(Volume, "Bricks")
class HostBricks(TendrlNavigateStep):
    VIEW = VolumeBricksView
    prerequisite = NavigateToAttribute("parent.parent", "Volumes")

    def step(self):
        time.sleep(1)
        self.parent.volumes(self.obj.volname).volname.click()
        time.sleep(4)
