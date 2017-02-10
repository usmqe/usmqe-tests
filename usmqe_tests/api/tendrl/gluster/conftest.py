import pytest
from usmqe.api.tendrlapi import glusterapi
from usmqe.gluster import gluster
import usmqe.inventory as inventory


@pytest.fixture
def valid_cluster_id():
    # TODO change
    api = glusterapi.ApiGluster()
    return api.get_cluster_list()[0]["cluster_id"]


@pytest.fixture(params=[None, "0000000000000000"])
def invalid_cluster_id(request):
    return request.param


@pytest.fixture
def valid_volume_id():
    volume = gluster.GlusterVolume(pytest.config.getini("usm_volume_name"))
    return volume.get_volume_id()


@pytest.fixture(params=[None, "0000000000000000"])
def invalid_volume_id(request):
    return request.param


@pytest.fixture
def valid_volume_bricks():
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
    return request.param


@pytest.fixture
def valid_volume_name():
    return pytest.config.getini("usm_volume_name")


@pytest.fixture(params=[None, "./,!@##$%^&*()__{}|:';/<*+>)("])
def invalid_volume_name(request):
    return request.param
