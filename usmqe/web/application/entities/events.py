import attr
import pytest
import time

from usmqe.web.application.entities import BaseCollection, BaseEntity
from usmqe.web.application.implementations.web_ui import ViaWebUI

from usmqe.web.application.views.event import ClusterEventsView
from usmqe.web.application.views.task import TaskEventsView


LOGGER = pytest.get_logger('events', module=True)


@attr.s
class BaseEvent(BaseEntity):
    """
    Base Event object. Can be either Cluster Event or Task Event.
    """
    event_id = attr.ib()
    description = attr.ib()
    date = attr.ib()


@attr.s
class Event(BaseEvent):
    """
    Event object is an item of a Cluster's EventsCollection.
    """
    cluster_name = attr.ib()


@attr.s
class EventsCollection(BaseCollection):
    ENTITY = Event

    def get_all_event_ids(self):
        """
        Return the list of event ids of all events associated with the given cluster.
        """
        view = self.application.web_ui.create_view(ClusterEventsView)
        time.sleep(2)
        return view.all_event_ids

    def get_events(self):
        """
        Return the list of instantiated Event objects, their attributes read from Events page.
        """
        view = ViaWebUI.navigate_to(self.parent, "Events")
        event_list = []
        for event_id in self.get_all_event_ids():
            event = self.instantiate(
                event_id,
                view.events(event_id).description.text,
                view.events(event_id).date.text,
                view.cluster_name.text)
            event_list.append(event)
        return event_list


@attr.s
class TaskEvent(BaseEvent):
    """
    Task Event object is an item of a Task's TaskEventsCollection.
    In addition to common event attributes Task Event also has event_type
    that can be either 'info' or 'error'.
    """
    event_type = attr.ib()


@attr.s
class TaskEventsCollection(BaseCollection):
    ENTITY = TaskEvent

    def get_all_event_ids(self):
        """
        Return the list of event ids of all events that were related to the given Task.
        """
        view = self.application.web_ui.create_view(TaskEventsView)
        time.sleep(2)
        return view.all_event_ids

    def get_events(self):
        """
        Return the list of instantiated Event objects, their attributes read from the Task's log.
        """
        view = ViaWebUI.navigate_to(self.parent, "Events")
        event_list = []
        for event_id in self.get_all_event_ids():
            event = self.instantiate(
                event_id,
                view.events(event_id).description.text,
                view.events(event_id).date.text,
                view.events(event_id).event_type.text,
                )
            event_list.append(event)
        return event_list
