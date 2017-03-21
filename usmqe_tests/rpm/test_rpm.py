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
    repoclosure_cmd = ["repoclosure", "--newest"]
    # configure systemd default repositories
    for name, url in CENTOS_REPOS.items():
        repoclosure_cmd.append("--repofrompath")
        repoclosure_cmd.append("{},{}".format(name, url))
        repoclosure_cmd.append("--lookaside={}".format(name))
    # configure tendrl repository (passed via rpm_repo fixture)
    repoclosure_cmd.append("--repofrompath")
    repoclosure_cmd.append("tendrl,{}".format(rpm_repo))
    repoclosure_cmd.append("--repoid=tendrl")
    LOGGER.debug(" ".join(repoclosure_cmd))
    # TODO: log stdout properly
    status = subprocess.run(repoclosure_cmd)
    pytest.check(status.returncode == 0)


def test_rpmlint(rpm_package):
    rpm_name, rpm_path = rpm_package
    LOGGER.info("checking %s", rpm_name)
    cmd = ["rpmlint", rpm_path]
    LOGGER.debug(" ".join(cmd))
    status = subprocess.run(cmd)
    pytest.check(status.returncode == 0)


@pytest.mark.parametrize("check_command", [
    "check-sat",
    "check-conflicts",
    ])
def test_rpmdeplint(rpm_package, check_command, rpm_repo):
    rpm_name, rpm_path = rpm_package
    LOGGER.info("checking %s", rpm_name)
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
    # running the check
    LOGGER.debug(" ".join(cmd))
    status = subprocess.run(cmd)
    pytest.check(status.returncode == 0)
