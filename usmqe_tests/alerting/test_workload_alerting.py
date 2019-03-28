"""
Alerting test suite - workload
"""

import pytest
from usmqe.alerting import Alerting


LOGGER = pytest.get_logger('workload_alerting', module=True)


@pytest.mark.testready
@pytest.mark.author("ebondare@redhat.com")
@pytest.mark.author("fbalak@redhat.com")
@pytest.mark.ansible_playbook_setup('test_setup.smtp.yml')
@pytest.mark.ansible_playbook_setup('test_setup.stress_tools.yml')
def test_cpu_utilization_mail_alert(
        ansible_playbook,
        workload_cpu_utilization, default_entities):
    """
    Check that Tendrl sends no CPU Utilization alerts if utilization is below
    70, it sends CPU Utilization warnings if CPU Utilization is between 70 and
    90 and it sends CPU Utilization critical alerts if utilization is above 90.
    """
    """
    :step:
      Get the messages that arrived in the interval provided by cpu utilization
      fixture or a little later
    :result:
      The list of all relevant messages
    """

    alerting = Alerting("root")
    entities = default_entities
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
        domain="node",
        subject="cpu",
        entities=entities)
    alert_count = alerting.search_mail(
        "[{0}] {1}".format(severity, mail_subject),
        mail_msg,
        workload_cpu_utilization['start'],
        workload_cpu_utilization['end'],
        target=target)
    pytest.check(
        alert_count == 1,
        "There should be 1 alert:\nSubject: '{0}'\nBody: '{1}'\n"
        "There is {2}".format(
            mail_subject, mail_msg, alert_count))


@pytest.mark.testready
@pytest.mark.author("fbalak@redhat.com")
@pytest.mark.ansible_playbook_setup('test_setup.snmp.yml')
@pytest.mark.ansible_playbook_setup('test_setup.stress_tools.yml')
def test_cpu_utilization_snmp_alert(
        ansible_playbook,
        workload_cpu_utilization, default_entities):
    """
    Check that Tendrl sends no CPU Utilization alerts if utilization is below
    70, it sends CPU Utilization warnings if CPU Utilization is between 70 and
    90 and it sends CPU Utilization critical alerts if utilization is above 90.
    """
    """
    :step:
      Get the messages that arrived in the interval provided by cpu utilization
      fixture or a little later
    :result:
      The list of all relevant messages
    """

    alerting = Alerting("root")
    entities = default_entities
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
        domain="node",
        subject="cpu",
        entities=entities)
    alert_count = alerting.search_snmp(
        "[{0}], {1}-{2}".format(severity, mail_subject, mail_msg),
        workload_cpu_utilization['start'],
        workload_cpu_utilization['end'],
        target=target)
    pytest.check(
        alert_count == 1,
        "There should be 1 alert:\nSubject: '{0}'\nBody: '{1}'\n"
        "There is {2}".format(
            mail_subject, mail_msg, alert_count))


@pytest.mark.testready
@pytest.mark.author("fbalak@redhat.com")
@pytest.mark.ansible_playbook_setup('test_setup.alerts_logger.yml')
@pytest.mark.ansible_playbook_setup('test_setup.stress_tools.yml')
def test_cpu_utilization_api_alert(
        ansible_playbook,
        workload_cpu_utilization, default_entities):
    """
    Check that Tendrl sends no CPU Utilization alerts if utilization is below
    70, it sends CPU Utilization warnings if CPU Utilization is between 70 and
    90 and it sends CPU Utilization critical alerts if utilization is above 90.
    """
    """
    :step:
      Get the messages that arrived in the interval provided by cpu utilization
      fixture or a little later
    :result:
      The list of all relevant messages
    """

    alerting = Alerting()
    entities = default_entities
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
    _, msg = alerting.generate_alert_msg(
        domain="node",
        subject="cpu",
        entities=entities)
    alert_count = alerting.search_api(
        severity,
        msg,
        workload_cpu_utilization['start'],
        workload_cpu_utilization['end'],
        target=target)
    pytest.check(
        alert_count >= 1,
        "There should be at least 1 alert:\nBody: '{0}'\n"
        "There is {1}".format(
            msg, alert_count))


@pytest.mark.testready
@pytest.mark.author("fbalak@redhat.com")
@pytest.mark.ansible_playbook_setup('test_setup.smtp.yml')
@pytest.mark.ansible_playbook_setup('test_setup.stress_tools.yml')
def test_memory_utilization_mail_alert(
        ansible_playbook,
        workload_memory_utilization, default_entities):
    """
    Check that Tendrl sends no memory Utilization alerts if utilization is
    below 70, it sends memory Utilization warnings if memory Utilization is
    between 70 and 90 and it sends memory Utilization critical alerts if
    utilization is above 90.
    """
    """
    :step:
      Get the messages that arrived in the interval provided by memory
      utilization fixture or a little later
    :result:
      The list of all relevant messages
    """

    alerting = Alerting("root")
    entities = default_entities
    target = workload_memory_utilization['result']
    if (workload_memory_utilization['result'] >= 75 and
            workload_memory_utilization['result'] < 90):
        severity = "WARNING"
        entities["value"] = "at $value and running out of memory"
    elif (workload_memory_utilization['result'] >= 90):
        severity = "CRITICAL"
        entities["value"] = "at $value and running out of memory"
    else:
        severity = "INFO"
        entities["value"] = "back to normal"
        target = None
    mail_subject, mail_msg = alerting.generate_alert_msg(
        domain="node",
        subject="memory",
        entities=entities)
    alert_count = alerting.search_mail(
        "[{0}] {1}".format(severity, mail_subject),
        mail_msg,
        workload_memory_utilization['start'],
        workload_memory_utilization['end'],
        target=target)
    pytest.check(
        alert_count == 1,
        "There should be 1 alert:\nSubject: '{0}'\nBody: '{1}'\n"
        "There is {2}".format(
            mail_subject, mail_msg, alert_count))


@pytest.mark.testready
@pytest.mark.author("fbalak@redhat.com")
@pytest.mark.ansible_playbook_setup('test_setup.snmp.yml')
@pytest.mark.ansible_playbook_setup('test_setup.stress_tools.yml')
def test_memory_utilization_snmp_alert(
        ansible_playbook,
        workload_memory_utilization, default_entities):
    """
    Check that Tendrl sends no memory Utilization alerts if utilization is
    below 70, it sends memory Utilization warnings if memory Utilization is
    between 70 and 90 and it sends memory Utilization critical alerts if
    utilization is above 90.
    """
    """
    :step:
      Get the messages that arrived in the interval provided by memory
      utilization fixture or a little later
    :result:
      The list of all relevant messages
    """

    alerting = Alerting("root")
    entities = default_entities
    target = workload_memory_utilization['result']
    if (workload_memory_utilization['result'] >= 75 and
            workload_memory_utilization['result'] < 90):
        severity = "WARNING"
        entities["value"] = "at $value and running out of memory"
    elif (workload_memory_utilization['result'] >= 90):
        severity = "CRITICAL"
        entities["value"] = "at $value and running out of memory"
    else:
        severity = "INFO"
        entities["value"] = "back to normal"
        target = None
    mail_subject, mail_msg = alerting.generate_alert_msg(
        domain="node",
        subject="memory",
        entities=entities)
    alert_count = alerting.search_snmp(
        "[{0}], {1}-{2}".format(severity, mail_subject, mail_msg),
        workload_memory_utilization['start'],
        workload_memory_utilization['end'],
        target=target)
    pytest.check(
        alert_count == 1,
        "There should be 1 alert:\nSubject: '{0}'\nBody: '{1}'\n"
        "There is {2}".format(
            mail_subject, mail_msg, alert_count))


@pytest.mark.testready
@pytest.mark.author("fbalak@redhat.com")
@pytest.mark.ansible_playbook_setup('test_setup.alerts_logger.yml')
@pytest.mark.ansible_playbook_setup('test_setup.stress_tools.yml')
def test_memory_utilization_api_alert(
        ansible_playbook,
        workload_memory_utilization, default_entities):
    """
    Check that Tendrl sends no memory Utilization alerts if utilization is
    below 70, it sends memory Utilization warnings if memory Utilization is
    between 70 and 90 and it sends memory Utilization critical alerts if
    utilization is above 90.
    """
    """
    :step:
      Get the messages that arrived in the interval provided by memory
      utilization fixture or a little later
    :result:
      The list of all relevant messages
    """

    alerting = Alerting()
    entities = default_entities
    target = workload_memory_utilization['result']
    if (workload_memory_utilization['result'] >= 75 and
            workload_memory_utilization['result'] < 90):
        severity = "WARNING"
        entities["value"] = "at $value and running out of memory"
    elif (workload_memory_utilization['result'] >= 90):
        severity = "CRITICAL"
        entities["value"] = "at $value and running out of memory"
    else:
        severity = "INFO"
        entities["value"] = "back to normal"
        target = None
    _, msg = alerting.generate_alert_msg(
        domain="node",
        subject="memory",
        entities=entities)
    alert_count = alerting.search_api(
        severity,
        msg,
        workload_memory_utilization['start'],
        workload_memory_utilization['end'],
        target=target)
    pytest.check(
        alert_count >= 1,
        "There should be at least 1 alert:\nBody: '{0}'\n"
        "There is {1}".format(
            msg, alert_count))
