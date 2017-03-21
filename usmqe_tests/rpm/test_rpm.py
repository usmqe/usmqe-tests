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
