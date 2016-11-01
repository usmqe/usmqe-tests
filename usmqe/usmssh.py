"""
Module for establishing remote ssh connection.

.. moduleauthor:: dahorak (inspired by aloganat's module)

Usage::

    # configure SSH keyfile (once in e.g. run.py)
    # default set to ~/.ssh/id_rsa
    import usmssh
    usmssh.KEYFILE = "/path/to/id_rsa"

    # ...use SSH connection in any module...
    # and close all open ssh connections at the end
    ssh = usmssh.get_ssh()
    ssh.finish()

    # ...use SSH in any module
    SSH = usmssh.get_ssh()
    SSH["host.example.com"].run("ls -l")
"""


import os

import plumbum
import pytest


LOGGER = pytest.get_logger("ssh", module=True)
KEYFILE = "~/.ssh/id_rsa"
__SSH = None


def get_ssh():
    """
    Return SSH object.
    """
    # pylint: disable=W0603
    global __SSH
    if not __SSH:
        __SSH = SSHConnections()
    return __SSH


class SSHConnections(object):
    """
    Class for remote commands.
    """

    # pylint: disable=R0903
    def __init__(self):
        self.__connections = {}

    def __getitem__(self, node):
        if node not in self.__connections:
            self.__connections[node] = RemoteConnection(node)
        return self.__connections[node]

    def finish(self):
        """
        Close all open connections.
        """
        for ssh_node in self.__connections.values():
            ssh_node.finish()


class RemoteConnection(object):
    """
    Class for establishing remote ssh connection for one user to one host.
    """

    def __init__(self, node, user='root'):
        """
        Initializes and establishes connection for one user to one host.
        It excepts properly configured KEYFILE variable.

        Parameters:
          * node - hostname
          * user - user (default 'root')
        """
        self.node = node
        self.user = user
        self.keyfile = KEYFILE
        self.establish_connection(
            self.node, user=self.user, keyfile=self.keyfile)

    def establish_connection(self, node, user='root', keyfile=None):
        """
        Establishes connection from localhost to node via plumbum.SshMachine.
        """
        try:
            self.ssh = plumbum.SshMachine(
                node, user, keyfile=os.path.expanduser(keyfile),
                ssh_opts=('-o StrictHostKeyChecking=no',),
                scp_opts=('-o StrictHostKeyChecking=no',))
            self.session = self.ssh.session()
        except Exception as ex:
            msg = "Unable to establish connection with: %s, reason: %s"
            raise RemoteException(msg % (node, ex))

    def run(self, cmd, verbose=True):
        """
        Run the specified command on remote machine.

        Parameters:
          * cmd - (string) command to run
          * verbose - (bool) log output of executed command

        Returns a tuple of (retcode, stdout, stderr) of the command.
        """
        LOGGER.info("Executing '%s' on %s", cmd, self.node)
        proc = self.session.popen(cmd)
        stdout, stderr = proc.communicate()
        retcode = proc.returncode

        if verbose or retcode != 0:
            LOGGER.debug("\"%s\" on %s: RETCODE is %d", cmd, self.node, retcode)
            if stdout != "" and verbose:
                LOGGER.debug("\"%s\" on %s: STDOUT is %s", cmd, self.node, stdout)
            if stderr != "" and verbose:
                LOGGER.debug("\"%s\" on %s: STDERR is %s", cmd, self.node, stderr)
        return (retcode, stdout, stderr)

    def finish(self):
        """
        Destroy all stored connections to user@remote-machine
        """
        try:
            LOGGER.info("Closing connection to %s@%s", self.user, self.node)
            self.session.close()
            self.ssh.close()

        except IOError as ex:
            msg = "Problem occurred in closing remote connections: %s"
            raise RemoteException(msg % ex)


class RemoteException(Exception):
    """
    Exception for ssh/remote connection issues.
    """
