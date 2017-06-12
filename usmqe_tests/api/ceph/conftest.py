import pytest
from usmqe.api.tendrlapi import cephapi


@pytest.fixture
def valid_cluster_id(valid_session_credentials):
    """
    Generate valid id of imported cluster.
    """
    # TODO change
    api = cephapi.TendrlApiCeph(auth=valid_session_credentials)
    cluster_list = [cl for cl in api.get_cluster_list()
                    if cl["sds_name"] == "ceph" and
                    cl["cluster_name"] == pytest.config.getini("usm_ceph_cl_name")
                    ]
    return cluster_list[0]["cluster_id"]


@pytest.fixture(params=[None, "0000000000000000"])
def invalid_cluster_id(request):
    """
    Generate invalid cluster id.
    """
    return request.param


@pytest.fixture
def valid_pool_id(valid_session_credentials):
    """
    Generate valid id of a created volume.
    """
# TODO change
    api = cephapi.TendrlApiCeph(auth=valid_session_credentials)
    cluster_list = [cl for cl in api.get_cluster_list()
                    if cl["sds_name"] == "ceph" and
                    cl["cluster_name"] == pytest.config.getini("usm_ceph_cl_name")
                    ]
    pools = cluster_list[0]["pools"]
    return [pool["pool_id"] for pool in pools.values()
            if pool["pool_name"] == pytest.config.getini("usm_pool_name")
            ][0]


@pytest.fixture(params=[None, "0000000000000000"])
def invalid_pool_id(request):
    """
    Generate invalid volume id.
    """
    return request.param


@pytest.fixture(params=[0])
def invalid_minsize(request):
    """
    Generate invalid min pool size(replicas).
    """
    return request.param


@pytest.fixture(params=[0])
def invalid_pg_num(request):
    """
    Generate invalid pool pg number.
    """
    return request.param


@pytest.fixture(params=[" ", "*", "!", "_", "--"])
def invalid_pool_name(request):
    """
    Generate invalid pool name.
    """
    return request.param


@pytest.fixture(params=[0])
def invalid_size(request):
    """
    Generate invalid pool size(replicas).
    """
    return request.param


@pytest.fixture(params=[2])
def valid_minsize(request):
    """
    Generate valid min pool size(replicas).
    """
    return request.param


@pytest.fixture(params=[128])
def valid_pg_num(request):
    """
    Generate invalid pool pg number.
    """
    return request.param


@pytest.fixture
def valid_pool_name():
    """
    Generate valid pool name.
    """
    return pytest.config.getini("usm_pool_name")


@pytest.fixture(params=[3])
def valid_size(request):
    """
    Generate valid pool size(replicas).
    """
    return request.param
