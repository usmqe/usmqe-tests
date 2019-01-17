import attr
import pytest
import time

from usmqe.base.application.entities import BaseCollection, BaseEntity
from usmqe.base.application.implementations.web_ui import ViaWebUI

from usmqe.base.application.views.task import ClusterTasksView


LOGGER = pytest.get_logger('volumes', module=True)


@attr.s
class Task(BaseEntity):
    task_id = attr.ib()
    task_name = attr.ib()
    submitted_date = attr.ib()
    status = attr.ib()
    changed_date = attr.ib()
    cluster_name = attr.ib()


@attr.s
class TasksCollection(BaseCollection):
    ENTITY = Task

    def get_all_task_ids(self):
        view = self.application.web_ui.create_view(ClusterTasksView)
        return view.all_task_ids

    def get_tasks(self):
        view = ViaWebUI.navigate_to(self.parent, "Tasks")
        task_list = []
        time.sleep(2)
        for task_id in self.get_all_task_ids():
            task = self.instantiate(
                task_id,
                view.tasks(task_id).task_name.text,
                view.tasks(task_id).submitted_date.text,
                view.tasks(task_id).status.text,
                view.tasks(task_id).changed_date.text,
                view.cluster_name.text)
            task_list.append(task)
        return task_list
