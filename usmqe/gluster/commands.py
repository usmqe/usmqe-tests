"""
Library for direct access to gluster commands.

.. moduleauthor:: fbalak@redhat.com
"""

import pytest

import usmqe.usmssh


LOGGER = pytest.get_logger('usmgluster.commands', module=True)
SSH = usmqe.usmssh.get_ssh()


class GlusterCommand(object):
    """
    gluster commands class
    """

    def __init__(self):
        """
        Run gluster command.
        """
        self._format_str = '--xml'
        self._timeout = 3
        self._base_command = 'gluster'

    def cmd(self, command):
        """
        Prepare gluster command.
        """
        return "{} {} {}".format(
            self._base_command, command, self._format_str)

    def run(self, host, command):
        """
        Run gluster command and parse output.
        """
        cmd = self.cmd(command)
        rcode, stdout, stderr = SSH[host].run(cmd)

        if rcode != 0:
            raise GlusterCommandErrorException(
                'Gluster command "{}" failed (rcode={})'.format(cmd, rcode),
                cmd=cmd, rcode=rcode, stdout=stdout.decode(),
                stderr=stderr.decode())
        output = stdout.decode()
        return output


class GlusterVolumeCommand(GlusterCommand):
    """
    gluster volume related commands class
    """

    def __init__(self, cluster=None, conf=None):
        """
        Run gluster command.
        """
        super(GlusterVolumeCommand, self).__init__()
        self._base_command = 'gluster volume'

    def cmd(self, command):
        """
        Prepare gluster command.
        """
        cmd = "{} {} {}".format(
            self._base_command, self._format_str, command)
        return cmd


class GlusterCommandErrorException(Exception):
    """
    Gluster command error exception.
    """

    def __init__(self, message, cmd=None, rcode=None, stdout=None,
                 stderr=None):
        """
        Initialize base exception and save rcode, stdout and stderr.
        """
        # Call the base class constructor with the parameters it needs
        super(GlusterCommandErrorException, self).__init__(message)
        # save additional data
        self.cmd = cmd
        self.rcode = rcode
        self.stdout = stdout
        self.stderr = stderr
