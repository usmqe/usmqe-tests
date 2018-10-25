"""
Alerting test suite - workload
"""

import pytest
import time
import usmqe.usmmail


LOGGER = pytest.get_logger('workload_alerting', module=True)


@pytest.mark.author("ebondare@redhat.com")
def test_cpu_alerts(workload_cpu_utilization):
    """
    Check that Tendrl sends no CPU Utilization alerts if utilization is below 70,
    it sends CPU Utilization warnings if CPU Utilization is between 70 and 90
    and it sends CPU Utilization critical alerts if utilization is above 90.
    """
    """
    :step:
      Get the messages that arrived in the interval provided by cpu utilization fixture
      or a little later
    :result:
      The list of all relevant messages
    """
    EXTRA_TIME = 30
    from_timestamp = workload_cpu_utilization["start"].timestamp()
    until_timestamp = workload_cpu_utilization["end"].timestamp() + EXTRA_TIME
    LOGGER.debug("Fixture start timestamp: {} ({})".format(from_timestamp,
                                                           workload_cpu_utilization["start"]))
    LOGGER.debug("Fixture end timestamp: {} ({})".format(until_timestamp - EXTRA_TIME,
                                                         workload_cpu_utilization["end"]))
    LOGGER.debug("Fixture result is: {}".format(workload_cpu_utilization["result"]))

    # Wait until the messages surely arrive
    time.sleep(EXTRA_TIME)
    messages = usmqe.usmmail.get_msgs_by_time(start_timestamp=from_timestamp,
                                              end_timestamp=until_timestamp)
    LOGGER.debug("Selected messages count: {}".format(len(messages)))

    """
    :step:
      Check that the type of alert corresponds to the workload
    :result:
      If the workload was low, there's no alert. If it's high, the correct alert was received.
    """
    # Distinguish between warnings and critical alerts
    cpu_warning = False
    cpu_critical = False
    for message in messages:
        LOGGER.debug("Message date: {}".format(message['Date']))
        LOGGER.debug("Message subject: {}".format(message['Subject']))
        LOGGER.debug("Message body: {}".format(message.get_payload(decode=True)))
        if message['Subject'].count("[WARNING] Cpu Utilization: threshold breached") > 0:
            cpu_warning = True
        if message['Subject'].count("[CRITICAL] Cpu Utilization: threshold breached") > 0:
            cpu_critical = True

    # Check if the number and type of alerts fits CPU Utilization
    if workload_cpu_utilization["result"] < 70:
        pytest.check(not cpu_warning and not cpu_critical)
    elif workload_cpu_utilization["result"] < 90:
        pytest.check(cpu_warning and not cpu_critical)
    else:
        pytest.check(cpu_critical and not cpu_warning)
