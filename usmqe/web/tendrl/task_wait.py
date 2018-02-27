"""
Description: A simple method waiting till the task has correct status

Author: ltrilety
"""


import time
import datetime
import pytest

from usmqe.web.tendrl.details.tasks.pages import TaskDetails, TaskEvents


class TaskWaitException(Exception):
    """
    task wait exception
    """


def task_wait(driver, desired_state='Finished', ttl=600,
              update_time=600, sleep_time=5):
    """
    wait till the task has desired state
    NOTE: it has to be on the page with task details

    Parameters:
        driver: selenium driver
        desired_state (str): task desired state
                             'New' -> 'Processing' -> 'Finished'/'Failed'
                             where 'New' is not accepted as desired state
        ttl (int): how long it waits till the tasks is finished
                   in seconds
        update_time (int): how long it waits till the new message (event)
                            is comming
                           it's also the time how long the task could
                            remain in 'New' state
                           in seconds
        sleep_time (int): sleep time between loops
    """
    task_details = TaskDetails(driver)

    # Wait till the task has the correct state
    # state of any task: New -> Processing -> Finished/Failed
    if desired_state == 'New':
        # initial task state, no need to wait for it
        raise TaskWaitException("Waiting for New doesn't make sense")
    if desired_state not in ('Processing', 'Finished', 'Failed'):
        raise TaskWaitException('Unknown desired task state - {}'.format(
            desired_state))

    status_str = task_details.status_text
    # No status icon presented till the end
    # status = task_details.status
    start_time = datetime.datetime.now()
    last_update = start_time
    task_timeout = datetime.timedelta(seconds=ttl)
    if desired_state == 'Processing':
        # if processing use ttl for initial wait
        # as there will be no other
        update_timeout = task_timeout
    else:
        update_timeout = datetime.timedelta(seconds=update_time)

    while status_str != 'Processing' and\
            status_str != 'Finished' and\
            status_str != 'Failed' and\
            datetime.datetime.now() - start_time <= update_timeout:
        pytest.check(
            status_str == 'New',
            "Task status should be 'New', it is '{}'".format(status_str))
        time.sleep(sleep_time)
        status_str = task_details.status_text

    pytest.check(
        datetime.datetime.now() - start_time <= update_timeout,
        "Timeout check: The state of the task should not remain in "
        "'New' state too long, longer than {} seconds".format(update_time),
        hard=True)

    task_events = TaskEvents(driver)
    events_nr = task_events.events_nr

    if desired_state == 'Processing':
        pytest.check(
            status_str == desired_state,
            "Task status should be 'Processing', it is '{}'".format(
                status_str))
        return

    while status_str == 'Processing' and\
            datetime.datetime.now() - start_time <= task_timeout and\
            datetime.datetime.now() - last_update <= update_timeout:
        time.sleep(sleep_time)
        status_str = task_details.status_text
        # check if there is a new event
        if events_nr < task_events.events_nr:
            last_update = datetime.datetime.now()
            events_nr = task_events.events_nr

    pytest.check(
        datetime.datetime.now() - start_time <= task_timeout,
        "Timeout check: The state of the task should not remain in "
        "'Processing' state too long, longer than {} seconds".format(ttl),
        hard=True)
    pytest.check(
        datetime.datetime.now() - last_update <= update_timeout,
        "Timeout check: There should be an update every {} "
        "seconds".format(update_time),
        hard=True)

    pytest.check(
        status_str == desired_state,
        "Task status should be '{}', it is '{}'".format(
            desired_state, status_str))
