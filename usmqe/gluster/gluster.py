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


LOGGER = pytest.get_logger('gluster_cluster', module=True)


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
            node = usmqe.inventory.role2hosts("gluster")[0]
        if not node:
            raise GlusterCommandErrorException(
                "Problem with gluster command '%s'.\n"
                "Possible problem is no gluster-node (gluster_node list: %s)" %
                (command, usmqe.inventory.role2hosts("gluster")[0]))
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
            nodes = usmqe.inventory.role2hosts("gluster")
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
                    (command, usmqe.inventory.role2hosts("gluster")))

        if parse_output:
            output = parse_output(output)
        return output

    def get_volume_names(self):
        """
        Returns name(s) of volume.
        TODO specify order or some search if more volumes
        """
        vol_name = self.run_on_node(command="volume info").findtext(
            "./volInfo/volumes/volume/name")
        LOGGER.debug("Volume_name: %s" % vol_name)
        return vol_name

    def get_hosts_from_trusted_pool(self, host):
        """
        Returns host names from trusted pool with given hostname.
        """
        # TODO change to right path to hostnames
        hosts = self.run_on_node(node=host, command="peer status").findall(
            "./peerStatus/peer/hostnames/hostname")
        hosts = [x.text for x in hosts]
        hosts.append(host)
        LOGGER.debug("Hosts in trusted pool: %s" % hosts)
        return hosts

    def find_volume_name(self, name, expected=True):
        """
        Check if there is volume with given name.
        """
        volume_name = self.get_volume_names()
        found = False
        # TODO test what vol_name looks like when there are more volumes name
        if isinstance(volume_name, list):
            for item in volume_name:
                # TODO use pytest.check in if?
                if item == name:
                    found = True
        else:
            if volume_name == name:
                found = True
        if expected:
            pytest.check(
                found,
                "If {} is among volumes from output \
                of gluster volume info command".format(name))
        else:
            pytest.check(
                not found,
                "If {} is not among volumes from output \
                of gluster volume info command".format(name))
        return found

    # TODO do it universal with name checking
    def check_status(self, name, status="Started"):
        """
        Check if volume status corresponds with specified status.
        """
        real_status = self.run_on_node(command="volume info").findtext(
            "./volInfo/volumes/volume/statusStr")
        LOGGER.debug("Volume_status: %s" % real_status)
        pytest.check(status == real_status)


class GlusterVolume(GlusterCommon):
    """
    Class representing gluster cluster.
    """

    def __init__(self, cluster):
        """
        Initialize GlusterCluster object.

        Args:
            cluster: cluster name
        """
        super(GlusterCommon, self).__init__(cluster)
        self.cmd = GlusterVolumeCommand()

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

        Returns:
            dictionary: parsed json from
                        ``gluster --format json --cluster CLUSTERNAME status``
                        command
        """
        return self.run_on_node('info')
