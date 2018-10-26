"""
REST API test suite - gluster nodes
"""
import pytest
from usmqe.api.tendrlapi import glusterapi


LOGGER = pytest.get_logger('volume_nodes', module=True)


@pytest.mark.author("dahorak@redhat.com")
@pytest.mark.testready
@pytest.mark.happypath
@pytest.mark.gluster
def test_nodes_list(
        valid_session_credentials,
        cluster_reuse,
        valid_trusted_pool_reuse):
    """
    List nodes for given cluster via API.

    :step:
      Connect to Tendrl API via GET request to ``APIURL/:cluster_id/nodes``
      Where cluster_id is set to predefined value.
    :result:
      Server should return response in JSON format:
      Return code should be **200** with data ``{"nodes": [{...}, ...]}``.
    """

    api = glusterapi.TendrlApiGluster(auth=valid_session_credentials)

    # list of nodes from Tendrl api
    t_nodes = api.get_node_list(cluster_reuse['cluster_id'])
    t_node_names = {node["fqdn"] for node in t_nodes["nodes"]}
    # list of nodes from Gluster command output
    g_node_names = set(valid_trusted_pool_reuse)

    LOGGER.info("list of nodes from Tendrl api: %s", str(t_node_names))
    LOGGER.info("list of nodes from gluster: %s", g_node_names)
    pytest.check(
        t_node_names == g_node_names,
        "List of nodes from Gluster should be the same as from Tendrl API.")