import pytest

from usmqe.web import tools


@pytest.mark.author("ebondare@redhat.com")
@pytest.mark.happypath
@pytest.mark.testready
def test_event_attributes(application, imported_cluster_reuse):
    """
    Check that all common event attributes are as expected
    """
    """
    :step:
      Log in to Web UI and get the cluster identified by cluster_member.
      Get the list of events associated with this cluster.
    :result:
      Event objects are initiated and their attributes are read from Tasks page
    """
    clusters = application.collections.clusters.get_clusters()
    test_cluster = tools.choose_cluster(clusters, imported_cluster_reuse["cluster_id"])
    assert test_cluster.managed == "Yes"
    events = test_cluster.events.get_events()
    """
    :step:
      Check that events list is not empty and that each event has description
      of reasonable length and date within reasonable range.
    :result:
      Attributes of all events in the event list are as expected.
    """
    pytest.check(events != [],
                 "Check that events list in UI isn't empty")
    for event in events:
        pytest.check(len(event.description) > 15,
                     "Description: {}. Should be more than 15 chars".format(event.description))
        pytest.check(int(event.date.split(" ")[2]) > 2018,
                     "Event date: {}. Year should be greater than 2018".format(event.date))
