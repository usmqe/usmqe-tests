# -*- coding: utf8 -*-

import pytest
import subprocess

from packagelist import tendrl_packages


LOGGER = pytest.get_logger(__name__, module=True)


@pytest.mark.parametrize("rpm_name", tendrl_packages)
def test_yum_install(chroot_dir, rpm_name):
    """
    Try to install and uninstall rpm package via yum in CentOS 7 chroot.
    """
    cmd = [
        "sudo",
        "yum", "--installroot=%s" % chroot_dir, "-y", "install", rpm_name]
    # running yum install
    LOGGER.info(" ".join(cmd))
    cp = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    LOGGER.debug("STDOUT: %s", cp.stdout)
    if len(cp.stderr) > 0:
        LOGGER.error("STDERR: %s", cp.stderr)
    else:
        LOGGER.debug("STDERR: %s", cp.stderr)
    check_msg = "return code of 'yum install {}' should be 0 indicating no errors"
    pytest.check(cp.returncode == 0, msg=check_msg.format(rpm_name))
    # check after installation
    cmd = ["rpm", "-q", rpm_name, "--root", chroot_dir]
    LOGGER.info(" ".join(cmd))
    cp = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    LOGGER.debug("STDOUT: %s", cp.stdout)
    LOGGER.debug("STDERR: %s", cp.stderr)
    check_msg = "return code of 'rpm -q {}' should be 0 indicating no errors"
    pytest.check(cp.returncode == 0, msg=check_msg.format(rpm_name))
    # running yum remove
    cmd = [
        "sudo",
        "yum", "--installroot=%s" % chroot_dir, "-y", "remove", rpm_name]
    LOGGER.info(" ".join(cmd))
    cp = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    LOGGER.debug("STDOUT: %s", cp.stdout)
    LOGGER.debug("STDERR: %s", cp.stderr)
    check_msg = "return code of 'yum remove {}' should be 0 indicating no errors"
    pytest.check(cp.returncode == 0, msg=check_msg.format(rpm_name))
