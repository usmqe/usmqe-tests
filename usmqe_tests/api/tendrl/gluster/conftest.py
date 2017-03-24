import pytest
from usmqe.api.tendrlapi import glusterapi
from usmqe.gluster import gluster
import usmqe.inventory as inventory


@pytest.fixture
def valid_cluster_id(valid_access_credentials):
    """
    Generate valid id of imported cluster.
    """
    # TODO change
    api = glusterapi.TendrlApiGluster()
    return api.get_cluster_list(valid_access_credentials)[0]["cluster_id"]


@pytest.fixture(params=[None, "0000000000000000"])
def invalid_cluster_id(request):
    """
    Generate invalid cluster id.
    """
    return request.param


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
def valid_volume_bricks():
    """
    Generate valid brick for api in format:
        hostname:brick_path
    """
    role = pytest.config.getini("usm_gluster_role")
    try:
        return ["{}:{}".format(x, pytest.config.getini(
            "usm_brick_path")) for x in inventory.role2hosts(role)]
    except TypeError as e:
        print(
            "TypeError({0}): You should probably define usm_brick_path and \
                    usm_gluster_role in usm.ini. {1}".format(
                e.errno,
                e.strerror))


@pytest.fixture(params=[None, "0000000000000000"])
def invalid_volume_bricks(request):
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


@pytest.fixture(params=[None, "./,!@##$%^&*()__{}|:';/<*+>)("])
def invalid_volume_name(request):
    """
    Generate invalid volume name.
    """
    return request.param
