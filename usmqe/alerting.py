import pytest
import re
from string import Template
import time
from usmqe.usmqeconfig import UsmConfig
import usmqe.usmmail
import usmqe.usmssh

LOGGER = pytest.get_logger('usmqe_alerting', module=True)
CONF = UsmConfig()


class Alerting(object):
    """
    Class for alert lookup. Supports alerts from SNMP, SMTP and tendrl api.
    For api lookup there have to run `usmqe_alerts_logger` service on api
    server. This can be installled by `test_setup.alerts_logger.yml` from
    usmqe-setup repository.
    """
    def __init__(self, user="admin", client=None, server=None,
                 msg_templates=None, divergence=15.0):
        """
        Args:
            user (str): Tendrl user that receives alerts.
            client (str): Machine address with SNMP and SMTP client.
            server (str): Machine where Tendrl runs.
            msg_templates (dict): Tendrl messages can be overwritten but for
                tendrl testing should be used `basic_messages()`.
            divergence (float): Applicable divergence for comparing messages
                containing numeric values.
        """
        self.user = user
        self.client = client or CONF.inventory.get_groups_dict()[
            "usm_client"][0]
        self.server = server or CONF.inventory.get_groups_dict()[
            "usm_server"][0]
        self.msg_templates = msg_templates or self.basic_messages()
        # uses some extra time if is set up
        self.wait = True
        self.prc_pattern = re.compile(r"\d{1,3}(\.\d{1,2})(\s\%)?")
        self.divergence = divergence

    def basic_messages(self):
        """
        Returns:
            dict: Contains templates for alert messages. First key represents
                message domain, second key represents subject and value is
                template. Entities that can be replaced in template are:
                    node, cluster, volume, path, value
        """
        return {
            "node": {
                "status": {
                    "subject": "Node Status: status changed",
                    "body": "Node $node is $value"},
                "cpu": {
                    "subject": "Cpu Utilization: threshold breached",
                    "body": "Cpu utilization on node $node in $cluster $value"
                        },
                "memory": {
                    "subject": "Memory Utilization: threshold breached",
                    "body": "Memory utilization on node $node in $cluster "
                            "$value"},
                "swap": {
                    "subject": "Swap Utilization: threshold breached",
                    "body": "Swap utilization on node $node in $cluster $value"
                        },
                "georeplication": {
                    "subject": "status changed",
                    "body": "Geo-replication between $node:$path and $volume "
                            "is $value"}, },
            "brick": {
                "status": {
                    "subject": "Brick Status: status changed",
                    "body": "Brick:$node:$path in volume:$volume has $value"},
                "utilization": {
                    "subject": "Brick Utilization: threshold breached",
                    "body": "Brick utilization on $node:$path in $volume "
                            "$value"}, },
            "cluster": {
                "health": {
                    "subject": "Cluster Health Status: status changed",
                    "body": "Cluster:$cluster is $value"}, },
            "glustershd": {
                "status": {
                    "subject": "status changed",
                    "body": "Service: glustershd is $value in cluster $cluster"
                        }, },
            "volume": {
                "running": {
                    "subject": "Volume State: status changed",
                    "body": "Volume:$volume is $value"},
                "status": {
                    "subject": "Volume Status: status changed",
                    "body": "Status of volume: $volume in cluster $cluster "
                            "changed $value"}}}

    def generate_alert_msg(
            self,
            domain,
            subject,
            entities=None):
        """
        Return alert message based on parameters.

        Args:
            domain (str): Represents entity where is subject tested.
            subject (str): Subject that is tested.
                For example cpu, memory, status...
            entities (dict): Keys are entities where is subject measured
                (host, brick, volume...) and values are identificators of
                entities. These values will be used for substitution in
                templates.

        Returns:
            tuple: Alert subject and alert message.
        """
        title = self.msg_templates[domain][subject]['subject']
        message = Template(
            self.msg_templates[domain][subject]['body'])
        message = message.safe_substitute(entities)
        LOGGER.debug("Generated message subject: '{}'".format(title))
        LOGGER.debug("Generated message body: '{}'".format(message))
        return title, message

    def compare_prc(self, val, target):
        """
        Compares two values if they are identical with regards of divergence.

        Args:
            val (str): Value from message.
            target (float): Targeted value.

        Returns:
            bool: If values in messages are identical.
        """
        val = val.rstrip('%').rstrip(' ')
        identical = False
        LOGGER.debug("Compared value: {}".format(val))
        LOGGER.debug("Divergence: {}".format(self.divergence))
        if float(target) - self.divergence <= float(val) <= float(
                target) + self.divergence:
            identical = True
        return identical

    def get_until_timestamp(self, until, extra_time=30):
        """
        Checks if alerting was already used. To make sure that all
        fixtures are loaded there is added some extra time in case the alert
        search is used for the first time. Provided time is converted into
        timestamp.

        Args:
            until (datetime): Datetime until which will be mail searched.
            extra_time (int): Time to be added to timestamp.

        Returns:
            int: timestamp.
        """
        if self.wait:
            time.sleep(extra_time)
            self.wait = False
            return until.timestamp() + extra_time
        else:
            return until.timestamp()

    def search_mail(self, title, msg, since, until, target=None):
        """
        Args:
            title (str): Message title that will be searched.
            msg (str): Message that will be searched.
            since (datetime): Datetime from which will be mail searched.
            until (datetime): Datetime until which will be mail searched.
            target (float): Targeted value that will be compared with found
                value in message.

        Returns:
            int: Number of found messages.
        """
        since_timestamp = since.timestamp()
        until_timestamp = self.get_until_timestamp(until)

        LOGGER.debug("Messages are searched from '{0}' until '{1}'".format(
            since_timestamp, until_timestamp))
        messages = usmqe.usmmail.get_msgs_by_time(
            start_timestamp=since_timestamp,
            end_timestamp=until_timestamp,
            host=self.client,
            user=self.user)

        message_count = 0
        matches = []
        for message in messages:
            LOGGER.debug("Message date: '{}'".format(message['Date']))
            LOGGER.debug("Message subject: '{}'".format(message['Subject']))
            msg_payload = message.get_payload(decode=True).decode("utf-8")
            LOGGER.debug("Message body: '{}'".format(msg_payload))

            def save_and_replace(match):
                matches.append(match)
                return '$value'
            msg_payload = self.prc_pattern.sub(save_and_replace, msg_payload)
            try:
                prc_value = matches.pop().group(0)
            except Exception:
                prc_value = None
            LOGGER.debug("Percent value: {}".format(prc_value))
            if message['Subject'].count(
                    title) == 1 and msg_payload.count(msg) == 1:
                if target:
                    if not self.compare_prc(prc_value, target):
                        LOGGER.debug("Message found but with wrong value:"
                                     "'{}'".format(prc_value))
                        message_count -= 1
                message_count += 1
        return message_count

    def search_snmp(self, msg, since, until, target=None):
        """
        Args:
            msg (str): Message that will be searched.
            since (datetime): Datetime from which will be message searched.
            until (datetime): Datetime until which will be message searched.
            target (float): Targeted value that will be compared with found
                value in message.

        Returns:
            int: Number of found messages.
        """
        since_timestamp = since.timestamp()
        until_timestamp = self.get_until_timestamp(until)

        LOGGER.debug("Messages are searched from '{0}' until '{1}'".format(
            since_timestamp, until_timestamp))
        SSH = usmqe.usmssh.get_ssh()
        journal_cmd = "journalctl --since \"$(date \"+%Y-%m-%d %H:%M:%S\" -d"\
            " @{})\" --until \"$(date \"+%Y-%m-%d %H:%M:%S\" -d @{})\"" \
            " -u snmptrapd".format(
                int(since_timestamp), int(until_timestamp))
        rcode, stdout, stderr = SSH[self.client].run(journal_cmd)
        if rcode != 0:
            raise OSError(stderr.decode("utf-8"))
        messages = stdout.decode("utf-8").split("\n")
        # remove header from journalctl output
        del messages[0]

        message_count = 0
        matches = []
        LOGGER.debug("SNMP message expected: '{}'".format(msg))
        for message in messages:
            if message == '':
                continue
            LOGGER.debug("SNMP message: '{}'".format(message))

            def save_and_replace(match):
                matches.append(match)
                return '$value'
            msg_payload = self.prc_pattern.sub(save_and_replace, message)
            try:
                prc_value = matches.pop().group(0)
            except Exception:
                prc_value = None
            LOGGER.debug("Percent value: {}".format(prc_value))
            if msg_payload.count(msg) == 1:
                if target:
                    if not self.compare_prc(prc_value, target):
                        LOGGER.debug("Message found but with wrong value:"
                                     "'{}'".format(prc_value))
                        message_count -= 1
                message_count += 1
        return message_count

    def search_api(self, severity, msg, since, until, target=None):
        """
        For this to work there have to be running test_setup.alerts_logger.yml`
        from usmqe-setup repository.

        Args:
            severity (str): Alert severity.
            msg (str): Message that will be searched.
            since(datetime): Datetime from which will be alert searched.
            until(datetime): Datetime until which will be alert searched.
            target (float): Targeted value that will be compared with found
                value in message.

        Returns:
            int: Number of found messages.
        """
        since_timestamp = since.timestamp()
        until_timestamp = self.get_until_timestamp(until)

        LOGGER.debug("Messages are searched from '{0}' until '{1}'".format(
            since_timestamp, until_timestamp))
        SSH = usmqe.usmssh.get_ssh()
        journal_cmd = "journalctl --since \"$(date \"+%Y-%m-%d %H:%M:%S\" -d"\
            " @{})\" --until \"$(date \"+%Y-%m-%d %H:%M:%S\" -d @{})\"" \
            " -u usmqe_alerts_logger@{}".format(
                int(since_timestamp), int(until_timestamp), self.user)
        rcode, stdout, stderr = SSH[self.client].run(journal_cmd)
        if rcode != 0:
            raise OSError(stderr.decode("utf-8"))

        messages = stdout.decode("utf-8").split("\n")
        # remove header from journalctl output
        del messages[0]

        message_count = 0
        matches = []
        LOGGER.debug("Api message expected: '{}'".format(msg))
        severity_re = re.compile("severity': u'(.*?)'")
        message_re = re.compile("message': u'(.*?)'")
        for message in messages:
            if message == '':
                continue

            LOGGER.debug("Api message: '{}'".format(message))
            msg_severity = severity_re.findall(message)
            if len(msg_severity) != 1:
                LOGGER.info("Incorrect number of severity options: {}".format(
                    msg_severity))
                continue
            msg_severity = msg_severity[0]
            LOGGER.info("Found severity: {}".format(msg_severity))
            msg_payload = message_re.findall(message)
            if len(msg_payload) != 1:
                LOGGER.info("Incorrect number message payloads: {}".format(
                    msg_payload))
                continue
            msg_payload = msg_payload[0]
            LOGGER.info("Found message: {}".format(msg_payload))

            def save_and_replace(match):
                matches.append(match)
                return '$value'
            msg_payload = self.prc_pattern.sub(save_and_replace, msg_payload)
            try:
                prc_value = matches.pop().group(0)
            except Exception:
                prc_value = None
            LOGGER.debug("Percent value: {}".format(prc_value))
            if msg_severity == severity:
                if msg_payload == msg:
                    if target:
                        if not self.compare_prc(prc_value, target):
                            LOGGER.debug("Message found but with wrong value:"
                                         "'{}'".format(prc_value))
                            message_count -= 1
                    message_count += 1
        return message_count
