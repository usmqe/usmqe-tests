# -*- coding: utf8 -*-

import glob
import os
import pathlib
import subprocess
import tempfile
import textwrap
import urllib

import pytest
import requests

from packagelist import list_packages
from packagelist import reponame2gpgkey_confname, reponame2baseurl_confname


@pytest.fixture(scope="module")
def chroot_dir(tendrl_repos):
    """
    Create chroot enviroment for rpm installation test.
    """
    tmpdirname = tempfile.mkdtemp()
    # create minimal directory tree
    os.makedirs(os.path.join(tmpdirname, "var/lib/rpm"))
    os.makedirs(os.path.join(tmpdirname, "etc/yum.repos.d"))
    os.makedirs(os.path.join(tmpdirname, "tmp"))
    # expected paths for gpg keys of rpm repositories
    repo_keys = [
        os.path.join(tmpdirname, "etc/pki/rpm-gpg/RPM-GPG-KEY-CentOS-7"),
        os.path.join(tmpdirname, "etc/pki/rpm-gpg/RPM-GPG-KEY-EPEL-7"),
        ]
    # download repo gpg key of the product we are testing
    reponame2gpgkey_url = {}
    for name in tendrl_repos.keys():
        try:
            gpgkey_url = pytest.config.getini(reponame2gpgkey_confname[name])
            req = requests.get(gpgkey_url)
            assert req.status_code == 200
            gpgkey_path = os.path.join(tmpdirname, "tmp", name + ".gpg")
            repo_keys.append(gpgkey_path)
            reponame2gpgkey_url[name] = gpgkey_url
            with open(gpgkey_path, "w") as keyfile:
                keyfile.write(req.content.decode())
        except ValueError as ex:
            # ignore exception raised when it is missing in the conf. file
            if "unknown configuration value" not in str(ex):
                raise ex
    # create repo file of the product we are testing
    repofile_path = os.path.join(tmpdirname, "etc/yum.repos.d/tmp.repo")
    repo_template = textwrap.dedent("""
    [{0}]
    name=Temporary Yum Repository for {0}
    baseurl={1}
    enabled=1
    {2}

    """)
    with open(repofile_path, "w") as repofile:
        for name, baseurl in tendrl_repos.items():
            gpgkey_url = reponame2gpgkey_url.get(name)
            if gpgkey_url is None:
                gpgcheck = "gpgcheck=0"
            else:
                gpgcheck = "gpgkey={}\ngpgcheck=1".format(gpgkey_url)
            content = repo_template.format(name, baseurl, gpgcheck)
            repofile.write(content)
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
    # HACK/WORKAROUND: download grafana repo gpg keys
    grafana_gpgkey_urls = [
        "https://packagecloud.io/gpg.key",
        "https://grafanarel.s3.amazonaws.com/RPM-GPG-KEY-grafana",
        ]
    for gpgkey_url in grafana_gpgkey_urls:
        req = requests.get(gpgkey_url)
        name = os.path.basename(gpgkey_url)
        assert req.status_code == 200
        gpgkey_path = os.path.join(tmpdirname, "tmp", name + ".gpg")
        repo_keys.append(gpgkey_path)
        with open(gpgkey_path, "w") as keyfile:
            keyfile.write(req.content.decode())
    # HACK/WORKAROUND: install grafana repo (upstream Tendrl dependency)
    # based on http://docs.grafana.org/installation/rpm/
    grafana_repofile_path = os.path.join(tmpdirname, "etc/yum.repos.d/grafana.repo")
    grafana_repofile_content = textwrap.dedent("""\
    [grafana]
    name=grafana
    baseurl=https://packagecloud.io/grafana/stable/el/6/$basearch
    repo_gpgcheck=1
    enabled=1
    gpgcheck=1
    gpgkey=https://packagecloud.io/gpg.key https://grafanarel.s3.amazonaws.com/RPM-GPG-KEY-grafana
    sslverify=1
    sslcacert=/etc/pki/tls/certs/ca-bundle.crt
    """)
    with open(grafana_repofile_path, "w") as repofile:
        repofile.write(grafana_repofile_content)
    # import the gpg keys for all yum repositories
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
        "gdeploy": "http://copr-be.cloud.fedoraproject.org/results/sac/gdeploy/epel-7-x86_64/",
        "grafana": "https://packagecloud.io/grafana/stable/el/6/x86_64/",
        }
    for url in repo_dict.values():
        reg = requests.get(url)
        assert reg.status_code == 200
    return repo_dict


def get_baseurl(conf_name):
    """
    Retrieve (from usmqe config file) and validate baseurl for given repo.
    """
    conf_value = pytest.config.getini(conf_name)
    baseurl = urllib.parse.urlparse(conf_value)
    # check remote url http://, https:// or ftp://
    if baseurl.scheme in ('http', 'https', 'ftp'):
        reg = requests.get(baseurl.geturl())
        assert reg.status_code == 200
    # check local path file://...
    elif baseurl.scheme in ('file', ):
        base_dir = pathlib.Path(baseurl.path)
        assert base_dir.is_dir()
    else:
        raise ValueError("Unsupported protocol '{}' in '{}': '{}'".format(
            baseurl.scheme, conf_name, baseurl.geturl()))
    return baseurl.geturl()


@pytest.fixture(scope="module")
def tendrl_repos():
    """
    Check if we can connect to the repo. If not, this issue will be immediately
    reported during setup so that the test case will end up in ERROR state
    (instead of FAILED if we were checking this during test itself).
    """
    repo_dict = {
        'tendrl-core': get_baseurl(reponame2baseurl_confname['tendrl-core'])}
    try:
        deps_baseurl = get_baseurl(reponame2baseurl_confname['tendrl-deps'])
        repo_dict['tendrl-deps'] = deps_baseurl
    except ValueError as ex:
        # usm_deps_baseurl is optional
        # ignore exception raised when it is missing in the conf. file
        if "unknown configuration value" in str(ex):
            pass
        else:
            raise ex
    return repo_dict


@pytest.fixture(
    scope="module",
    params=list_packages('tendrl-core') + list_packages('tendrl-deps'))
def rpm_package(request, tendrl_repos):
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
        repo_template = textwrap.dedent("""
        [{0}]
        name=Temporary Yum Repository for {0}
        baseurl={1}
        enabled=1

        """)
        with open(os.path.join(yum_repos_d, "tmp.repo"), "w") as repofile:
            for name, baseurl in tendrl_repos.items():
                repofile.write(repo_template.format(name, baseurl))
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
