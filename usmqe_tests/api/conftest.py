# -*- coding: utf8 -*-

import time

import pytest

from usmqe.api.tendrlapi.common import TendrlAuth, login, logout, TendrlApi
from plugin.usmqe_config import UsmConfig

config = UsmConfig()


@pytest.fixture(scope="session")
def valid_session_credentials(request):
    """
    During setup phase, login default usmqe user account (username and password
    comes from usm.ini config file) and return requests auth object.
    Then during teardown logout the user to close the session.
    """
    auth = login(
        config.config["tests"]["usm_username"],
        config.config["tests"]["usm_password"])
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
    username = config.config["tests"]["usm_username"]
    invalid_token = request.param
    auth = TendrlAuth(token=invalid_token, username=username)
    return auth


@pytest.fixture
def cluster_reuse(valid_session_credentials):
    """
    Returns cluster identified by one of machines
    from cluster.
    Returned cluster can be used for further testing.
    Function uses Tendrl API(clusters). In case there
    is need to identify cluster directly by storage
    tools this function should be split.
    """
    id_hostname = config.config["tests"]["usm_cluster_member"]
    api = TendrlApi(auth=valid_session_credentials)
    for _ in range(12):
        clusters = api.get_cluster_list()
        clusters = [cluster for cluster in clusters
                    if id_hostname in
                    [node["fqdn"] for node in cluster["nodes"]]
                    ]
        if len(clusters) == 1:
            return clusters[0]
        time.sleep(5)

    raise Exception("There is not one cluster which includes node"
                    " with FQDN == {}.".format(id_hostname))
