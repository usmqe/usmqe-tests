# -*- coding: utf8 -*-

import pytest

from usmqe.api.tendrlapi.common import TendrlAuth, login, logout, TendrlApi


@pytest.fixture(scope="session")
def valid_session_credentials(request):
    """
    During setup phase, login default usmqe user account (username and password
    comes from usm.ini config file) and return requests auth object.
    Then during teardown logout the user to close the session.
    """
    auth = login(
        pytest.config.getini("usm_username"),
        pytest.config.getini("usm_password"))
    yield auth
    logout(auth=auth)


@pytest.fixture(
    scope="session",
    params=[
        "",
        None,
        "this_is_invalid_access_token_00000",
        "4e3459381b5b94fcd642fb0ca30eba062fbcc126a47c6280945a3405e018e824",
        ])
def invalid_session_credentials(request):
    """
    Return invalid access (for testing negative use cases), no login or logout
    is performed during setup or teardown.
    """
    username = pytest.config.getini("usm_username")
    invalid_token = request.param
    auth = TendrlAuth(token=invalid_token, username=username)
    return auth


@pytest.fixture
def cluster_reuse(valid_session_credentials):
    """
    Returns imported or created cluster identified
    by one of machine from cluster.
    Returned cluster can be used for further testing.
    Function uses Tendrl API(GetNodeList and GetClusterList).
    In case there is need to identify cluster directly
    by storage tools this function should be split.
    """
    id_hostname = pytest.config.getini("usm_id_fqdn")
    api = TendrlApi(auth=valid_session_credentials)
    node_list = api.get_nodes()
    hash_hostname = [node for node in node_list["nodes"]
                     if node["fqdn"] == id_hostname
                     ]
    if len(hash_hostname) != 1:
        raise Exception("There is not one node with FQDN = {}.".format(id_hostname))
    hash_hostname = hash_hostname[0]["node_id"]
    clusters = api.get_cluster_list()
    clusters = [cluster for cluster in clusters
                if hash_hostname in cluster["nodes"].keys()
                ]
    if len(clusters) != 1:
        raise Exception("There is not one cluster which includes node"
                        " with FQDN == {}.".format(id_hostname))
    return clusters[0]
