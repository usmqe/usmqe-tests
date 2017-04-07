# -*- coding: utf8 -*-

import glob
import os
import tempfile
import textwrap

import pytest
import requests
import subprocess


@pytest.fixture(scope="module")
def chroot_dir(rpm_repo):
    """
    Create chroot enviroment for rpm installation test.
    """
    gpgkey_url = pytest.config.getini("usm_rpm_gpgkey_url")
    tmpdirname = tempfile.mkdtemp()
    # create minimal directory tree
    os.makedirs(os.path.join(tmpdirname, "var/lib/rpm"))
    os.makedirs(os.path.join(tmpdirname, "etc/yum.repos.d"))
    os.makedirs(os.path.join(tmpdirname, "tmp"))
    # download repo gpg key of the product we are testing
    req = requests.get(gpgkey_url)
    assert req.status_code == 200
    gpgkey_file = os.path.join(tmpdirname, "tmp", "pubkey.gpg")
    with open(gpgkey_file, "w") as keyfile:
        keyfile.write(req.content.decode())
    # create repo file of the product we are testing
    repofile_path = os.path.join(tmpdirname, "etc/yum.repos.d/tmp.repo")
    repofile_template = textwrap.dedent("""
    [tmp]
    name=Temporary Yum Repository
    baseurl={}
    enabled=1
    gpgkey={}
    gpgcheck=1
    """)
    with open(repofile_path, "w") as repofile:
        repofile.write(repofile_template.format(rpm_repo, gpgkey_url))
    # initialize rpmdb
    rpm_cmd = ["rpm", "--root", tmpdirname, "--initdb"]
    subprocess.run(rpm_cmd, cwd=os.path.join(tmpdirname), check=True)
    # download and install centos-release and epel-release packages
    # in the tmpdirname using default system repositories (we expect to run
    # on CentOS anyway)
    for rpm_name in ("centos-release", "epel-release"):
        yum_cmd = [
            "yumdownloader",
            "--destdir={}".format(os.path.join(tmpdirname, "tmp")),
            rpm_name]
        subprocess.run(yum_cmd, cwd=tmpdirname, check=True)
        files = glob.glob(os.path.join(tmpdirname, "tmp", rpm_name + "*.rpm"))
        assert len(files) == 1
        rpm_path = files[0]
        # note: we expect that current user can do run anything as root via sudo
        # (which is configured in usmqe-setup playbook for qe server role)
        rpm_cmd = [
            "sudo",
            "rpm", "--root", tmpdirname, "-iv", "--nodeps", rpm_path]
        subprocess.run(rpm_cmd, cwd=tmpdirname, check=True)
    # import the gpg keys for all yum repositories
    repo_keys = [
        os.path.join(tmpdirname, "etc/pki/rpm-gpg/RPM-GPG-KEY-CentOS-7"),
        os.path.join(tmpdirname, "etc/pki/rpm-gpg/RPM-GPG-KEY-EPEL-7"),
        os.path.join(tmpdirname, "tmp/pubkey.gpg"),  # product gpg repo key
        ]
    for key in repo_keys:
        cmd = ["rpm", "--root", tmpdirname, "--import", key]
        subprocess.run(cmd, cwd=os.path.join(tmpdirname), check=True)
    # and that's all
    yield tmpdirname
    # teardown:
    # since most files in tmpdirname are owned by root now, let's do the
    # cleanup manually
    cmd = ["sudo", "rm", tmpdirname, "-rf"]
    subprocess.run(cmd, cwd=tmpdirname, check=True)


@pytest.fixture(scope="module")
def centos_repos():
    """
    Hardcoded list of default el7 repositories for upstream use case.

    Check if we can connect to all default repositories. If not, this issue
    will be immediately reported during setup so that the test case will end up
    in ERROR state (instead of FAILED if we were checking this during test
    itself).
    """
    repo_dict = {
        "centos-base": "http://mirror.centos.org/centos/7/os/x86_64/",
        "centos-updates": "http://mirror.centos.org/centos/7/updates/x86_64/",
        "centos-extras": "http://mirror.centos.org/centos/7/extras/x86_64/",
        "fedora-epel": "http://mirror.karneval.cz/pub/linux/fedora/epel/7/x86_64/",
        }
    for url in repo_dict.values():
        reg = requests.get(url)
        assert reg.status_code == 200
    return repo_dict


@pytest.fixture(scope="module")
def rpm_repo():
    """
    Check if we can connect to the repo. If not, this issue will be immediately
    reported during setup so that the test case will end up in ERROR state
    (instead of FAILED if we were checking this during test itself).
    """
    baseurl = pytest.config.getini("usm_rpm_baseurl")
    reg = requests.get(baseurl)
    assert reg.status_code == 200
    return baseurl


@pytest.fixture(scope="module", params=[
    "gstatus",
    "hwinfo",
    "libx86emu1",
    "namespaces",
    "python-etcd",
    "python-maps",
    "python2-ruamel-yaml",
    "rubygem-bundler",
    "rubygem-etcd",
    "rubygem-minitest",
    "rubygem-mixlib-log",
    "rubygem-puma",
    "rubygem-sinatra",
    "rubygem-tilt",
    "tendrl-api",
    "tendrl-api-httpd",
    "tendrl-ceph-integration",
    "tendrl-commons",
    "tendrl-dashboard",
    "tendrl-gluster-integration",
    "tendrl-node-agent",
    "tendrl-node-monitoring",
    "tendrl-performance-monitoring",
    ])
def rpm_package(request, rpm_repo):
    """
    Fixture downloads given rpm package from given repository
    and returns it's local path to the test. Downloaded package
    is deleted later during tear down phase.

    GnuPG signature is not verified during package download.
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
        name=Temporary Yum Repository
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
        subprocess.run(cmd, cwd=tmpdirname, check=True)
        # and check file in rpms directory
        rpms_list = os.listdir(os.path.join(tmpdirname, "rpms"))
        assert len(rpms_list) == 1
        file_name = rpms_list[0]
        assert file_name.endswith("rpm")
        rpm_path = os.path.join(tmpdirname, "rpms", file_name)
        yield rpm_name, rpm_path