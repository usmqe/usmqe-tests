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
from py.path import local
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

        base_path = local(os.path.abspath(__file__)).new(basename='..')
        # get default usm.yaml from conf/usm.yaml
        if not args.config_file:
            config_file = os.path.join(str(base_path), "conf", "usm.yaml")
        else:
            try:
                config_file = args.config_file
            except FileNotFoundError() as err:
                print("Configuration file {} does not exist.".format(
                    args.config_file))
        self.usm = self.load_config(config_file)

        # get default inventory file from conf/usm.hosts
        if not args.inventory_file:
            inventory_file = os.path.join(str(base_path), "conf", "usm.hosts")
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
