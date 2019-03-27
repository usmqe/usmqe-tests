import pytest

from usmqe.web import tools


@pytest.mark.author("ebondare@redhat.com")
@pytest.mark.happypath
@pytest.mark.testready
def test_task_attributes(application, imported_cluster_reuse):
    """
    Check that all common task attributes are as expected
    """
    """
    :step:
      Log in to Web UI and get the cluster identified by cluster_member.
      Get the list of tasks associated with this cluster.
    :result:
      Task objects are initiated and their attributes are read from Tasks page
    """
    clusters = application.collections.clusters.get_clusters()
    test_cluster = tools.choose_cluster(clusters,
                                        imported_cluster_reuse["cluster_id"],
                                        imported_cluster_reuse["short_name"])
    assert test_cluster.managed == "Yes"
    tasks = test_cluster.tasks.get_tasks()
    """
    :step:
      Check that tasks list is not empty and that each task has well-formed task id,
      correct status and date within reasonable range.
    :result:
      Attributes of all task in the task list are as expected.
    """
    pytest.check(tasks != [],
                 "Check that cluster's Tasks list isn't empty")
    for task in tasks:
        pytest.check(len(task.task_id) == 36,
                     "Task id: {} Should be of length 36".format(task.task_id))
        pytest.check(task.task_id[8] == "-",
                     "The 9th symbol of task id should be ``-``")
        pytest.check(task.status in {"New", "Completed", "Failed"},
                     "Task status: {}. Should be New, Completed or Failed".format(task.status))
        pytest.check(int(task.submitted_date.split(" ")[2]) > 2018,
                     "Task submitted on {}. Should be later than 2018".format(task.submitted_date))
        pytest.check(int(task.changed_date.split(" ")[2]) > 2018,
                     "Task changed on {}. Should be later than 2018".format(task.changed_date))


def test_task_log(application, imported_cluster_reuse):
    """
    Test that clicking task name opens task log page
    and all events in the log have expected attributes
    """
    """
    :step:
      Log in to Web UI and get the cluster identified by cluster_member.
      Get the list of tasks associated with this cluster.
    :result:
      Task objects are initiated and their attributes are read from Tasks page
    """
    clusters = application.collections.clusters.get_clusters()
    test_cluster = tools.choose_cluster(clusters,
                                        imported_cluster_reuse["cluster_id"],
                                        imported_cluster_reuse["short_name"])
    assert test_cluster.managed == "Yes"
    tasks = test_cluster.tasks.get_tasks()
    pytest.check(tasks != [],
                 "Check that cluster's Tasks list isn't empty")
    """
    :step:
      For each task get its log and check the attributes of the events in the log
    :result:
      Attributes of all events in all task logs are as expected.
    """
    for task in tasks:
        events = task.task_events.get_events()
        pytest.check(events != [],
                     "Check that task's Events list isn't empty")
        for event in events:
            pytest.check(event.event_type in {"info", "error"},
                         "Event type: {}. Should be 'info' or 'error'".format(event.event_type))
            pytest.check(len(event.description) > 10,
                         "Description: {}. Should be more than 10 char".format(event.description))
            pytest.check(int(event.date.split(" ")[2]) > 2018,
                         "Date: {}. Should be later than 2018".format(event.date))
