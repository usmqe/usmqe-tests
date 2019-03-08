import attr
from wait_for import wait_for

from usmqe.web.application.entities import BaseCollection, BaseEntity
from usmqe.web.application.implementations.web_ui import ViaWebUI
from usmqe.web.application.entities.bricks import VolumeBricksCollection
from usmqe.web.application.views.brick import VolumeBricksView
from usmqe.web import tools


@attr.s
class VolumePart(BaseEntity):
    """
    Either replica set or subvolume.
    Each Volume Part has its own collection of Bricks.
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
        return (view.volume_parts(self.part_id).is_expanded and
                tools.bricks_displayed(view, self.parent.parent.bricks_count, self.part_id))

    def expand(self):
        """
        Click on volume part name to expand this part's list of bricks
        """
        view = self.application.web_ui.create_view(VolumeBricksView)
        view.volume_parts(self.part_id).part_name.click()
        wait_for(lambda: self.is_expanded, timeout=3)

    def collapse(self):
        """
        Click on volume part name to collapse this part's list of bricks
        """
        view = self.application.web_ui.create_view(VolumeBricksView)
        view.volume_parts(self.part_id).part_name.click()
        wait_for(lambda: (not self.is_expanded), timeout=3)


@attr.s
class VolumePartsCollection(BaseCollection):
    ENTITY = VolumePart

    def get_parts(self):
        """
        Return the list of all Volume Part objects, their attributes read from the Volume's
        Brick details page.
        """
        view = ViaWebUI.navigate_to(self.parent, "Bricks")
        wait_for(lambda: view.is_displayed, timeout=10, delay=2)
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

    @property
    def is_expanded(self):
        for part in self.get_parts():
            if not part.is_expanded:
                return False
        return True

    @property
    def is_collapsed(self):
        for part in self.get_parts():
            if part.is_expanded:
                return False
        return True

    def expand_all(self):
        """
        Expand all lists of bricks by clicking "Expand All" link
        """
        view = self.application.web_ui.create_view(VolumeBricksView)
        view.expand_all.click()
        wait_for(lambda: self.is_expanded, timeout=3)

    def collapse_all(self):
        """
        Collapse all lists of bricks by clicking "Collapse All" link
        """
        view = self.application.web_ui.create_view(VolumeBricksView)
        view.browser.selenium.execute_script("window.scrollTo(0, -document.body.scrollHeight)")
        view.collapse_all.click()
        wait_for(lambda: self.is_collapsed, timeout=3)
