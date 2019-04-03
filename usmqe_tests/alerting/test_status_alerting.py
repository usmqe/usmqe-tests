"""
Alerting test suite - status
"""

import pytest
import re
from usmqe.alerting import Alerting
from usmqe.api.tendrlapi.notifications import ApiNotifications


LOGGER = pytest.get_logger('status_alerting', module=True)


def detect_bz1600910(creds, alert_count):
    """
    Tests that problem from bz 1600910 appeared.

    Args:
        alert_count (int): number of alerts reported during testing.

    Return:
        bool: If number of alerts in in api for node DOWN is greater than
            number of alerts detected in test.
    """
    api = ApiNotifications(auth=creds)
    alerts = api.get_alerts()
    down_api = [alert['tags']['message'] for alert in alerts if re.match(
        "Node .* is DOWN", alert['tags']['message'])]
    return len(down_api) > alert_count


@pytest.mark.testready
@pytest.mark.author("fbalak@redhat.com")
def test_volume_status_mail_alert(
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


@pytest.mark.testready
@pytest.mark.author("fbalak@redhat.com")
def test_volume_status_snmp_alert(
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


@pytest.mark.testready
@pytest.mark.author("fbalak@redhat.com")
def test_volume_status_api_alert(
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


@pytest.mark.testready
@pytest.mark.author("fbalak@redhat.com")
def test_host_status_mail_alert(
        workload_stop_hosts, default_entities, valid_session_credentials):
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
    results = []
    total_alert_count = 0
    for host in workload_stop_hosts["result"]:
        entities["node"] = host
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
        total_alert_count += alert_count
        record = {
            'node': host,
            'subject': mail_subject,
            'msg': mail_msg,
            'alerts': alert_count}
        results.append(record)

    bz1600910 = detect_bz1600910(valid_session_credentials, total_alert_count)
    pytest.check(
        not bz1600910,
        issue="https://bugzilla.redhat.com/show_bug.cgi?id=1600910")
    if not bz1600910:
        for record in results:
            pytest.check(
                record['alerts'] == 1,
                "There should be 1 alert:\nSubject: '{0}'\nBody: '{1}'\n"
                "There is {2}".format(
                    record['subject'], record['msg'], record['alert_count']))


@pytest.mark.testready
@pytest.mark.author("fbalak@redhat.com")
def test_host_status_snmp_alert(
        workload_stop_hosts, default_entities, valid_session_credentials):
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
    results = []
    total_alert_count = 0
    for host in workload_stop_hosts["result"]:
        entities["node"] = host
        LOGGER.debug("searching host: {0}".format(host))

        entities["value"] = "DOWN"
        mail_subject, mail_msg = alerting.generate_alert_msg(
            domain="node",
            subject="status",
            entities=entities)
        alert_count = alerting.search_snmp(
            "[{0}], {1}-{2}".format(severity, mail_subject, mail_msg),
            workload_stop_hosts['start'],
            workload_stop_hosts['end'])
        total_alert_count += alert_count
        record = {
            'node': host,
            'subject': mail_subject,
            'msg': mail_msg,
            'alerts': alert_count}
        results.append(record)

    bz1600910 = detect_bz1600910(valid_session_credentials, total_alert_count)
    pytest.check(
        not bz1600910,
        issue="https://bugzilla.redhat.com/show_bug.cgi?id=1600910")
    if not bz1600910:
        for record in results:
            pytest.check(
                record['alerts'] == 1,
                "There should be 1 alert:\nSubject: '{0}'\nBody: '{1}'\n"
                "There is {2}".format(
                    record['subject'], record['msg'], record['alert_count']))


@pytest.mark.testready
@pytest.mark.author("fbalak@redhat.com")
def test_host_status_api_alert(
        workload_stop_hosts, default_entities, valid_session_credentials):
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
    results = []
    total_alert_count = 0
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
        total_alert_count += alert_count
        record = {
            'node': host,
            'msg': msg,
            'alerts': alert_count}
        results.append(record)

    bz1600910 = detect_bz1600910(valid_session_credentials, total_alert_count)
    pytest.check(
        not bz1600910,
        issue="https://bugzilla.redhat.com/show_bug.cgi?id=1600910")
    if not bz1600910:
        for record in results:
            pytest.check(
                record['alerts'] >= 1,
                "There should be 1 alert:\nBody: '{0}'\n"
                "There is {1}".format(
                    record['msg'], record['alert_count']))
