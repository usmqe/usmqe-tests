import pytest


@pytest.mark.author("ebondare@redhat.com")
@pytest.mark.happypath
@pytest.mark.testready
def test_task_attributes(application):
    """
    Check that all common task attributes are as expected
    """
    """
    :step:
      Log in to Web UI and get the first cluster from the cluster list.
      Get the list of tasks associated with this cluster.
    :result:
      Task objects are initiated and their attributes are read from Tasks page
    """
    clusters = application.collections.clusters.get_clusters()
    test_cluster = clusters[0]
    tasks = test_cluster.tasks.get_tasks()
    """
    :step:
      Check that tasks list is not empty and that each task has well-formed task id,
      correct status and date within reasonable range.
    :result:
      Attributes of all task in the task list are as expected.
    """
    pytest.check(tasks != [])
    for task in tasks:
        pytest.check(len(task.task_id) == 36)
        pytest.check(task.task_id[8] == "-")
        pytest.check(task.status in {"New", "Completed", "Failed"})
        pytest.check(int(task.submitted_date.split(" ")[2]) > 2010)
        pytest.check(int(task.submitted_date.split(" ")[2]) < 2100)
        pytest.check(int(task.changed_date.split(" ")[2]) > 2010)
        pytest.check(int(task.changed_date.split(" ")[2]) < 2100)


def test_task_log(application):
    """
    Test that clicking task name opens task log page
    and all events in the log have expected attributes
    """
    """
    :step:
      Log in to Web UI and get the first cluster from the cluster list.
      Get the list of tasks associated with this cluster.
    :result:
      Task objects are initiated and their attributes are read from Tasks page
    """
    clusters = application.collections.clusters.get_clusters()
    test_cluster = clusters[0]
    tasks = test_cluster.tasks.get_tasks()
    pytest.check(tasks != [])
    """
    :step:
      For each task get its log and check the attributes of the events in the log
    :result:
      Attributes of all events in all task logs are as expected.
    """
    for task in tasks:
        events = task.task_events.get_events()
        pytest.check(events != [])
        for event in events:
            pytest.check(event.event_type in {"info", "error"})
            pytest.check(len(event.description) > 10)
            pytest.check(int(event.date.split(" ")[2]) > 2010)
