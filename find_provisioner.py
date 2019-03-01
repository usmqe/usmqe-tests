#!/usr/bin/env python3
# -*- coding: utf8 -*-


"""
Script to find Tendrl *provisioner* node. It requires the same setup and
configuration as our tests executed via ``pytest_cli.py`` wrapper (eg. to
locate, authenticate and access etcd instance).

TODO: move get_nodes_by_tag() into usmqe module
"""


import argparse
import json
import sys

# This is a terrible HACK, overcomming lack of code reusability and
# entanglement of code in usmqe module :/
import pytest
import plugin.log_assert
def _check(*args, **kwargs):
    pass
pytest.get_logger = plugin.log_assert.get_logger
pytest.set_logger = plugin.log_assert.set_logger
pytest.check = _check

# Another HACK: initialize mrglog module
LOGGER = pytest.get_logger("find_provisioner")
pytest.set_logger(LOGGER)

from usmqe.api.etcdapi.etcdapi import EtcdApi
from usmqe.usmqeconfig import UsmConfig


def get_nodes_by_tag(tag):
    """
    Query Tendrl etcd instance for nodes with given tag.
    """
    etcd = EtcdApi()
    resp = etcd.get_key_value('/indexes/tags/{}/'.format(tag))
    # note: we expect that given inner node (directory) in etcd contains one
    # leaf node (file), with value (content) we are actually interested in ...
    # see: https://coreos.com/etcd/docs/latest/v2/api.html
    try:
        nodes_str_val = resp['node']['nodes'][0]['value']
        nodes = json.loads(nodes_str_val)
    except Exception:
        LOGGER.error("etcd data doesn't follow expected structure: can't get list of nodes for given tag")
        nodes = []
    node_names = []
    for node_id in nodes:
        resp = etcd.get_key_value('/nodes/{}/NodeContext/fqdn'.format(node_id))
        node_names.append(resp['node']['value'])
    return node_names


def main():
    ap = argparse.ArgumentParser(description="Find Tendrl provisioner node(s).")
    ap.add_argument("-v", dest="verbose", action="store_true", help="set LOGGER to DEBUG level")
    args = ap.parse_args()

    if args.verbose:
        LOGGER.setLevel("DEBUG")
    else:
        LOGGER.setLevel("INFO")

    LOGGER.debug("loading UsmConfig")
    conf = UsmConfig()
    LOGGER.info("url of etcd: %s", conf.config["usmqe"]["etcd_api_url"])

    provisioner_nodes = get_nodes_by_tag("provisioner")
    LOGGER.info("found %d provisioner node(s)", len(provisioner_nodes))
    for node_name in provisioner_nodes:
        LOGGER.info(node_name)

if __name__ == '__main__':
    sys.exit(main())
