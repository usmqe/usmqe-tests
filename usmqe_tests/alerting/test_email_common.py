"""
Alerting test suite - general tests
"""
import pytest
import usmqe.usmmail
from datetime import datetime


LOGGER = pytest.get_logger('alerting_common', module=True)


def test_no_messages_from_future():
    """
    Alerting: common
    *******************

    .. test_metadata:: author ebondare@redhat.com

    Description
    ===========

    Test that there are no messages with date later than the current date
    """
    messages = usmqe.usmmail.get_msgs_by_time(start_timestamp=datetime.now().timestamp())
    LOGGER.debug("Current time: {}".format(datetime.now()))
    LOGGER.debug("Current timestamp: {}".format(datetime.now().timestamp()))
    LOGGER.debug("Selected messages count: {}".format(len(messages)))
    for message in messages:
        LOGGER.debug("Message date: {}".format(message['Date']))
    pytest.check(len(messages) == 0)
