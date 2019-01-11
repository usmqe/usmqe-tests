"""
Alerting test suite - workload
"""

import pytest
from usmqe.alerting.alerting import Alerting


LOGGER = pytest.get_logger('workload_alerting', module=True)


@pytest.mark.author("ebondare@redhat.com")
@pytest.mark.author("fbalak@redhat.com")
@pytest.mark.ansible_playbook_setup('test_setup.smtp.yml')
@pytest.mark.ansible_playbook_setup('test_setup.snmp.yml')
@pytest.mark.ansible_playbook_setup('test_setup.stress_ng.yml')
def test_cpu_utilization_mail_alert(
        #ansible_playbook,
        workload_cpu_utilization, default_entities):
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

    alerting = Alerting("root")
    entities = default_entities
    # todo(fbalak) use this when supported
    # entities["volume"] = workload_cpu_utilization["metadata"]["volume_name"]
    target = workload_cpu_utilization['result']
    if (workload_cpu_utilization['result'] >= 75 and
        workload_cpu_utilization['result'] < 90):
            severity = "WARNING"
            entities["value"] = "at $value and running out of cpu"
    elif (workload_cpu_utilization['result'] >= 90):
        severity = "CRITICAL"
        entities["value"] = "at $value and running out of cpu"
    else:
        severity = "INFO"
        entities["value"] = "back to normal"
        target = None
    mail_subject, mail_msg = alerting.generate_alert_msg(
        level=severity,
        domain="node",
        subject="cpu",
        entities=entities)
    alert_count = alerting.search_mail(
        mail_subject,
        mail_msg,
        workload_cpu_utilization['start'],
        workload_cpu_utilization['end'],
        target=target)
    pytest.check(
        alert_count == 1,
        "There should be 1 alert:\nSubject: '{0}'\nBody: '{1}'\n"\
        "There is {2}".format(
            mail_subject, mail_msg, alert_count))
    #todo(fbalak): check for clearing alert


    """
    :step:
      Check that the type of alert corresponds to the workload
    :result:
      If the workload was low, there's no alert. If it's high, the correct alert was received.
    """
