"""
Library for direct access to ceph commands.
NOTE: If user would like to use this module with different key than id_rsa,
it should be imported inside testcase and not in usual python import section

.. moduleauthor:: dahorak@redhat.com
.. moduleauthor:: mkudlej@redhat.com
"""

import pytest

import usmqe.usmssh


LOGGER = pytest.get_logger('usmceph.commands', module=True)
usmqe.usmssh.KEYFILE = "~/.ssh/id_rsa"
try:
    usmqe.usmssh.KEYFILE = pytest.config.getini("usm_ssh_keyfile")
except ValueError:
    pass
SSH = usmqe.usmssh.get_ssh()


class CephCommand(object):
    """
    ceph commands class
    """

    def __init__(self):
        """
        Run ceph command.
        """
        self._format = 'json'
        self._timeout = 3
        self._base_command = 'ceph'

    def cmd(self, command):
        """
        Prepare ceph command.
        """
        format_str = "--format {}".format(self._format) if self._format else ""
        timeout_str = "--connect-timeout {}".format(self._timeout) \
                      if self._timeout else ""
        cmd = "{} {} {} {}".format(
            self._base_command, timeout_str, format_str, command)
        # TODO EOL workaround because of https://bugzilla.redhat.com/show_bug.cgi?id=1448057
        if self._format == 'json':
            cmd = "{} {}".format(cmd, "; echo ''")
        return cmd

    def run(self, host, command):
        """
        Run ceph command and parse output.
        """
        cmd = self.cmd(command)
        rcode, stdout, stderr = SSH[host].run(cmd)

        if rcode != 0:
            raise CephCommandErrorException(
                'Ceph command "{}" failed (rcode={})'.format(cmd, rcode),
                cmd=cmd, rcode=rcode, stdout=stdout.decode(),
                stderr=stderr.decode())
        output = stdout.decode()
        return output


class CephClusterCommand(CephCommand):
    """
    ceph cluster related commands class
    """

    def __init__(self, cluster=None, conf=None):
        """
        Run ceph command.
        """
        super(CephClusterCommand, self).__init__()
        self._cluster = cluster
        self._conf = conf

    def cmd(self, command):
        """
        Prepare ceph command.
        """
        format_str = "--format {}".format(self._format) if self._format else ""
        cluster_str = "--cluster {}".format(self._cluster) \
                      if self._cluster else ""
        conf_str = "--conf {}".format(self._conf) if self._conf else ""
        timeout_str = "--connect-timeout {}".format(self._timeout) \
                      if self._timeout else ""

        cmd = "{} {} {} {} {} {}".format(
            self._base_command, timeout_str, format_str, cluster_str,
            conf_str, command)
        # TODO EOL workaround because of https://bugzilla.redhat.com/show_bug.cgi?id=1448057
        if self._format == 'json':
            cmd = "{} {}".format(cmd, "; echo ''")
        return cmd


class RadosCommand(CephCommand):
    """
    rados related commands class
    """

    def __init__(self, cluster=None, conf=None):
        """
        Run rados command.
        """
        super(RadosCommand, self).__init__()
        self._base_command = 'rados'
        self._cluster = cluster
        self._conf = conf

    def cmd(self, command):
        """
        Prepare rados command.
        """
        cluster_str = "--cluster {}".format(self._cluster) \
                      if self._cluster else ""
        conf_str = "--conf {}".format(self._conf) if self._conf else ""
        format_str = "--format {}".format(self._format) if self._format else ""

        cmd = "{} {} {} {} {}".format(
            self._base_command, format_str, cluster_str, conf_str, command)
        # TODO EOL workaround because of https://bugzilla.redhat.com/show_bug.cgi?id=1448057
        if self._format == 'json':
            cmd = "{} {}".format(cmd, "; echo ''")
        return cmd


class RBDCommand(CephCommand):
    """
    rbd related commands class
    """

    def __init__(self, cluster=None, conf=None, pool=None):
        """
        Run rbd command.
        """
        super(RBDCommand, self).__init__()
        self._base_command = 'rbd'
        self._cluster = cluster
        self._conf = conf
        self._pool = pool

    def cmd(self, command):
        """
        Prepare rbd command.
        """
        cluster_str = "--cluster {}".format(self._cluster) \
                      if self._cluster else ""
        conf_str = "--conf {}".format(self._conf) if self._conf else ""
        format_str = "--format {}".format(self._format) if self._format else ""
        pool_str = "--pool {}".format(self._pool) if self._pool else ""

        cmd = "{} {} {} {} {} {}".format(
            self._base_command, format_str, cluster_str,
            conf_str, pool_str, command)
        # TODO EOL workaround because of https://bugzilla.redhat.com/show_bug.cgi?id=1448057
        if self._format == 'json':
            cmd = "{} {}".format(cmd, "; echo ''")
        return cmd


class CephCommandErrorException(Exception):
    """
    Ceph command error exception.
    """

    def __init__(self, message, cmd=None, rcode=None, stdout=None,
                 stderr=None):
        """
        Initialize base exception and save rcode, stdout and stderr.
        """
        # Call the base class constructor with the parameters it needs
        super(CephCommandErrorException, self).__init__(message)
        # save additional data
        self.cmd = cmd
        self.rcode = rcode
        self.stdout = stdout
        self.stderr = stderr
