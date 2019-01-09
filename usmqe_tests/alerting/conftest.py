import pytest
from usmqe.usmqeconfig import UsmConfig

CONF = UsmConfig()

@pytest.fixture(scope="function", autouse=True)
def default_entities(cluster_reuse):
    """
    Returns basic items that are occuring in alert messages and can be used
    for substitution.
    """
    cluster_identifier = cluster_reuse["cluster_name"] or cluster_reuse["cluster_id"]
    node = CONF.config["usmqe"]["cluster_member"]
    return {
            "cluster": cluster_identifier,
            "node": node}
