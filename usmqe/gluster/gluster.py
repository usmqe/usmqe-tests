"""
Library for direct access to gluster commands.

.. moduleauthor:: fbalak@redhat.com

Quick example of usage::

    from usmqe.gluster import gluster

    gluster_cl = gluster_cluster.CephCluster(CLUSTER_NAME)
    gluster_cl.status()
    gluster_cl.report()
    ...
    gluster_cl.mon.stat()
    gluster_cl.mon.dump()
    ...
    gluster_cl.osd.stat()
    gluster_cl.osd.df()
    gluster_cl.osd.dump()
    ...
    gluster_cl.rados.df()
    gluster_cl.rados.lspools()
    ...
"""


import json
import re
import xml.etree.ElementTree

import pytest

from usmqe.gluster.commands import GlusterCommand, GlusterCommandErrorException
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

    def run_on_node(self, command, nodes=None, executor=None,
                   parse_output=xml.etree.ElementTree.fromstring):
        """
        Run command on gluster node
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
            except CephCommandErrorException as err:
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


class GlusterVolume(GlusterCommon):
    """
    Class representing gluster cluster.
    """

    def __init__(self, cluster):
        """
        Initialize CephCluster object.

        Args:
            cluster: cluster name or dict with ``name`` key or
                     :py:class:`CephCommon`/:py:class:`CephCluster` object
        """
        super(GlusterCluster, self).__init__(cluster)

    @property
    def node(self):
        """
        Property node returns initialized :py:class:`CephClusterMon` object.
        """
        if not self._node:
            self._node = GlusterVolumeNode(self)
        return self._node

    def info(self):
        """
        Run gluster command: ``gluster volume info``

        Returns:
            dictionary: parsed json from
                        ``gluster --format json --cluster CLUSTERNAME status``
                        command

        Example output (only root elements)::

            { 'election_epoch': 6,
              'fsid': 'aaaaaaaa-bbbb-cccc-ddddddddddddddddd',
              'health': {...},
              'mdsmap': {...},
              'monmap': {...},
              'osdmap': {...},
              'pgmap': {...},
              'quorum': [0, 1, 2],
              'quorum_names': ['b', 'c', 'a'],}
        """
        return self.run_on_node('info')
