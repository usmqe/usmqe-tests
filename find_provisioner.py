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
pytest.check = _check

from usmqe.api.etcdapi.etcdapi import EtcdApi


def get_nodes_by_tag(tag):
    """
    Query Tendrl etcd instance for nodes with given tag.
    """
    etcd = EtcdApi()
    resp = etcd.get_key_value('/indexes/tags/{}/'.format(tag))
    # TODO: WTF? Why?
    nodes_str_val = resp['node']['nodes'][0]['value']
    nodes = json.loads(nodes_str_val)
    node_names = []
    for node_id in nodes:
        resp = etcd.get_key_value('/nodes/{}/NodeContext/fqdn'.format(node_id))
        node_names.append(resp['node']['value'])
    return node_names


def main():
    ap = argparse.ArgumentParser(description="Find Tendrl provisioner node(s).")
    ap.add_argument("-v", dest="verbose", action="store_true", help="verbose")
    args = ap.parse_args()

    for node_name in get_nodes_by_tag("provisioner"):
        print(node_name)


if __name__ == '__main__':
    sys.exit(main())
