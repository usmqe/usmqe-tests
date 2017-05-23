"""
Description: A simple method waiting till the task has correct status

Author: ltrilety
"""


import time
import datetime
import pytest


class TaskWaitException(Exception):
    """
    task wait exception
    """


def task_wait(task_details, desired_state='Finished', ttl=600):
    """
    wait till the task has desired state

    Parameters:
        task_details: webstr page object with task details
        desired_state (str): task desired state
                             'New' -> 'Processing' -> 'Finished'/'Failed'
                             where 'New' is not accepted as desired state
        ttl (int): how long it waits till the tasks is finished
                   in seconds
    """
    # Wait till the task has the correct state
    # state of any task: New -> Processing -> Finished/Failed
    if desired_state == 'New':
        # initial task state, no need to wait for it
        return
    elif desired_state == 'Processing':
        ttl = 4 * ttl
    elif desired_state != 'Finished' and desired_state != 'Failed':
        raise TaskWaitException('Unknown desired task state - {}'.format(
            desired_state))

    status_str = task_details.status_text
    # No status icon presented till the end
    # status = task_details.status
    start_time = datetime.datetime.now()
    timeout = datetime.timedelta(0, ttl, 0)

    while status_str != 'Processing' and\
            status_str != 'Finished' and\
            status_str != 'Failed' and\
            datetime.datetime.now() - start_time <= timeout/4:
        pytest.check(
            status_str == 'New',
            "Task status should be 'New', it is '{}'".format(status_str))
        time.sleep(5)
        status_str = task_details.status_text

    pytest.check(
        datetime.datetime.now() - start_time <= timeout/4,
        "Timeout check: The state of the task should not remain in "
        "'New' state too long, longer than {} seconds".format(ttl/4),
        hard=True)

    if desired_state == 'Processing':
        pytest.check(
            status_str != 'Finished' and status_str != 'Failed',
            "Task status should be 'Processing', it is '{}'".format(
                status_str))
        return

    while status_str == 'Processing' and\
            datetime.datetime.now() - start_time <= timeout:
        time.sleep(5)
        status_str = task_details.status_text

    pytest.check(
        datetime.datetime.now() - start_time <= timeout,
        "Timeout check: The state of the task should not remain in "
        "'Processing' state too long, longer than {} seconds".format(ttl),
        hard=True)

    pytest.check(
        status_str == desired_state,
        "Task status should be '{}', it is '{}'".format(
            desired_state, status_str))
