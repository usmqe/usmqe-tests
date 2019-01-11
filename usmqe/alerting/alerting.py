import pytest
import re
from string import Template
import time
from usmqe.usmqeconfig import UsmConfig
import usmqe.usmmail
import usmqe.usmssh

LOGGER = pytest.get_logger('usmqe_alerting', module=True)
CONF = UsmConfig()

# seconds to wait until alerts are in place
EXTRA_TIME = 30

class Alerting(object):
    """
    Class for alert lookup. Supports alerts from SNMP, SMTP and tendrl api.
    For api lookup there have to run `usmqe_alerts_logger` service on api
    server. This can be installled by `test_setup.alerts_logger.yml` from
    usmqe-setup repository.
    """
    def __init__(self, user, client=None, server=None, msg_templates=None,
            divergence=15.0):
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
        self.client = client or CONF.inventory.get_groups_dict()["usm_client"][0]
        self.server = server or CONF.inventory.get_groups_dict()["usm_server"][0]
        self.msg_templates = msg_templates or self.basic_messages()
        # uses EXTRA_TIME if is set up
        self.wait = True
        self.prc_pattern = re.compile("\d{1,3}(\.\d{1,2})(\s\%)?")
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
            "node":{
                "status": {
                    "subject": "status changed",
                    "body": "Peer $node in cluster $cluster is $value"},
                "cpu": {
                    "subject": "Cpu Utilization: threshold breached",
                    "body": "Cpu utilization on node $node in $cluster $value"},
                "memory": {
                    "subject": "Memory Utilization: threshold breached",
                    "body": "Memory utilization on node $node in $cluster $value"},
                "swap": {
                    "subject": "Swap Utilization: threshold breached",
                    "body": "Swap utilization on node $node in $cluster $value"},
                "georeplication": {
                    "subject": "status changed",
                    "body": "Geo-replication between $node:$path and $volume is $value"},},
            "brick": {
                "status": {
                    "subject": "status changed",
                    "body": "Brick:$node:$path in volume:$volume has $value"},
                "utilization": {
                    "subject": "Brick Utilization: threshold breached",
                    "body": "Brick utilization on $node:$path in $volume $value"},},
            "cluster": {
                "status": {
                    "subject": "status changed",
                    "body": "Cluster:$cluster is $value"},},
            "glustershd": {
                "status": {
                    "subject": "status changed",
                    "body": "Service: glustershd is $value in cluster $cluster"},},
            "volume": {
                "running": {
                    "subject": "status changed",
                    "body": "Volume:$volume is $value"},
                "status": {
                    "subject": "status changed",
                    "body": "Status of volume: $volume in cluster $cluster changed $value"}}}

    def generate_alert_msg(
            self,
            level,
            domain,
            subject,
            entities=None):
        """
        Return alert message based on parameters.

        Args:
            level (str): Severity of message (INFO|WARNING|CRITICAL).
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
        title = "[{0}] {1}".format(level, self.msg_templates[
            domain][subject]['subject'])
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
        if self.wait:
            until_timestamp = until.timestamp() + EXTRA_TIME
            time.sleep(EXTRA_TIME)
            self.wait = False
        else:
            until_timestamp = until.timestamp()

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
            LOGGER.debug("Message body after sub: {}".format(msg_payload))
            try:
                prc_value = matches.pop().group(0)
            except:
                prc_value = None
            LOGGER.debug("Percent value: {}".format(prc_value))
            if message['Subject'].count(
                title) == 1 and msg_payload.count(msg) == 1:
                    if target:
                        if not self.compare_prc(prc_value, target):
                            LOGGER.debug("Message found but with wrong value:"\
                                "'{}'".format(prc_value))
                            message_count -= 1
                    message_count += 1
        return message_count

    def search_snmp(self, msg, since, until):
        """
        Args:
            since(datetime): Datetime from which will be mail searched.
            until(datetime): Datetime until which will be mail searched.
            msg (str): Message that will be searched.

        Returns:
            int: Number of found messages.
        """
        since_timestamp = since.timestamp()
        if self.wait:
            until_timestamp = until.timestamp() + EXTRA_TIME
            time.sleep(EXTRA_TIME)
            self.wait = False
        else:
            until_timestamp = until.timestamp()

        SSH = usmqe.usmssh.get_ssh()
        journal_cmd = "journalctl --since \"{}\" --until \"{}\"" \
            " -u snmptrap".format(
                since_timestamp, until_timestamp, self.user)
        rcode, stdout, stderr = SSH[self.client].run(journal_cmd)
        if rcode != 0:
            raise OSError(stderr.decode("utf-8"))

        messages = stdout.decode("utf-8").split("\n")
        message_count = 0
        for message in messages:
            LOGGER.debug("Message date: {}".format(message['Date']))
            LOGGER.debug("Message subject: {}".format(message['Subject']))
            LOGGER.debug("Message body: {}".format(message.get_payload(decode=True)))
            if message['Subject'].count(msg) > 0:
                message_count += 1
        return message_count

    def search_api(self, msg, since, until):
        """
        For this to work there have to be running test_setup.alerts_logger.yml`
        from usmqe-setup repository.

        Args:
            since(datetime): Datetime from which will be mail searched.
            until(datetime): Datetime until which will be mail searched.
            msg (str): Message that will be searched.

        Returns:
            int: Number of found messages.
        """
        since_timestamp = since.timestamp()
        if self.wait:
            until_timestamp = until.timestamp() + EXTRA_TIME
            time.sleep(EXTRA_TIME)
            self.wait = False
        else:
            until_timestamp = until.timestamp()

        SSH = usmqe.usmssh.get_ssh()
        journal_cmd = "journalctl --since \"{}\" --until \"{}\"" \
            " -u usmqe_alerts_logger@{}".format(
                since_timestamp, until_timestamp, self.user)
        rcode, stdout, stderr = SSH[self.server].run(journal_cmd)
        if rcode != 0:
            raise OSError(stderr.decode("utf-8"))

        messages = stdout.decode("utf-8").split("\n")
        message_count = 0
        for message in messages:
            LOGGER.debug("Message date: {}".format(message['Date']))
            LOGGER.debug("Message subject: {}".format(message['Subject']))
            LOGGER.debug("Message body: {}".format(message.get_payload(decode=True)))
            if message['Subject'].count(msg) > 0:
                message_count += 1
        return message_count
