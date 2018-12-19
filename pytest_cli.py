#!/usr/bin/env python3

from collections.abc import Iterable
from os import pardir, path
import subprocess
import sys

from usmqe.usmqeconfig import UsmConfig

conf = UsmConfig()

# This serves as predefined pytest plugin configuration.
# There can be added new options required by pytest plugins.
# Prefered way to execute this script is to call pytest_cli.py from terminal
# instead of pytest command.
params = {
    "ansible_playbook_directory": path.abspath(
        path.join(path.dirname(__file__), pardir, "usmqe-setup")),
    "ansible_playbook_inventory": conf.config["inventory_file"]
    }


# `ansible_playbook_inventory` option is preprocessed
# todo(fbalak): add inventory file concatenation or something
# now is used first inventory file in UsmConfig
if params['ansible_playbook_inventory'] is not None:
    if (not isinstance(params['ansible_playbook_inventory'], str)
        and isinstance(params['ansible_playbook_inventory'], Iterable)):
            params['ansible_playbook_inventory'] = params[
                'ansible_playbook_inventory'][0]

if not path.isabs(params['ansible_playbook_inventory']):
    base_path = path.abspath(path.dirname(__file__))
    params['ansible_playbook_inventory'] = path.join(
        str(base_path), params['ansible_playbook_inventory'])


predefined_params = ["--{}={}".format(key.replace("_", "-"), val)
        for key, val in params.items()]

command = ["python3", "-m", "pytest"] + predefined_params + sys.argv[1:]
print("COMMAND: {}".format(command))
result = subprocess.run(command)
sys.exit(result.returncode)
