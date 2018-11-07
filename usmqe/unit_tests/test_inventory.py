# -*- coding: utf-8 -*-
# This test uses example inventory file conf/example-usm1.hosts, as defined in
# conf/main.yaml config.


from usmqe.usmqeconfig import UsmConfig


def test_inventory_groups_exists():
    CONF = UsmConfig()
    gd = CONF.inventory.get_groups_dict()
    assert "gluster_servers" in gd
    assert "usm_nodes" in gd
    assert "usm_server" in gd
    assert "usm_client" in gd


def test_inventory_get_hosts():
    CONF = UsmConfig()
    gd = CONF.inventory.get_groups_dict()
    example_server = "example-usm1-gl1.usmqe.tendrl.org"
    assert len(gd["usm_nodes"]) == 6
    assert len(gd["usm_server"]) == 1


def test_inventory_get_hosts_gluster_is_node():
    CONF = UsmConfig()
    gd = CONF.inventory.get_groups_dict()
    example_server = "example-usm1-gl1.usmqe.tendrl.org"
    assert example_server in gd["usm_nodes"]
    assert example_server in gd["gluster_servers"]
    assert gd["usm_nodes"] == gd["gluster_servers"]
