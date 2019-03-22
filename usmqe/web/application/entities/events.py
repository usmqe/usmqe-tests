import attr
import pytest
from wait_for import wait_for

from usmqe.web.application.entities import BaseCollection, BaseEntity
from usmqe.web.application.implementations.web_ui import ViaWebUI


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

    def get_events(self):
        """
        Return the list of instantiated Event objects, their attributes read from Events page.
        """
        view = ViaWebUI.navigate_to(self.parent, "Events")
        wait_for(lambda: view.is_displayed,
                 timeout=10,
                 delay=2,
                 message="Events page hasn't been displayed in time")
        event_list = []
        for event_id in view.all_event_ids:
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

    def get_events(self):
        """
        Return the list of instantiated Event objects, their attributes read from the Task's log.
        """
        view = ViaWebUI.navigate_to(self.parent, "Events")
        wait_for(lambda: view.is_displayed,
                 timeout=10,
                 delay=2,
                 message="Events page hasn't been displayed in time")
        event_list = []
        for event_id in view.all_event_ids:
            event = self.instantiate(
                event_id,
                view.events(event_id).description.text,
                view.events(event_id).date.text,
                view.events(event_id).event_type.text,
                )
            event_list.append(event)
        return event_list
