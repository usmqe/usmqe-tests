"""
Library for direct access to gluster commands.

.. moduleauthor:: fbalak@redhat.com

Quick example of usage::

    from usmqe.gluster import gluster

    gluster_cl = gluster_cluster.GlusterVolume(cluster_id)
    gluster_cl.info()
    ...
"""


import xml.etree.ElementTree

import pytest

from usmqe.gluster.commands import (
    GlusterCommand,
    GlusterCommandErrorException,
    GlusterVolumeCommand
)
import usmqe.inventory
from config.usmqe_config import UsmConfig


LOGGER = pytest.get_logger('gluster_cluster', module=True)
config = UsmConfig()


class GlusterCommon(object):
    """
    Class representing Gluster cluster.
    """

    def __init__(self, cluster=None):
        """
        Initialize GlusterCommon object.

        Args:
            cluster: cluster name or dict with ``name`` key or
                     :py:class:`CephCommon`/:py:class:`CephCluster` object
        """
        self.cmd = GlusterCommand()
        self.cluster = cluster

    def run_on_node(self, command, node=None, executor=None,
                    parse_output=xml.etree.ElementTree.fromstring):
        """
        Run command on gluster node
        """
        last_error = None
        output = None
        if node is None:
            node = config.config["tests"]["usm_cluster_member"]
        if not node:
            raise GlusterCommandErrorException(
                "Problem with gluster command '%s'.\n"
                "Possible problem is no gluster-node (gluster_node list: %s)" %
                (command, config.config["tests"]["usm_cluster_member"]))
        if not executor:
            executor = self.cmd
        try:
            output = executor.run(node, command)
        except GlusterCommandErrorException as err:
            last_error = err
        if last_error:
            raise GlusterCommandErrorException(
                "Problem with gluster command '%s'.\n"
                "Last command rcode: %s, stdout: %s, stderr: %s" %
                (last_error.cmd, last_error.rcode,
                 last_error.stdout, last_error.stderr))

        if parse_output:
            output = parse_output(output)
        return output

    def run_on_all_nodes(self, command, nodes=None, executor=None,
                         parse_output=xml.etree.ElementTree.fromstring):
        """
        Run command on all gluster nodes
        """
        last_error = None
        output = None
        if nodes is None:
            nodes = usmqe.inventory.role2hosts(config.config["tests"]["usm_gluster_role"])
        if not executor:
            executor = self.cmd
        for node in nodes:
            try:
                output = executor.run(node, command)
            except GlusterCommandErrorException as err:
                last_error = err
                continue
            break
        else:
            if last_error:
                raise GlusterCommandErrorException(
                    "Problem with gluster command '%s'.\n"
                    "Last command rcode: %s, stdout: %s, stderr: %s" %
                    (last_error.cmd, last_error.rcode,
                     last_error.stdout, last_error.stderr))
            else:
                raise GlusterCommandErrorException(
                    "Problem with gluster command '%s'.\n"
                    "Possible problem is no gluster-node (gluster_node list: %s)" %
                    (command, usmqe.inventory.role2hosts(config.config["tests"]["usm_gluster_role"])))

        if parse_output:
            output = parse_output(output)
        return output

    def get_volume_names(self):
        """
        Returns list of volume names.
        """
        vol_names = [vn.text for vn in self.run_on_node(command="list").findall(
            "./volList/volume")]
        LOGGER.debug("Volume_names: %s", vol_names)
        return vol_names

    def get_hosts_from_trusted_pool(self, host=None):
        """
        Returns host names from trusted pool with given hostname.
        """
        # TODO change to right path to hostnames
        if host is None:
            host = config.config["tests"]["usm_cluster_member"]
        hosts = self.run_on_node(node=host, command="peer status").findall(
            "./peerStatus/peer/hostnames/hostname")
        hosts = [x.text for x in hosts]
        hosts.append(host)
        LOGGER.debug("Hosts in trusted pool: %s" % hosts)
        return hosts

    def get_cluster_hosts_connection_states(self, host):
        """
        Returns dictionary of hosts where key is hostname and value is host
        status of connectivity from trusted pool with given hostname.
        """
        hosts = self.run_on_node(node=host, command="peer status").findall(
            "./peerStatus/peer")
        states = {}
        states[host] = True
        for host in hosts:
            if host.find("connected").text == "1":
                states[host.find("hostnames/hostname").text] = True
            else:
                states[host.find("hostnames/hostname").text] = False
        LOGGER.debug("Host connectivity in trusted pool: %s" % states)
        return states

    def find_volume_name(self, name, expected=True):
        """
        Check if there is volume with given name.
        """
        volume_name = self.get_volume_names()
        found = False
        # TODO test what vol_name looks like when there are more volumes name
        if expected:
            pytest.check(
                name in volume_name if isinstance(volume_name, list) else volume_name == name,
                "{} should be among volumes from output \
                of gluster volume info command".format(name))
        else:
            pytest.check(
                name not in volume_name if isinstance(volume_name, list) else volume_name != name,
                "{} should not be among volumes from output \
                of gluster volume info command".format(name))
        return found


class GlusterVolume(GlusterCommon):
    """
    Class representing gluster volume.
    """

    def __init__(self, volume_name=None, cluster=None):
        """
        Initialize GlusterCluster object.

        Args:
            cluster: cluster name
            volume_name: volume name
        """
        super().__init__(cluster)
        self.name = volume_name
        self.cmd = GlusterVolumeCommand()
        self.status = None
        self.id = None
        self.stripe_count = None
        self.replica_count = None
        self.brick_count = None
        self.snap_count = None

#    @property
#    def node(self):
#        """
#        Property node returns initialized :py:class:`CephClusterMon` object.
#        """
#        if not self._node:
#            self._node = GlusterVolumeNode(self)
#        return self._node

    def info(self):
        """
        Run gluster command: ``gluster volume info``
        with volume name specified by class.
        """

        xml = self.run_on_node('info {}'.format(self.name))
        self.id = xml.findtext("./volInfo/volumes/volume/id")
        LOGGER.debug("Volume_id: %s" % self.id)
        self.status = xml.findtext(
            "./volInfo/volumes/volume/statusStr")
        self.stripe_count = xml.findtext(
            "./volInfo/volumes/volume/stripeCount")
        self.replica_count = xml.findtext(
            "./volInfo/volumes/volume/replicaCount")
        self.brick_count = xml.findtext(
            "./volInfo/volumes/volume/brickCount")
        self.snap_count = xml.findtext(
            "./volInfo/volumes/volume/snapshotCount")
        # parse bricks informations
        self.bricks = [
                brick.text for brick in xml.findall('./volInfo/volumes/volume/bricks/brick')]

        LOGGER.debug("Volume_status: %s" % self.status)

    def get_volume_id(self):
        """
        Returns id of volume with given name.
        """
        if not self.id:
            self.info()
        return self.id

    # TODO do it universal with name checking
    def check_status(self, status="Started"):
        """
        Check if volume status corresponds with specified status.
        """
        self.info()
        real_status = self.status
        pytest.check(
            status == real_status,
            "Volume status is {}, should be {}".format(real_status, status))
