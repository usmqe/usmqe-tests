import pytest
import os.path
from usmqe.api.tendrlapi import glusterapi
from usmqe.gluster import gluster
import usmqe.inventory as inventory


@pytest.fixture
def valid_nodes(valid_session_credentials):
    """
    Generate valid host info from GetClusterList api call related to tendrl/nodes
    """
    api = glusterapi.TendrlApiGluster(auth=valid_session_credentials)
    cluster_list = api.get_nodes()
    return [x for x in cluster_list["nodes"]
            if "tendrl/node" in x["tags"]
            and x["status"] == "UP"]


@pytest.fixture(params=[None, "0000000000000000"])
def invalid_cluster_id(request):
    """
    Generate invalid cluster id.
    """
    return request.param


@pytest.fixture
def valid_trusted_pool():
    """
    Return list of node hostname from created trusted pool.
    """
    storage = gluster.GlusterCommon()
    host = inventory.role2hosts(pytest.config.getini("usm_gluster_role"))[0]
    return storage.get_hosts_from_trusted_pool(host)


@pytest.fixture(params=[None, "0000000000000000"])
def invalid_volume_id(request):
    """
    Generate invalid volume id.
    """
    return request.param


@pytest.fixture
def valid_brick_name():
    """
    Generate valid brick name.
    """
    return pytest.config.getini("usm_brick_name")


@pytest.fixture
def valid_brick_path(valid_brick_name):
    """
    Generate valid brick path. Bricks are generated in directory:
    ``/tendrl_gluster_bricks/<brick_name>_mount``

    as described in https://github.com/Tendrl/gluster-integration/issues/320
    and in https://github.com/nnDarshan/documentation/blob/415c3e9fd50d1a6e38ce6cc84abbde8db31475c4/
                   gluster_brick_provisioning.adoc
    """
    return os.path.join(os.path.sep, "tendrl_gluster_bricks", "{}_mount".format(
        valid_brick_name))


@pytest.fixture
def valid_devices(valid_session_credentials, count=1):
    """
    Generate device paths.

    Args:
        count (int): How many device paths should be generated.
                     There have to be enough devices.
    """

    api = glusterapi.TendrlApiGluster(auth=valid_session_credentials)
    nodes_free_devs = {x["node_id"]: list(x["localstorage"]["blockdevices"]["free"].values())
                       for x in api.get_nodes()["nodes"]
                       if len(x["localstorage"]["blockdevices"]["free"]) > 0}
    nodes_free_kern_name = {}
    for node_id in nodes_free_devs:
        for device in nodes_free_devs[node_id]:
            if node_id not in nodes_free_kern_name:
                nodes_free_kern_name[node_id] = []
            nodes_free_kern_name[node_id].append(device["device_kernel_name"])

    try:
        return {node_id: sorted(nodes_free_kern_name[node_id])[0:count]
                for node_id in nodes_free_kern_name}
    except IndexError as err:
        raise Exception(
                "TypeError({0}): There are not enough devices. There are: {1}. {2}"
                .format(
                    err.errno,
                    nodes_free_kern_name,
                    err.strerror))

# TODO change to use bricks mapping
@pytest.fixture
def volume_conf_2rep(cluster_reuse):
    """
    Generate valid configuration for volume creation with set:
        "Volume.volname", "Volume.bricks", "Volume.replica_count", "Volume.force"
    Node list for brick list is created from list of nodes in cluster.
    Always is used first(alphabetic order) free brick on node.
    Cluster is identified by one node from cluster.
    *Volume name should be defined for each test!*
    *Configuration is made for replica count == 2.*
    """
    hosts = cluster_reuse["nodes"]
    bricks = [[{"{}".format(hosts[i]["fqdn"]):
                "{}".format(sorted(hosts[i]["bricks"]["free"])[0])},
               {"{}".format(hosts[i+1]["fqdn"]):
                "{}".format(sorted(hosts[i+1]["bricks"]["free"])[0])}]
              for i in range(0, len(hosts), 2)]

    return {
        "Volume.volname": "{}",
        "Volume.bricks": bricks,
        "Volume.replica_count": "2",
        "Volume.force": True}


@pytest.fixture(params=[{
    "Volume.volname": "Volume_invalid",
    "Volume.bricks": None,
    "Volume.replica_count": "2",
    "Volume.force": True}])
def invalid_volume_configuration(request):
    """
    Generate invalid bricks.
    """
    return request.param


# TODO(fbalak) as `./,!@##$%^&*()__{}|:';/<*+>)(` as parameter
@pytest.fixture(params=[None])
def invalid_volume_name(request):
    """
    Generate invalid volume name.
    """
    return request.param

@pytest.fixture
def valid_bricks_for_crud_volume(
    valid_session_credentials,
    cluster_reuse,
    valid_brick_name):
    api = glusterapi.TendrlApiGluster(auth=valid_session_credentials)

    nodes = cluster_reuse["nodes"]

    job_id = api.create_bricks(
        cluster_reuse["cluster_id"],
        cluster_reuse["nodes"],
        valid_devices,
        valid_brick_name)["job_id"]
    api.wait_for_job_status(job_id)
    import time
    time.sleep(400)
