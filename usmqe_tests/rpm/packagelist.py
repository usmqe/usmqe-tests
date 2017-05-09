# -*- coding: utf8 -*-

import configparser
import subprocess


# list of all tendrl packages
tendrl_packages = [
    "tendrl-alerting",
    "tendrl-api",
    "tendrl-api-doc",
    "tendrl-api-httpd",
    "tendrl-ceph-integration",
    "tendrl-commons",
    "tendrl-dashboard",
    "tendrl-gluster-integration",
    "tendrl-node-agent",
    "tendrl-node-monitoring",
    "tendrl-performance-monitoring",
    ]


# name of usmqe config option (as in usm.ini file) for given tendrl reponame
reponame2gpgkey_confname = {
    "tendrl-core": "usm_core_gpgkey_url",
    "tendrl-deps": "usm_deps_gpgkey_url",
    }
reponame2baseurl_confname = {
    "tendrl-core": "usm_core_baseurl",
    "tendrl-deps": "usm_deps_baseurl",
    }


def list_packages(reponame):
    """
    This helper function returns list of all rpm packages in given repository.
    """
    # try to get baseurl of repository directly from usmqe config file,
    # which is even more TERRIBLE HACK, but I can't help it as pytest.config is
    # not available during of fixture arguments ...
    # TODO: we may want to reconsider design of usmqe configuration
    pytest_ini = configparser.ConfigParser()
    pytest_ini.read_file(open("pytest.ini"))
    usm_config_path = pytest_ini.get("pytest", "usm_config")
    usm_config = configparser.ConfigParser()
    usm_config.read_file(open(usm_config_path))
    # if repo is not defined in config file, we have no packages to check ...
    if (
            "usmqepytest" in usm_config and
            reponame2baseurl_confname[reponame] in usm_config["usmqepytest"]
            ):
        baseurl = usm_config.get(
            "usmqepytest",
            reponame2baseurl_confname[reponame])
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
