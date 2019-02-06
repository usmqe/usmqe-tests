import attr
import time

from usmqe.web.application.entities import BaseCollection, BaseEntity
from usmqe.web.application.implementations.web_ui import ViaWebUI
from usmqe.web.application.entities.bricks import VolumeBricksCollection
from usmqe.web.application.views.brick import VolumeBricksView


@attr.s
class VolumePart(BaseEntity):
    """
    Either replica set or subvolume.
    """
    part_id = attr.ib()
    part_name = attr.ib()
    volume_name = attr.ib()
    utilization = attr.ib()

    _collections = {'bricks': VolumeBricksCollection}

    @property
    def bricks(self):
        return self.collections.bricks

    @property
    def is_expanded(self):
        view = self.application.web_ui.create_view(VolumeBricksView)
        return view.volume_parts(self.part_id).is_expanded

    def expand_or_collapse(self):
        """
        Click on volume part name to expand or collapse detailed information on this part
        """
        view = self.application.web_ui.create_view(VolumeBricksView)
        view.volume_parts(self.part_id).part_name.click()
        time.sleep(1)


@attr.s
class VolumePartsCollection(BaseCollection):
    ENTITY = VolumePart

    def get_parts(self):
        view = ViaWebUI.navigate_to(self.parent, "Bricks")
        part_list = []
        assert view.all_part_ids != []
        for part_id in view.all_part_ids:
            part = self.instantiate(
                part_id,
                view.volume_parts(part_id).part_name.text,
                view.volume_name,
                view.volume_parts(part_id).utilization.text)
            part_list.append(part)
        return part_list

    def expand_all(self):
        view = self.application.web_ui.create_view(VolumeBricksView)
        view.expand_all.click()
        time.sleep(2)

    def collapse_all(self):
        view = self.application.web_ui.create_view(VolumeBricksView)
        view.collapse_all.click()
        time.sleep(2)
