import pytest
from usmqe.api.tendrlapi import tendrlapi
from usmqe.gluster import gluster
import usmqe.inventory as inventory


def generate_test_parameters(*args):
    """ From input consisting of single values, lists or tuples of test parameters
    in format:
    (positive1, negative1), (positive2, negative2) .. (positiveN, negativeN)
    is created created list of tuples with length of *args. These tuples are mixture
    of positive and negative parameters with at least one negative parameter.
    e.g.: [(positive1,negative2,positive3), (negative1,negative2,positive3), ...]

    Args:
        args: tuples of given format
    """
    return [tuple(fixture1[1] if index1 == index2 else tuple(fixture1)[0]
            if type(fixture1) is not tuple or type(fixture1) is not list
            else fixture1[0]
            for index2, fixture2 in enumerate(args))
            for index1, fixture1 in enumerate(args)]


@pytest.fixture
def valid_cluster_id():
    # TODO change
    api = tendrlapi.ApiGluster()
    return api.get_cluster_list()[0]["cluster_id"]


@pytest.fixture
def invalid_cluster_ids():
    return (None, "0000000000000000")


@pytest.fixture
def valid_volume_id():
    # TODO change
    test_gluster = gluster.GlusterCommon()
    xml = test_gluster.run_on_node(command="volume info")
    return xml.findtext("./volInfo/volumes/volume/id")


@pytest.fixture
def invalid_volume_ids():
    return (None, "0000000000000000")


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


@pytest.fixture
def invalid_volume_bricks():
    return (None, "0000000000000000")


@pytest.fixture
def valid_volume_name():
    return pytest.config.getini("usm_volume_name")


@pytest.fixture
def invalid_volume_names():
    return (None, "./,!@##$%^&*()__{}|:';/<*+>)(")
