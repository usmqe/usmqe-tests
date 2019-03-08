import attr
import pytest
from navmazing import NavigateToAttribute
from wait_for import wait_for

from usmqe.web.application.entities import BaseCollection, BaseEntity
from usmqe.web.application.implementations.web_ui import ViaWebUI
from usmqe.web.application.entities.events import TaskEventsCollection
from usmqe.web.application.implementations.web_ui import TendrlNavigateStep
from usmqe.web.application.views.task import TaskEventsView


LOGGER = pytest.get_logger('volumes', module=True)


@attr.s
class Task(BaseEntity):
    """
    Task object is an item of a Cluster's TasksCollection.
    Each task has its collection of Events.
    """
    task_id = attr.ib()
    task_name = attr.ib()
    submitted_date = attr.ib()
    status = attr.ib()
    changed_date = attr.ib()
    cluster_name = attr.ib()

    _collections = {'task_events': TaskEventsCollection}

    @property
    def task_events(self):
        return self.collections.task_events


@attr.s
class TasksCollection(BaseCollection):
    ENTITY = Task

    def get_tasks(self):
        """
        Return the list of instantiated Task objects, their attributes read from Tasks page.
        """
        view = ViaWebUI.navigate_to(self.parent, "Tasks")
        wait_for(lambda: view.is_displayed, timeout=10, delay=2)
        task_list = []
        for task_id in view.all_task_ids:
            task = self.instantiate(
                task_id,
                view.tasks(task_id).task_name.text,
                view.tasks(task_id).submitted_date.text,
                view.tasks(task_id).status.text,
                view.tasks(task_id).changed_date.text,
                view.cluster_name.text)
            task_list.append(task)
        return task_list


@ViaWebUI.register_destination_for(Task, "Events")
class TaskEvents(TendrlNavigateStep):
    """
    Navigate to the task's event log by clicking on the task name.
    """
    VIEW = TaskEventsView
    prerequisite = NavigateToAttribute("parent.parent", "Tasks")

    def step(self):
        self.parent.tasks(self.obj.task_id).task_name.click()
