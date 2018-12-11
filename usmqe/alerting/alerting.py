from string import Template
from usmqe.usmqeconfig import UsmConfig

CONF = UsmConfig()

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

    def check_mail():
        pass

    def check_snmp():
        pass

    def check_api(api, msg, ):
        pass
