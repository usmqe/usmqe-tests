import pytest
from usmqe.api.tendrlapi import glusterapi

LOGGER = pytest.get_logger('grafana_conftest', module=True)


@pytest.fixture
def up_gluster_nodes(valid_session_credentials):
    """
    Generate valid host info from GetNodeList api call related to tendrl/nodes
    for hosts that are UP.
    """
    api = glusterapi.TendrlApiGluster(auth=valid_session_credentials)
    cluster_list = api.get_nodes()
    return [x for x in cluster_list["nodes"]
            if "tendrl/node" in x["tags"] and x["status"] == "UP"]
