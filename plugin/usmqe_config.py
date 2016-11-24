# -*- coding: utf8 -*-
"""
Pytest plugin to handle usmqe ini config files.

.. moduleauthor:: Martin Kudlej <mkudlej@redhat.com>
"""


from configparser import ConfigParser

import pytest

import usmqe.inventory


def pytest_addoption(parser):
    """
    Add ini options to be accepted by pytest.
    """
    # defaults are specified in root pytest.ini file
    parser.addini('USM_CONFIG', 'USM configuration')
    parser.addini('USM_HOST_CONFIG', 'USM host configuration')
    parser.addini('USM_USERNAME', 'USM username for login')
    parser.addini('USM_PASSWORD', 'USM password for login')
    parser.addini('USM_WEB_URL', 'USM url for web')
    parser.addini('USM_API_URL', 'USM url for api')
    parser.addini('USM_LOG_LEVEL', 'USM log test level')
    parser.addini('USM_KEYFILE', 'USM key file for passwordless ssh')
    parser.addini('USM_CA_CERT', 'USM use CA certificate', type='bool')


@pytest.fixture(autouse=True, scope="session")
def load_inventory():
    """
    Load inventory file to module inventory.py.

    To use content from inventory file just *import inventory* and then use
    proper function from ``usmqe.inventory``.
    Name of inventory file is stored in ``USM_HOST_CONFIG`` option in
    ``pytest.ini``.  Its value can be overriden by ``pytest -o
    USM_HOST_CONFIG=path``.
    """
    # update machine config (reading ansible inventory)
    hosts = ConfigParser(allow_no_value=True)
    hosts.read(pytest.config.getini("USM_HOST_CONFIG"))
    for rolename in hosts.sections():
        for hostname, _ in hosts.items(rolename):
            usmqe.inventory.add_host_entry(rolename, hostname)


@pytest.fixture(autouse=True, scope="session")
def load_config():
    """
    Loads configuration from pytest.ini file.

    If there is configured external configuration file(USM_CONFIG)
    then ini values are updated by values from configuration file.

    All configuration entries can be overriden by::

        $ py.test -o USM_USERNAME=admin2
    """
    if pytest.config.getini("USM_CONFIG"):
        conf = ConfigParser()
        conf.read(pytest.config.getini("USM_CONFIG"))

        for section in ('webstr', 'usm', 'ldap'):
            if section in conf.sections():
                for key, value in conf.items(section):
                    if section == 'usm':
                        name = "USM_{0}".format(key.upper())
                    else:
                        name = "USM_{0}_{1}".format(
                            section.upper(), key.upper())

                    override_value = pytest.config._get_override_ini_value(
                        name)
                    if override_value is None:
                        pytest.config._inicache[name] = value
                    else:
                        pytest.config._inicache[name] = override_value
