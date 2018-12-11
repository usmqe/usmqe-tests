import pytest
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
    def __init__(self, user, client=None, server=None, msg_templates=None):
        """
        Args:
            user (str): Tendrl user that receives alerts.
            client (str): Machine address with SNMP and SMTP client.
            server (str): Machine where Tendrl runs.
            msg_templates (dict): Tendrl messages can be overwritten but for
            tendrl testing should be used `basic_messages()`.
        """
        self.user = user
        self.client = client or CONF.inventory.get_groups_dict()["usm_client"][0]
        self.server = server or CONF.inventory.get_groups_dict()["usm_server"][0]
        self.msg_templates = msg_templates or self.basic_messages()
        # uses EXTRA_TIME if is set up
        self.wait = True

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
                "status": "Peer $node in cluster $cluster is $value",
                "cpu": "Cpu utilization on node $node in $cluster $value",
                "memory": "Memory utilization on node $node in $cluster $value",
                "swap": "Swap utilization on node $node in $cluster $value",
                "georeplication": "Geo-replication between $node:$path and $volume is $value"},
            "brick": {
                "status": "Brick:$node:$path in volume:$volume has $value",
                "utilization": "Brick utilization on $node:$path in $volume $value"},
            "cluster": {
                "status": "Cluster:$cluster is $value"},
            "glustershd": {
                "status": "Service: glustershd is $value in cluster $cluster"},
            "volume": {
                "running": "Volume:$volume is $value",
                "status": "Status of volume: $volume in cluster $cluster changed $value"}}


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
            str: Alert message.
        """
        message = "[{0}] ".format(level)
        message = Template(message + self.msg_templates[domain][subject])
        return message.safe_substitute(entities)

    def search_mail(self, since, until, msg):
        """
        Args:
            since (datetime): Datetime from which will be mail searched.
            until (datetime): Datetime until which will be mail searched.
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

        messages = usmqe.usmmail.get_msgs_by_time(
            start_timestamp=since_timestamp,
            end_timestamp=until_timestamp,
            host=self.client,
            user=self.user)

        message_count = 0
        for message in messages:
            LOGGER.debug("Message date: {}".format(message['Date']))
            LOGGER.debug("Message subject: {}".format(message['Subject']))
            LOGGER.debug("Message body: {}".format(message.get_payload(decode=True)))
            if message['Subject'].count(msg) > 0:
                message_count += 1
        return message_count

    def search_snmp():
        pass

    def search_api(self, since, until, msg):
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
