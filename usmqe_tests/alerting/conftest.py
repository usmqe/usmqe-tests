import pytest
import time
from usmqe.gluster import gluster
from usmqe.usmqeconfig import UsmConfig
from usmqe_tests.conftest import measure_operation

# initialize usmqe logging module
LOGGER = pytest.get_logger("pytests_test")
pytest.set_logger(LOGGER)
CONF = UsmConfig()

@pytest.fixture(scope="function", autouse=True)
def default_entities(cluster_reuse):
    """
    Returns basic items that are occuring in alert messages and can be used
    for substitution.
    """
    cluster_identifier = cluster_reuse[
        "short_name"] or cluster_reuse["cluster_id"]
    node = CONF.config["usmqe"]["cluster_member"]
    return {
            "cluster": cluster_identifier,
            "node": node}


@pytest.fixture
def workload_stop_volumes():
    """
    Test ran with this fixture have to use fixture `ansible_playbook`
    and markers before this fixture is called:
    @pytest.mark.ansible_playbook_setup("test_setup.gluster_volume_stop.yml")
    @pytest.mark.ansible_playbook_teardown("test_teardown.gluster_volume_stop.yml")
    Returns:
        dict: contains information about `start` and `stop` time of wait
        procedure and as `result` is used number of nodes.
    """
    def wait():
        gl_volumes = gluster.GlusterVolume()
        LOGGER.info("Measure time when volumes stopped.")
        time.sleep(240)
        return gl_volumes.list()
    return measure_operation(wait)
