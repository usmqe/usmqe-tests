import pytest
import os.path
from usmqe.api.tendrlapi import glusterapi
from usmqe.gluster import gluster
import usmqe.inventory as inventory


@pytest.fixture
def valid_cluster_id(valid_session_credentials):
    """
    Generate valid id of imported cluster.
    """
    # TODO change
    api = glusterapi.TendrlApiGluster(auth=valid_session_credentials)
    cluster_list = api.get_cluster_list()
    return cluster_list[0]["cluster_id"]


@pytest.fixture
def valid_nodes(valid_session_credentials):
    """
    Generate valid host info from GetNodeList api call related to tendrl/nodes
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


@pytest.fixture
def valid_volume_id():
    """
    Generate valid id of a created volume.
    """
    volume = gluster.GlusterVolume(pytest.config.getini("usm_volume_name"))
    return volume.get_volume_id()


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
    device_info = [list(x["localstorage"]["blockdevices"]["all"].values())[0]
                   if x["localstorage"]["blockdevices"]["all"] is not None
                   else None for x in api.get_nodes()["nodes"]]
    device_info = [x for x in device_info if x is not None]
    print(device_info)
    devices = [x["device_kernel_name"] for x in device_info]

    try:
        return devices[0:count]
    except IndexError as e:
        raise Exception(
                "TypeError({0}): There are not enough devices. There are: {1}. {2}"
                .format(
                    e.errno,
                    devices,
                    e.strerror))


@pytest.fixture
def valid_volume_configuration(valid_volume_name, valid_brick_path):
    """
    Generate valid configuration for volume creation with set:
        "Volume.volname", "Volume.bricks", "Volume.replica_count", "Volume.force"
    """
    role = pytest.config.getini("usm_gluster_role")
    try:
        bricks = [[{"{}".format(inventory.role2hosts(role)[i]):
                    "{}".format(valid_brick_path)},
                   {"{}".format(inventory.role2hosts(role)[i+1]):
                    "{}".format(valid_brick_path)}]
                  for i in range(0, len(inventory.role2hosts(role)), 2)]
    except TypeError as e:
        raise Exception(
            "TypeError({0}): You should probably define usm_brick_path and \
                    usm_gluster_role in usm.ini. {1}".format(
                e.errno,
                e.strerror))
    return {
        "Volume.volname": valid_volume_name,
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


@pytest.fixture
def valid_volume_name():
    """
    Generate valid volume name defined in usm.ini.
    """
    return pytest.config.getini("usm_volume_name")


# TODO(fbalak) as `./,!@##$%^&*()__{}|:';/<*+>)(` as parameter
@pytest.fixture(params=[None])
def invalid_volume_name(request):
    """
    Generate invalid volume name.
    """
    return request.param
