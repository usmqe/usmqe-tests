import pytest
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
def valid_gluster_nodes(valid_session_credentials):
    """
    Generate valid host info from GetNodeList api call related to gluster
    """
    api = glusterapi.TendrlApiGluster(auth=valid_session_credentials)
    cluster_list = api.get_nodes()
    return [x if "gluster/server" in x["tags"] for x in cluster_list["nodes"]]


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
def valid_volume_configuration(valid_volume_name):
    """
    Generate valid configuration for volume creation with set:
        "Volume.volname", "Volume.bricks", "Volume.replica_count", "Volume.force"
    """
    role = pytest.config.getini("usm_gluster_role")
    try:
        bricks = [[{"{}".format(inventory.role2hosts(role)[i]):
                    "{}".format(pytest.config.getini("usm_brick_path"))},
                   {"{}".format(inventory.role2hosts(role)[i+1]):
                    "{}".format(pytest.config.getini("usm_brick_path"))}]
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
