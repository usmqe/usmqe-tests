"""
Alerting test suite - status
"""

import pytest
from usmqe.alerting import Alerting


LOGGER = pytest.get_logger('status_alerting', module=True)


@pytest.mark.author("fbalak@redhat.com")
@pytest.mark.ansible_playbook_teardown('test_teardown.gluster_volume_stop.yml')
@pytest.mark.ansible_playbook_setup('test_setup.gluster_volume_stop.yml')
@pytest.mark.ansible_playbook_setup('test_setup.smtp.yml')
def test_volume_status_mail_alert(
        ansible_playbook,
        workload_stop_volumes, default_entities):
    """
    Check that Tendrl sends correct status alert when volume is stopped.
    """
    """
    :step:
      Get the messages that arrived in the interval provided by
      workload_stopped_volume fixture or a little later
    :result:
      The list of all relevant messages
    """

    alerting = Alerting("root")
    entities = default_entities
    severity = "WARNING"
    for volume in workload_stop_volumes["result"]:
        entities["volume"] = volume

        entities["value"] = "from Started to Stopped"
        mail_subject, mail_msg = alerting.generate_alert_msg(
            domain="volume",
            subject="status",
            entities=entities)
        alert_count = alerting.search_mail(
            "[{0}] {1}".format(severity, mail_subject),
            mail_msg,
            workload_stop_volumes['start'],
            workload_stop_volumes['end'])
        pytest.check(
            alert_count == 1,
            "There should be 1 alert:\nSubject: '{0}'\nBody: '{1}'\n"
            "There is {2}".format(
                mail_subject, mail_msg, alert_count))

        entities["value"] = "down"
        mail_subject, mail_msg = alerting.generate_alert_msg(
            domain="volume",
            subject="running",
            entities=entities)
        alert_count = alerting.search_mail(
            "[{0}] {1}".format(severity, mail_subject),
            mail_msg,
            workload_stop_volumes['start'],
            workload_stop_volumes['end'])
        pytest.check(
            alert_count == 1,
            "There should be 1 alert:\nSubject: '{0}'\nBody: '{1}'\n"
            "There is {2}".format(
                mail_subject, mail_msg, alert_count))

    entities["value"] = "unhealthy"
    mail_subject, mail_msg = alerting.generate_alert_msg(
        domain="cluster",
        subject="health",
        entities=entities)
    alert_count = alerting.search_mail(
        "[{0}] {1}".format(severity, mail_subject),
        mail_msg,
        workload_stop_volumes['start'],
        workload_stop_volumes['end'])
    pytest.check(
        alert_count == 1,
        "There should be 1 alert:\nSubject: '{0}'\nBody: '{1}'\n"
        "There is {2}".format(
            mail_subject, mail_msg, alert_count))


@pytest.mark.author("fbalak@redhat.com")
@pytest.mark.ansible_playbook_teardown('test_teardown.gluster_volume_stop.yml')
@pytest.mark.ansible_playbook_setup('test_setup.gluster_volume_stop.yml')
@pytest.mark.ansible_playbook_setup('test_setup.snmp.yml')
def test_volume_status_snmp_alert(
        ansible_playbook,
        workload_stop_volumes, default_entities):
    """
    Check that Tendrl sends correct status alert when volume is stopped.
    """
    """
    :step:
      Get the messages that arrived in the interval provided by
      workload_stopped_volume fixture or a little later
    :result:
      The list of all relevant messages
    """

    alerting = Alerting("root")
    entities = default_entities
    severity = "WARNING"
    for volume in workload_stop_volumes["result"]:
        entities["volume"] = volume

        entities["value"] = "from Started to Stopped"
        mail_subject, mail_msg = alerting.generate_alert_msg(
            domain="volume",
            subject="status",
            entities=entities)
        alert_count = alerting.search_snmp(
            "[{0}], {1}-{2}".format(severity, mail_subject, mail_msg),
            workload_stop_volumes['start'],
            workload_stop_volumes['end'])
        pytest.check(
            alert_count == 1,
            "There should be 1 alert:\nSubject: '{0}'\nBody: '{1}'\n"
            "There is {2}".format(
                mail_subject, mail_msg, alert_count))

        entities["value"] = "down"
        mail_subject, mail_msg = alerting.generate_alert_msg(
            domain="volume",
            subject="running",
            entities=entities)
        alert_count = alerting.search_snmp(
            "[{0}], {1}-{2}".format(severity, mail_subject, mail_msg),
            workload_stop_volumes['start'],
            workload_stop_volumes['end'])
        pytest.check(
            alert_count == 1,
            "There should be 1 alert:\nSubject: '{0}'\nBody: '{1}'\n"
            "There is {2}".format(
                mail_subject, mail_msg, alert_count))

    entities["value"] = "unhealthy"
    mail_subject, mail_msg = alerting.generate_alert_msg(
        domain="cluster",
        subject="health",
        entities=entities)
    alert_count = alerting.search_snmp(
        "[{0}], {1}-{2}".format(severity, mail_subject, mail_msg),
        workload_stop_volumes['start'],
        workload_stop_volumes['end'])
    pytest.check(
        alert_count == 1,
        "There should be 1 alert:\nSubject: '{0}'\nBody: '{1}'\n"
        "There is {2}".format(
            mail_subject, mail_msg, alert_count))


@pytest.mark.author("fbalak@redhat.com")
@pytest.mark.ansible_playbook_teardown('test_teardown.gluster_volume_stop.yml')
@pytest.mark.ansible_playbook_setup('test_setup.gluster_volume_stop.yml')
@pytest.mark.ansible_playbook_setup('test_setup.alerts_logger.yml')
def test_volume_status_api_alert(
        ansible_playbook,
        workload_stop_volumes, default_entities):
    """
    Check that Tendrl sends correct status alert when volume is stopped.
    """
    """
    :step:
      Get the messages that arrived in the interval provided by
      workload_stopped_volume fixture or a little later
    :result:
      The list of all relevant messages
    """

    alerting = Alerting()
    entities = default_entities
    severity = "WARNING"
    for volume in workload_stop_volumes["result"]:
        entities["volume"] = volume

        entities["value"] = "from Started to Stopped"
        _, msg = alerting.generate_alert_msg(
            domain="volume",
            subject="status",
            entities=entities)
        alert_count = alerting.search_api(
            severity,
            msg,
            workload_stop_volumes['start'],
            workload_stop_volumes['end'])
        pytest.check(
            alert_count >= 1,
            "There should be at least 1 alert:\nBody: '{0}'\n"
            "There is {1}".format(
                msg, alert_count))

        entities["value"] = "down"
        _, msg = alerting.generate_alert_msg(
            domain="volume",
            subject="running",
            entities=entities)
        alert_count = alerting.search_api(
            severity,
            msg,
            workload_stop_volumes['start'],
            workload_stop_volumes['end'])
        pytest.check(
            alert_count >= 1,
            "There should be at least 1 alert:\nBody: '{0}'\n"
            "There is {1}".format(
                msg, alert_count))

    entities["value"] = "unhealthy"
    _, msg = alerting.generate_alert_msg(
        domain="cluster",
        subject="health",
        entities=entities)
    alert_count = alerting.search_api(
        severity,
        msg,
        workload_stop_volumes['start'],
        workload_stop_volumes['end'])
    pytest.check(
        alert_count >= 1,
        "There should be at least 1 alert:\nBody: '{0}'\n"
        "There is {1}".format(
            msg, alert_count))


@pytest.mark.author("fbalak@redhat.com")
@pytest.mark.ansible_playbook_setup('test_setup.smtp.yml')
def test_host_status_mail_alert(
        ansible_playbook,
        workload_stop_hosts, default_entities):
    """
    Check that Tendrl sends correct status alert when host is stopped.
    """
    """
    :step:
      Get the messages that arrived in the interval provided by
      workload_stopped_host fixture or a little later
    :result:
      The list of all relevant messages
    """

    alerting = Alerting("root")
    entities = default_entities
    severity = "WARNING"
    for host in workload_stop_hosts["result"]:
        entities["host"] = host
        LOGGER.debug("searching host: {0}".format(host))

        entities["value"] = "DOWN"
        mail_subject, mail_msg = alerting.generate_alert_msg(
            domain="node",
            subject="status",
            entities=entities)
        alert_count = alerting.search_mail(
            "[{0}] {1}".format(severity, mail_subject),
            mail_msg,
            workload_stop_hosts['start'],
            workload_stop_hosts['end'])
        pytest.check(
            alert_count == 1,
            "There should be 1 alert:\nSubject: '{0}'\nBody: '{1}'\n"
            "There is {2}".format(
                mail_subject, mail_msg, alert_count))


@pytest.mark.author("fbalak@redhat.com")
@pytest.mark.ansible_playbook_setup('test_setup.snmp.yml')
def test_host_status_snmp_alert(
        ansible_playbook,
        workload_stop_hosts, default_entities):
    """
    Check that Tendrl sends correct status alert when host is stopped.
    """
    """
    :step:
      Get the messages that arrived in the interval provided by
      workload_stopped_host fixture or a little later
    :result:
      The list of all relevant messages
    """

    alerting = Alerting("root")
    entities = default_entities
    severity = "WARNING"
    for host in workload_stop_hosts["result"]:
        LOGGER.debug("searching host: {0}".format(host))
        entities["host"] = host

        entities["value"] = "DOWN"
        mail_subject, mail_msg = alerting.generate_alert_msg(
            domain="node",
            subject="status",
            entities=entities)
        alert_count = alerting.search_snmp(
            "[{0}], {1}-{2}".format(severity, mail_subject, mail_msg),
            workload_stop_hosts['start'],
            workload_stop_hosts['end'])
        pytest.check(
            alert_count == 1,
            "There should be 1 alert:\nSubject: '{0}'\nBody: '{1}'\n"
            "There is {2}".format(
                mail_subject, mail_msg, alert_count))


@pytest.mark.author("fbalak@redhat.com")
@pytest.mark.ansible_playbook_setup('test_setup.alerts_logger.yml')
def test_host_status_api_alert(
        ansible_playbook,
        workload_stop_hosts, default_entities):
    """
    Check that Tendrl sends correct status alert when host is stopped.
    """
    """
    :step:
      Get the messages that arrived in the interval provided by
      workload_stopped_host fixture or a little later
    :result:
      The list of all relevant messages
    """

    alerting = Alerting()
    entities = default_entities
    severity = "WARNING"
    for host in workload_stop_hosts["result"]:
        entities["node"] = host
        LOGGER.debug("searching host: {0}".format(host))

        entities["value"] = "DOWN"
        _, msg = alerting.generate_alert_msg(
            domain="node",
            subject="status",
            entities=entities)
        alert_count = alerting.search_api(
            severity,
            msg,
            workload_stop_hosts['start'],
            workload_stop_hosts['end'])
        pytest.check(
            alert_count >= 1,
            "There should be at least 1 alert:\nBody: '{0}'\n"
            "There is {1}".format(
                msg, alert_count))
