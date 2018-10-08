# -*- coding: utf8 -*-
"""
Pytest plugin to handle usmqe ini config files.

.. moduleauthor:: Martin Kudlej <mkudlej@redhat.com>
.. moduleauthor:: Filip Balak <fbalak@redhat.com>
"""


from configparser import ConfigParser

import pytest
import os
import argparse
import yaml
from ansible.inventory.manager import InventoryManager
from ansible.parsing.dataloader import DataLoader



class UsmConfig(object):
    """
    Configuration object containing inventory hosts file and configuration
    specified in usm yaml configuration file.
    """

    def __init__(self):
        self.inventory = {}
        self.usm = {}
        self.pytest = {}

        parser = argparse.ArgumentParser()
        parser.add_argument(
            "--config-file",
            nargs='?',
            help="path to file where is usm yaml configuration")
        parser.add_argument(
            "--inventory-file",
            nargs='?',
            help="path to usm inventory file")
        args = parser.parse_args()

        # get default usm.yaml from conf/usm.yaml
        if not args.config_file:
            config_file = os.path.join(os.getcwd(), "conf", "usm.yaml")
        else:
            try:
                config_file = args.config_file
            except FileNotFoundError() as err:
                print("Configuration file {} does not exist.".format(
                    args.config_file))
        self.usm = self.load_config(config_file)

        # get default inventory file from conf/usm.hosts
        if not args.inventory_file:
            inventory_file = os.path.join(os.getcwd(), "conf", "usm.hosts")
        else:
            try:
                inventory_file = args.inventory_file
            except FileNotFoundError() as err:
                print("Inventory file {} does not exist.".format(
                    args.inventory_file))
        loader = DataLoader()
        self.inventory = InventoryManager(
            loader=loader,
            sources=inventory_file)


    def load_inventory(self, inventory_file):
        """
        Load inventory file to module inventory.py.

        To use content from inventory file just *import inventory* and then use
        proper function from ``usmqe.inventory``.
        Name of inventory file is stored in ``usm_inventory`` option in
        ``pytest.ini``.  Its value can be overriden by ``pytest -o
        usm_inventory=path``.
        """
        inventory = InventoryManager(loader=loader, sources="/home/usmqe/usmqe-tests/conf/usm.hosts")
        # update machine config (reading ansible inventory)
        hosts = ConfigParser(allow_no_value=True)
        hosts.read(inventory_file)
        for rolename in hosts.sections():
            for hostname, _ in hosts.items(rolename):
                usmqe.inventory.add_host_entry(rolename, hostname)


    def load_config(self, config_file):
        """
        Loads configuration from pytest.yaml file.
        """
        with open(config_file) as config_open:
            conf = yaml.load(config_open)
        return conf
