import pytest
import usmqe.usmssh as usmssh
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

@pytest.fixture
def total_host_memory():
    """
    Get total memory of host in bytes.
    """
    SSH = usmssh.get_ssh()
    host = pytest.config.getini("usm_cluster_member")
    meminfo_cmd = "free -b | awk '{if (NR==2) print $2}'"
    _, stdout, _ = SSH[host].run(meminfo_cmd)
    mem_total = stdout.decode("utf-8")
    return mem_total
