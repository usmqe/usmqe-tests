# -*- coding: utf-8 -*-
# This is rather just an example than a serious unit test.


import pytest


@pytest.fixture
def inventory_data():
    data = []
    data.append(("usm_server", "example-usm3-server.usmqe.tendrl.org"))
    for i in range(1, 4):
        node = "example-usm3-mon{0}.usmqe.tendrl.org".format(i)
        data.append(("ceph_mon", node))
        data.append(("usm_nodes", node))
    for i in range(1, 9):
        node = "example-usm3-node{0}.usmqe.tendrl.org".format(i)
        data.append(("ceph_osd", node))
        data.append(("usm_nodes", node))
    return data


def test_host2roles_null(inventory_data):
    import usmqe.inventory
    for _, host in inventory_data:
        assert usmqe.inventory.host2roles(host) is None


def test_role2hosts_null(inventory_data):
    import usmqe.inventory
    for role, _ in inventory_data:
        assert usmqe.inventory.role2hosts(role) is None


def test_get_all_hosts_null():
    import usmqe.inventory
    assert len(usmqe.inventory.get_all_hosts()) == 0


def test_get_all_hosts(inventory_data):
    import usmqe.inventory
    assert len(usmqe.inventory.get_all_hosts()) == 0
    for role, host in inventory_data:
        usmqe.inventory.add_host_entry(role, host)
    expected = sorted(list(set([host for _, host in inventory_data])))
    assert sorted(list(usmqe.inventory.get_all_hosts())) == expected
