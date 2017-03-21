# -*- coding: utf8 -*-

import os
import tempfile
import textwrap

import pytest
import requests
import subprocess


@pytest.fixture
def rpm_repo():
    """
    Check if we can connect to the repo. If not, this issue will be immediately
    reported during setup so that the test case will end up in ERROR state
    (instead of FAILED if we were checking this during test itself).
    """
    baseurl = pytest.config.getini("usm_rpm_baseurl")
    reg = requests.get(baseurl)
    pytest.check(reg.status_code == 200)
    return baseurl


@pytest.fixture(params=[
    "tendrl-commons",
    "tendrl-node-agent",
    "tendrl-ceph-integration",
    "tendrl-gluster-integration",
    "tendrl-api",
    "tendrl-dashboard",
    "tendrl-node-monitoring",
    "tendrl-performance-monitoring",
    ])
def rpm_package(request, rpm_repo):
    """
    Fixture downloads given rpm package from given repository
    and returns it's local path to the test. Downloaded package
    is deleted later during tear down phase.
    """
    with tempfile.TemporaryDirectory() as tmpdirname:
        # name of rpm package under test
        rpm_name = request.param
        # we need to trick yumdownloader into thinking that rpm repo is enabled
        # in the system
        yum_repos_d = os.path.join(tmpdirname, "chroot", "etc", "yum.repos.d")
        os.makedirs(yum_repos_d)
        repofile_template = textwrap.dedent("""
        [tmp]
        name=Temporary Repository
        baseurl={}
        enabled=1
        """)
        with open(os.path.join(yum_repos_d, "tmp.repo"), "w") as repofile:
            repofile.write(repofile_template.format(rpm_repo))
        # create directory where we downdload the package
        # so that we can assume that in this directory is only single
        # file - downloaded rpm package
        os.mkdir(os.path.join(tmpdirname, "rpms"))
        # (hopefully) download the package
        cmd = [
            "yumdownloader",
            "--installroot={}".format(os.path.join(tmpdirname, "chroot")),
            "--destdir={}".format(os.path.join(tmpdirname, "rpms")),
            rpm_name]
        status = subprocess.run(cmd)
        pytest.check(status.returncode == 0)
        # and check file in rpms directory
        rpms_list = os.listdir(os.path.join(tmpdirname, "rpms"))
        pytest.check(len(rpms_list) == 1)
        file_name = rpms_list[0]
        pytest.check(file_name.endswith("rpm"))
        rpm_path = os.path.join(tmpdirname, "rpms", file_name)
        yield rpm_name, rpm_path
