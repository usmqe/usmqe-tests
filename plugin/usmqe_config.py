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
    parser.addini('usm_config', 'USM configuration')
    parser.addini('usm_inventory', 'USM host configuration')


@pytest.fixture(autouse=True, scope="session")
def load_inventory():
    """
    Load inventory file to module inventory.py.

    To use content from inventory file just *import inventory* and then use
    proper function from ``usmqe.inventory``.
    Name of inventory file is stored in ``usm_inventory`` option in
    ``pytest.ini``.  Its value can be overriden by ``pytest -o
    usm_inventory=path``.
    """
    # update machine config (reading ansible inventory)
    hosts = ConfigParser(allow_no_value=True)
    hosts.read(pytest.config.getini("usm_inventory"))
    for rolename in hosts.sections():
        for hostname, _ in hosts.items(rolename):
            usmqe.inventory.add_host_entry(rolename, hostname)


@pytest.fixture(autouse=True, scope="session")
def load_config():
    """
    Loads configuration from pytest.ini file.

    If there is configured external configuration file(usm_config)
    then ini values are updated by values from configuration file.

    All configuration entries can be overriden by::

        $ py.test -o=usm_username=admin2
    """
    if pytest.config.getini("usm_config"):
        conf = ConfigParser()
        conf.read(pytest.config.getini("usm_config"))
        if "usmqepytest" not in conf.sections():
            # TODO: report a problem
            return
        for key, value in conf.items("usmqepytest"):
            override_value = pytest.config._get_override_ini_value(key)
            if override_value is None:
                pytest.config._inicache[key] = value
            else:
                pytest.config._inicache[key] = override_value
