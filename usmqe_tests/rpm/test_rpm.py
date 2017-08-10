# -*- coding: utf8 -*-

import subprocess
import tempfile

import pytest

from packagelist import list_packages, tendrl_packages


LOGGER = pytest.get_logger(__name__, module=True)


def test_repoclosure(tendrl_repos, centos_repos):
    cmd = ["repoclosure", "--newest"]
    # configure systemd default repositories
    for name, url in centos_repos.items():
        cmd.append("--repofrompath")
        cmd.append("{},{}".format(name, url))
        cmd.append("--lookaside={}".format(name))
    # configure tendrl repository (passed via tendrl_repos fixture)
    for name, baseurl in tendrl_repos.items():
        cmd.append("--repofrompath")
        cmd.append("{},{}".format(name, baseurl))
        # we expect that other repositories are for dependencies
        if name != "tendrl-core":
            cmd.append("--lookaside={}".format(name))
    cmd.append("--repoid=tendrl-core")
    # running repoclosure
    LOGGER.info(" ".join(cmd))
    with tempfile.TemporaryDirectory() as tmpdirname:
        cp = subprocess.run(
            cmd,
            cwd=tmpdirname,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
    LOGGER.debug("STDOUT: %s", cp.stdout)
    LOGGER.debug("STDERR: %s", cp.stderr)
    check_msg = "repoclosure return code should be 0 indicating no errors"
    pytest.check(cp.returncode == 0, msg=check_msg)
    # when the check fails, report the error in readable way
    if cp.returncode != 0:
        for line in cp.stdout.splitlines():
            LOGGER.failed(line.decode())
        for line in cp.stderr.splitlines():
            LOGGER.failed(line.decode())


def test_repo_packagelist(tendrl_repos):
    """
    Check that tendrl core repository contains all expected tendrl packages and
    doesn't contain anything else.
    """
    LOGGER.info(
        "expected tendrl-core packages are: " + ",".join(tendrl_packages))
    # get actual list of packages from tendrl-core repository (via repoquery)
    packages = list_packages('tendrl-core')
    for rpm_name in tendrl_packages:
        msg = "package {} should be present in tendrl-core repo"
        package_present = rpm_name in packages
        pytest.check(package_present, msg.format(rpm_name))
        if package_present:
            packages.remove(rpm_name)
    pytest.check(packages == [], msg="there should be no extra packages")
    for rpm_name in packages:
        LOGGER.failed("unexpected package in tendrl-core: {}".format(rpm_name))


def test_rpmlint(rpm_package):
    rpm_name, rpm_path = rpm_package
    cmd = ["rpmlint", rpm_path]
    # running rpmlint
    LOGGER.info(" ".join(cmd))
    cp = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    LOGGER.debug("STDOUT: %s", cp.stdout)
    LOGGER.debug("STDERR: %s", cp.stderr)
    LOGGER.debug("RCODE: %s", cp.returncode)
    # when the check fails, report the error in readable way
    for line in cp.stdout.splitlines():
        line_str = line.decode()
        if "E: unknown-key" in line_str or line_str.startswith("1 packages"):
            continue
        LOGGER.failed(line_str)


@pytest.mark.parametrize("check_command", [
    "check-sat",
    "check-conflicts",
    "check-upgrade",
    ])
def test_rpmdeplint(rpm_package, check_command, tendrl_repos, centos_repos):
    rpm_name, rpm_path = rpm_package
    cmd = ["rpmdeplint", check_command, "--arch", "x86_64"]
    # configure systemd default repositories
    for name, url in centos_repos.items():
        cmd.append("--repo")
        cmd.append("{},{}".format(name, url))
    # configure tendrl repository (passed via tendrl_repos fixture)
    for name, baseurl in tendrl_repos.items():
        cmd.append("--repo")
        cmd.append("{},{}".format(name, baseurl))
    # and last but not least: specify the package
    cmd.append(rpm_path)
    # running rpmdeplint
    LOGGER.info(" ".join(cmd))
    cp = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    LOGGER.debug("STDOUT: %s", cp.stdout)
    LOGGER.debug("STDERR: %s", cp.stderr)
    LOGGER.debug("RCODE: %s", cp.returncode)
    # when the check fails, report the error in readable way
    if cp.returncode != 0:
        for line in cp.stderr.splitlines():
            line_str = line.decode()
            if "Undeclared file conflicts:" == line_str:
                LOGGER.debug(line_str)
                continue
            if "provides /etc/grafana/grafana.ini which is also provided by " \
                    "grafana-4.1.2-1486989747.x86_64" in line_str:
                LOGGER.debug("IGNORING (old grafana packages): %s", line_str)
                continue
            LOGGER.failed(line_str)
