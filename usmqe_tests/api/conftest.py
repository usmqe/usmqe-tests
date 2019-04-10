# -*- coding: utf8 -*-

import pytest
import pytest_ansible_playbook

from usmqe.api.tendrlapi import glusterapi
from usmqe.api.tendrlapi.common import TendrlAuth
from usmqe.usmqeconfig import UsmConfig

CONF = UsmConfig()


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
    username = CONF.config["usmqe"]["username"]
    invalid_token = request.param
    auth = TendrlAuth(token=invalid_token, username=username)
    return auth


@pytest.fixture
def importfail_setup_nodeagent_stopped_on_one_node(
        request,
        managed_cluster,
        valid_session_credentials):
    """
    This fixture stops node agent on one storage machine. During teardown it
    makes sure that the node agent is back and then runs unmanage job to
    cleanup state after a failed import.

    Don't use this fixture if you are not running negative test cases for
    import cluster feature.
    """
    with pytest_ansible_playbook.runner(
            request,
            ["test_setup.tendrl_nodeagent_stopped_on_one_node.yml"],
            ["test_teardown.tendrl_nodeagent_stopped_on_one_node.yml"]):
        yield
    # And now something completely different: we need to run unmanage because
    # the cluster is not managed after a failed import, which would block any
    # future import attempt.
    tendrl = glusterapi.TendrlApiGluster(auth=valid_session_credentials)
    job = tendrl.unmanage_cluster(managed_cluster["cluster_id"])
    tendrl.wait_for_job_status(job["job_id"])
