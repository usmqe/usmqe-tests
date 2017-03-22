# -*- coding: utf8 -*-

import pytest
import subprocess


LOGGER = pytest.get_logger(__name__, module=True)


# Hardcoded list of default el7 repositories for upstream use case.
CENTOS_REPOS = {
    "centos-base": "http://mirror.centos.org/centos/7/os/x86_64/",
    "centos-updates": "http://mirror.centos.org/centos/7/updates/x86_64/",
    "centos-extras": "http://mirror.centos.org/centos/7/extras/x86_64/",
    "epel": "http://mirror.karneval.cz/pub/linux/fedora/epel/7/x86_64/",
    }


def test_repoclosure(rpm_repo):
    cmd = ["repoclosure", "--newest"]
    # configure systemd default repositories
    for name, url in CENTOS_REPOS.items():
        cmd.append("--repofrompath")
        cmd.append("{},{}".format(name, url))
        cmd.append("--lookaside={}".format(name))
    # configure tendrl repository (passed via rpm_repo fixture)
    cmd.append("--repofrompath")
    cmd.append("tendrl,{}".format(rpm_repo))
    cmd.append("--repoid=tendrl")
    # running repoclosure
    LOGGER.info(" ".join(cmd))
    cp = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    LOGGER.debug("STDOUT: %s", cp.stdout)
    LOGGER.debug("STDERR: %s", cp.stderr)
    check_msg = "repoclosure return code should be 0 indicating no errors"
    pytest.check(cp.returncode == 0, msg=check_msg)
    # when the check fails, report the error in readable way
    if cp.returncode != 0:
        for line in cp.stdout.splitlines():
            LOGGER.failed(str(line))
        for line in cp.stderr.splitlines():
            LOGGER.failed(str(line))


def test_rpmlint(rpm_package):
    rpm_name, rpm_path = rpm_package
    cmd = ["rpmlint", rpm_path]
    # running rpmlint
    LOGGER.info(" ".join(cmd))
    cp = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    LOGGER.debug("STDOUT: %s", cp.stdout)
    LOGGER.debug("STDERR: %s", cp.stderr)
    check_msg = "rpmlint return code should be 0 indicating no errors"
    pytest.check(cp.returncode == 0, msg=check_msg)
    # when the check fails, report the error in readable way
    if cp.returncode != 0:
        for line in cp.stdout.splitlines():
            LOGGER.failed(str(line))


@pytest.mark.parametrize("check_command", [
    "check-sat",
    "check-conflicts",
    ])
def test_rpmdeplint(rpm_package, check_command, rpm_repo):
    rpm_name, rpm_path = rpm_package
    cmd = ["rpmdeplint", check_command]
    # configure systemd default repositories
    for name, url in CENTOS_REPOS.items():
        cmd.append("--repo")
        cmd.append("{},{}".format(name, url))
    # configure tendrl repository (passed via rpm_repo fixture)
    cmd.append("--repo")
    cmd.append("tendrl,{}".format(rpm_repo))
    # and last but not least: specify the package
    cmd.append(rpm_path)
    # running rpmdeplint
    LOGGER.info(" ".join(cmd))
    cp = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    LOGGER.debug("STDOUT: %s", cp.stdout)
    LOGGER.debug("STDERR: %s", cp.stderr)
    check_msg = "rpmdeplint return code should be 0 indicating no errors"
    pytest.check(cp.returncode == 0, msg=check_msg)
    # when the check fails, report the error in readable way
    if cp.returncode != 0:
        for line in cp.stderr.splitlines():
            LOGGER.failed(str(line))
