import pytest
import datetime
import usmqe.usmssh
from usmqe.api.tendrlapi import glusterapi

LOGGER = pytest.get_logger('grafana_conftest', module=True)


def measure_operation(operation):
    """
    Get dictionary with keys 'start', 'end' and 'result' that contain
    information about start and stop time of given function and its result.

    Args:
        operation (function): Function to be performed.

    Returns:
        dict: contains information about `start` and `stop` time of given
            function and its `result`
    """
    start_time = datetime.datetime.now()
    result = operation()
    end_time = datetime.datetime.now()
    return {
        "start": start_time,
        "end": end_time,
        "result": result}


@pytest.fixture(params=[60, 80, 95])
def measured_cpu_utilization(request):
    """
    Returns:
        dict: contains information about `start` and `stop` time of stress-ng
            command and its `result`
    """
    def fill_cpu():
        """
        Use `stress-ng` tool to stress cpu for 1 minute to given percentage
        """
        # stress cpu for for 180 seconds
        run_time = 180
        SSH = usmqe.usmssh.get_ssh()
        host = pytest.config.getini("usm_cluster_member")
        processors_cmd = "grep -c ^processor /proc/cpuinfo"
        retcode, processors_count, _ = SSH[host].run(processors_cmd)
        stress_cmd = "stress-ng --cpu {} -l {} --timeout {}s".format(
            int(processors_count),
            request.param,
            run_time)
        retcode, stdout, stderr = SSH[host].run(stress_cmd)
        if retcode != 0:
            raise OSError(stderr)
        return request.param

    return measure_operation(fill_cpu)


@pytest.fixture
def valid_nodes(valid_session_credentials):
    """
    Generate valid host info from GetNodeList api call related to tendrl/nodes
    """
    api = glusterapi.TendrlApiGluster(auth=valid_session_credentials)
    cluster_list = api.get_nodes()
    return [x for x in cluster_list["nodes"]
            if "tendrl/node" in x["tags"] and x["status"] == "UP"]
