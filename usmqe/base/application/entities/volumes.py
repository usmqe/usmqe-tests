import attr
import pytest
import time

from usmqe.base.application.entities import BaseCollection, BaseEntity
from usmqe.base.application.implementations.web_ui import ViaWebUI

from usmqe.base.application.views.volume import ClusterVolumesView


LOGGER = pytest.get_logger('volumes', module=True)


@attr.s
class Volume(BaseEntity):
    volname = attr.ib()
    # add status
    volume_type = attr.ib()
    bricks_count = attr.ib()
    running = attr.ib()
    rebalance = attr.ib()
    profiling = attr.ib()
    alerts = attr.ib()
    cluster_name = attr.ib()

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
        pass


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
