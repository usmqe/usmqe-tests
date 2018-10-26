# -*- coding: utf8 -*-

import subprocess

from usmqe.usmqeconfig import UsmConfig


# list of all tendrl packages
tendrl_packages = [
    "carbon-selinux",
    "tendrl-ansible",
    "tendrl-api",
    "tendrl-api-httpd",
    "tendrl-collectd-selinux",
    "tendrl-commons",
    "tendrl-gluster-integration",
    "tendrl-grafana-plugins",
    "tendrl-grafana-selinux",
    "tendrl-monitoring-integration",
    "tendrl-node-agent",
    "tendrl-notifier",
    "tendrl-selinux",
    "tendrl-ui",
    ]


# name of usmqe config option (as in usm.ini file) for given tendrl reponame
reponame2confname = {
    "tendrl-core": "core",
    "tendrl-deps": "deps",
    }


def list_packages(reponame):
    """
    This helper function returns list of all rpm packages in given repository.
    """
    # try to get baseurl of repository directly from usmqe config file,
    # which is even more TERRIBLE HACK, but I can't help it as pytest.config is
    # not available during of fixture arguments ...
    # TODO: we may want to reconsider design of usmqe configuration
    usm_config = UsmConfig()
    # if repo is not defined in config file, we have no packages to check ...
    if (
            "usmqe" in usm_config.config and
            "rpm_repo" in usm_config.config["usmqe"] and
            reponame2confname[reponame] in usm_config.config["usmqe"]["rpm_repo"]
            ):
        baseurl = usm_config.config["usmqe"]["rpm_repo"][reponame2confname[reponame]]["baseurl"]
    else:
        return []
    # list all package names from given repo
    cmd = [
        "repoquery",
        "--repofrompath={},{}".format(reponame, baseurl),
        "--repoid={}".format(reponame),
        "--all",
        "--qf='%{name}'",
        ]
    stdout = subprocess.check_output(cmd)
    rpm_name_list = stdout.decode('utf-8').replace("'", "").split("\n")
    # account for edge case of stdout2list conversion
    if len(rpm_name_list) >= 1 and len(rpm_name_list[-1]) == 0:
        rpm_name_list.pop()
    return rpm_name_list
