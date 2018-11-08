from collections.abc import Iterable
from os import pardir, path
import subprocess
import sys

from usmqe.usmqeconfig import UsmConfig

conf = UsmConfig()

# This serves as predefined pytest plugin configuration.
# There can be added new options required by pytest plugins.
params = {
    "ansible_playbook_directory": path.abspath(
        path.join(path.dirname(__file__), pardir, "usmqe-setup")),
    "ansible_playbook_inventory": conf.config["inventory_file"]
    }


# `ansible_playbook_inventory` option is preprocessed
if params['ansible_playbook_inventory']:
    if isinstance(params['ansible_playbook_inventory'], Iterable):
        params['ansible_playbook_inventory'] = params[
            'ansible_playbook_inventory'][0]
    else:
        params['ansible_playbook_inventory'] = params[
            'ansible_playbook_inventory']
if not path.isabs(params['ansible_playbook_inventory']):
    base_path = path.abspath(path.dirname(__file__))
    params['ansible_playbook_inventory'] = path.join(
        str(base_path), params['ansible_playbook_inventory'])


predefined_params = " ".join(
    ["--{}={}".format(key.replace("_", "-"), params[key])
        for key in params.keys()])

command = "python3 -m pytest {} {}".format(
    predefined_params,
    " ".join(
        sys.argv[1:] if sys.argv[0].startswith("python") else sys.argv[2:]))
subprocess.call(command, shell=True)
