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
