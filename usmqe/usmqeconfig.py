# -*- coding: utf8 -*-
"""
Pytest plugin to handle usmqe ini config files.

.. moduleauthor:: Martin Kudlej <mkudlej@redhat.com>
.. moduleauthor:: Filip Balak <fbalak@redhat.com>
"""


from collections.abc import Iterable, Mapping
from copy import deepcopy
import os
import yaml

from py.path import local
from ansible.inventory.manager import InventoryManager
from ansible.parsing.dataloader import DataLoader


def update_config(original_config, new_config):
    """
    Merges two dictionaries that contain more dictionaries.
    """
    for k, v in new_config.items():
        dict_found = original_config.get(k)
        if isinstance(v, Mapping) and isinstance(dict_found, Mapping):
            update_config(dict_found, v)
        else:
            original_config[k] = deepcopy(v)


class UsmConfig(object):
    """
    Configuration object containing inventory hosts file and configuration
    specified in usm yaml configuration files. Main configuration is defined
    in conf/main.yaml.
    """

    def __init__(self):
        self.inventory = {}
        self.config = {}

        base_path = local(os.path.abspath(__file__)).new(basename='..')
        # get default configuration from conf/main.yaml
        try:
            config_file = os.path.join(str(base_path), "conf", "main.yaml")
        except FileNotFoundError() as err:
            print("conf/main.yaml configuration file does not exist.")
        self.config = self.load_config(config_file)

        if self.config["configuration_files"]:
            for new_config in self.config["configuration_files"]:
                if not os.path.isabs(new_config):
                    new_config = os.path.join(str(base_path), new_config)
                update_config(self.config, self.load_config(new_config))

        # load inventory file to ansible interface
        # referenced in this class instance
        if self.config['inventory_file']:
            if isinstance(self.config['inventory_file'], Iterable):
                inventory_file = self.config['inventory_file'][0]
            else:
                inventory_file = self.config['inventory_file']
            if not os.path.isabs(inventory_file):
                inventory_file = os.path.join(str(base_path), inventory_file)
        else:
            raise FileNotFoundError(
                "No inventory file was provided in configuration "
                "(inventory_file in configuration file).")
        if not os.path.isfile(inventory_file):
            raise IOError("Could not find provided inventory file {}".format(
                inventory_file))
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
