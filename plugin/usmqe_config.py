# -*- coding: utf8 -*-
"""
Pytest plugin to handle usmqe ini config files.

.. moduleauthor:: Martin Kudlej <mkudlej@redhat.com>
.. moduleauthor:: Filip Balak <fbalak@redhat.com>
"""


import pytest
import os
import yaml
from py.path import local
from ansible.inventory.manager import InventoryManager
from ansible.parsing.dataloader import DataLoader


class UsmConfig(object):
    """
    Configuration object containing inventory hosts file and configuration
    specified in usm yaml configuration files. Main configuration is defined
    in conf/MAIN.yaml.
    """

    def __init__(self):
        self.inventory = {}
        self.config = {}

        base_path = local(os.path.abspath(__file__)).new(basename='..')
        # get default configuration from conf/MAIN.yaml
        config_file =             try:
            config_file = os.path.join(str(base_path), "conf", "MAIN.yaml")
        except FileNotFoundError() as err:
            print("conf/MAIN.yaml configuration file does not exist."
        self.config = self.load_config(config_file)


        if self.config.configuration_files:
            for new_config in self.config.configuration_files:
                self.config = {**self.config, **new_config}
        # get default inventory file from conf/usm.hosts
        if self.config.inventory_file:
            try:
                inventory_file = self.config.inventory_file
            except FileNotFoundError() as err:
                print("Inventory file {} does not exist.".format(
                    args.inventory_file))
        else:
            except FileNotFoundError() as err:
                print("No inventory file was provided in configuration "
                      "(inventory_file in configuration file).")
        loader = DataLoader()
        self.inventory = InventoryManager(
            loader=loader,
            sources=inventory_file)

    def load_config(self, config_file):
        """
        Loads configuration from pytest.yaml file.
        """
        with open(config_file, "r") as stream:
            try:
                conf = yaml.load(stream)
            except yaml.YAMLError as exc:
                print(exc)
        return conf
