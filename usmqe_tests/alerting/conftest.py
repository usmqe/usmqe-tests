import pytest
import time
from usmqe.gluster import gluster
from usmqe.usmqeconfig import UsmConfig
import usmqe.usmssh as usmssh
from usmqe_tests.conftest import measure_operation
from pytest_ansible_playbook import runner

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


@pytest.fixture(scope="module")
def workload_stop_volumes(request):
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
        LOGGER.info("Measure time when volumes are stopped.")
        time.sleep(180)
        return gl_volumes.list()
    with runner(
            request,
            ["test_setup.gluster_volume_stop.yml"],
            ["test_teardown.gluster_volume_stop.yml"]):
        yield measure_operation(wait)
    msg = "Wait 5 seconds to make sure that all volumes are correctly loaded"
    LOGGER.info(msg)
    time.sleep(5)


@pytest.fixture(scope="module")
def workload_stop_hosts(request):
    """
    Test ran with this fixture have to use fixture `ansible_playbook`
    and markers before this fixture is called:
    @pytest.mark.ansible_playbook_setup("test_setup.tendrl_services_stopped_on_nodes.yml")
    @pytest.mark.ansible_playbook_teardown("test_teardown.tendrl_services_stopped_on_nodes.yml")
    Returns:
        dict: contains information about `start` and `stop` time of wait
        procedure and as `result` is used number of nodes.
    """
    def wait():
        LOGGER.info("Measure time when hosts are stopped.")
        time.sleep(180)
        return CONF.inventory.get_groups_dict()["gluster_servers"]
    with runner(
            request,
            ["test_setup.tendrl_services_stopped_on_nodes.yml"],
            ["test_teardown.tendrl_services_stopped_on_nodes.yml"]):
        yield measure_operation(wait)
    msg = "Wait 10 seconds to make sure that all services are correctly loaded"
    LOGGER.info(msg)
    time.sleep(10)


@pytest.fixture(params=[85, 30], scope="module")
def workload_cpu_utilization_alerts(request):
    """
    Stress Cpu utilization on `cluster_member` node to value given in
    parameter and measure the time it was utilized. If provided parameter
    is below 80 (alert breach threshold) then the node is first utilized
    to 85% and after that it is utilized again and measured.

    Returns:
        dict: contains information about `start` and `stop` time of stress-ng
            command and its `result`
    """
    def fill_cpu():
        """
        Use `stress-ng` tool to stress cpu for 3 minutes to given percentage
        """
        # stress cpu for for 180 seconds
        run_time = 180
        SSH = usmssh.get_ssh()
        host = CONF.config["usmqe"]["cluster_member"]
        processors_cmd = "grep -c ^processor /proc/cpuinfo"
        retcode, processors_count, _ = SSH[host].run(processors_cmd)
        stress_cmd = "stress-ng --cpu {} -l {} --timeout {}s".format(
            int(processors_count),
            fill_pct,
            run_time)
        retcode, stdout, stderr = SSH[host].run(stress_cmd)
        if retcode != 0:
            raise OSError(stderr)
        return fill_pct
    if request.param < 80:
        fill_pct = 85
        fill_cpu()
    fill_pct = request.param
    return measure_operation(fill_cpu)


@pytest.fixture(params=[89, 30], scope="module")
def workload_memory_utilization_alerts(request):
    """
    Stress memory utilization on `cluster_member` node to value given in
    parameter and measure the time it was utilized. If provided parameter
    is below 80 (alert breach threshold) then the node is first utilized
    to 89% and after that it is utilized again and measured.

    Returns:
        dict: contains information about `start` and `stop` time of stress-ng
            command and its `result`
    """
    def fill_memory():
        """
        Use `stress` tool to stress memory for 3 minutes to given percentage
        """
        # stress memory for for 180 seconds
        run_time = 180
        SSH = usmssh.get_ssh()
        host = CONF.config["usmqe"]["cluster_member"]
        stress_cmd = "stress --vm-bytes $(awk '/MemAvailable/{{printf "\
                     "\"%d\\n\" , $2 * ({0}/100);}}' < /proc/meminfo)k "\
                     "--vm-keep -m {1}".format(fill_pct, 1)
        stress_cmd += " --timeout {}s".format(
            run_time)
        retcode, stdout, stderr = SSH[host].run(stress_cmd)
        if retcode != 0:
            raise OSError(stderr)
        return fill_pct
    if request.param < 80:
        fill_pct = 89
        fill_memory()
    fill_pct = request.param
    return measure_operation(fill_memory)
