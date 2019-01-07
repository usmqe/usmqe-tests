# -*- coding: utf8 -*-
"""
Pytest plugin for scheduling tasks on nodes.
.. moduleauthor:: Filip Balak <fbalak@redhat.com>
"""
import usmqe.usmssh as usmssh
import datetime
import random
import string


class Scheduler(object):
    """
    Wrapper around `usmssh` module that handles scheduling tasks on multiple
    nodes simultaneously.
    """

    def __init__(self, nodes):
        """
        Args:
            nodes (list): list of nodes used for command scheduling
        """
        self.nodes = nodes
        self.ssh = usmssh.get_ssh()

    def run_at(self, command, time=None):
        """
        Schedule a job on all machines with `at` command.

        Args:
            command (str): Command to be executed.
            time (time): Time to execute. Time has to be in `at` compatible
                format. If None is provided then all commands are executed
                in next minute.
        """
        if not time:
            time = datetime.datetime.utcnow() + datetime.timedelta(minutes=1)
            time = time.strftime("%H:%M")
        files = self.create_job_file(command)
        for node in self.nodes:
            time_command = "at $(date --date='TZ=\"UTC\" {0}' +%H:%M) -f {1} ".format(time, files[node])
            self.ssh[node].run(time_command)

    def create_job_file(self, command):
        """
        Create task file in /tmp directory which can be used by at command.

        Args:
            command (str): Command to be executed.

        Returns:
            dict: Keys are node hostnames and values are file paths.
        """
        files = {}
        for node in self.nodes:
            char_set = string.ascii_lowercase + string.digits
            file_name = "/tmp/schedulertask_{0}".format(
                ''.join(random.sample(char_set*6, 6)))
            create_file_cmd = "echo '#!/bin/sh\n{0}' > {1}".format(
                command,
                file_name)
            retcode, _, stderr = self.ssh[node].run(create_file_cmd)
            if retcode != 0:
                raise OSError(stderr.decode("utf8"))
            files[node] = file_name
        return files

    def jobs(self):
        """
        Get dictionary of job lists where dictionary key is a node.

        Returns:
            dict: Keys are nodes and values are lists containing job position
                and job description.
        """
        jobs = {}
        for node in self.nodes:
            _, stdout, _ = self.ssh[node].run("atq")
            jobs[node] = [job.split("\t") for job in stdout.decode(
                "utf8").rstrip("\n").split("\n")]
        return jobs
