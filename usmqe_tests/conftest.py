import configparser
import datetime
import time
from urllib.parse import urlparse
import pytest

import usmqe.usmssh as usmssh
from pytest_ansible_playbook import runner
from usmqe.api.tendrlapi.common import login, logout, TendrlApi
from usmqe.web.application import Application
from usmqe.usmqeconfig import UsmConfig
from usmqe.gluster.gluster import GlusterVolume


# initialize usmqe logging module
LOGGER = pytest.get_logger("pytests_test")
pytest.set_logger(LOGGER)
CONF = UsmConfig()


# NOTE beware any usmqe import has to be after LOGGER is initialized not before
#      all import lines must have NOQA flag to be ignored by flake,
#        because all imports have to be at the begginning of the file
#      other possibility is to have imports where they are really needed
from usmqe.api.tendrlapi import user as tendrlapi_user  # NOQA flake8


def get_name(fname):
    """
    Generate test name from method name.

    Parameters:
        fname (string): function name with parametrized arguments
                        e.g. "Test <Function 'test_my_method[1-my_arg-42]'>"
    """
    # take only function name with its parameters
    import re
    fname = re.sub(".*'(?P<name>.*)'.*", r'\g<name>', fname)
    # remove 'test_' from the beginning and
    # replace all underscores with spaces
    return fname[5:].replace('_', ' ')


def measure_operation(
        operation, minimal_time=None, metadata=None, measure_after=False):
    """
    Get dictionary with keys 'start', 'end' and 'result' that contain
    information about start and stop time of given function and its result.

    Args:
        operation (function): function to be performed.
        minimal_time (int): minimal number of seconds to run, it can be more
            based on given operation
        metadata (dict): this can contain dictionary object with information
            relevant to test (e.g. volume name, operating host, ...)
        measure_after (bool): determine if time measurement is done before or
            after the operation returns its state

    Returns:
        dict: contains information about `start` and `stop` time of given
            function and its `result`
    """
    if not measure_after:
        start_time = datetime.datetime.now()
    result = operation()
    if measure_after:
        start_time = datetime.datetime.now()
    passed_time = datetime.datetime.now() - start_time
    if minimal_time:
        additional_time = minimal_time - passed_time.total_seconds()
        if additional_time > 0:
            time.sleep(additional_time)
    end_time = datetime.datetime.now()
    LOGGER.info("Wait 10 seconds for graphite to load dataframes")
    time.sleep(10)
    return {
        "start": start_time,
        "end": end_time,
        "result": result,
        "metadata": metadata}


@pytest.fixture(scope="session", autouse=True)
def logger_session():
    """
    Close logger on a session scope.
    """
    log_level = CONF.config["usmqe"]["log_level"]
    LOGGER.setLevel(log_level)
    yield
    LOGGER.close()


@pytest.fixture(scope="function", autouse=True)
def logger_testcase(request):
    """
    Mark start and end of a test case using usmqe logger.
    """
    print()
    LOGGER.testStart(get_name(str(request.node)))
    yield
    LOGGER.testEnd()


@pytest.fixture(
    params=[{
        "name": "Tom Admin",
        "username": "tom-admin",
        "email": "tom-admin@example.com",
        "role": "admin",
        "password": "tomadmin1234",
        "email_notifications": False}])
def valid_admin_user_data(request):
    """
    Generate valid data that can be imported into tendrl as a new user with
    admin role. `example.com` domain is replaced with hostname `usm_client`
    inventory file role.

    ``params`` parameter takes list of dictionaries where each dictionary
        contains ``username`` and ``password`` as keys.
    """
    request.param["email"] = request.param["email"].replace(
        "@example.com", "@" + CONF.inventory.get_groups_dict()["usm_client"][0])
    return request.param


def create_new_user(user_data):
    """
    Create user from given user_data.
    """
    auth = login(
        CONF.config["usmqe"]["username"],
        CONF.config["usmqe"]["password"])
    admin = tendrlapi_user.ApiUser(auth=auth)
    admin.add_user(user_data)

    if user_data['email'].endswith(
            CONF.inventory.get_groups_dict()["usm_client"][0]):
        SSH = usmssh.get_ssh()
        useradd = 'useradd {}'.format(user_data['username'])
        node_connection = SSH[CONF.inventory.get_groups_dict()["usm_client"][0]]
        node_connection.run(useradd)
        passwd = 'echo "{}" | passwd --stdin {}'.format(
            user_data['password'],
            user_data['username'])
        passwd_response = node_connection.run(passwd)
        # passwd command returned 0 return code
        assert passwd_response[0] == 0


def delete_new_user(user_data):
    """
    Delete user with given user_data.
    """
    auth = login(
        CONF.config["usmqe"]["username"],
        CONF.config["usmqe"]["password"])
    admin = tendrlapi_user.ApiUser(auth=auth)
    if user_data['email'].endswith(
            CONF.inventory.get_groups_dict()["usm_client"][0]):
        SSH = usmssh.get_ssh()
        node_connection = SSH[CONF.inventory.get_groups_dict()["usm_client"][0]]
        userdel = 'userdel {}'.format(user_data['username'])
        userdel_response = node_connection.run(userdel)
        # userdel command returned 0 return code
        assert userdel_response[0] == 0
    admin.del_user(user_data["username"])
    logout(auth=auth)


@pytest.fixture
def valid_new_admin_user(valid_admin_user_data):
    """
    Create user from valid_admin_user_data fixture and return these data.
    At the end remove this user.
    """
    create_new_user(valid_admin_user_data)
    yield valid_admin_user_data
    delete_new_user(valid_admin_user_data)


@pytest.fixture(
    params=[{
        "name": "Jerry Normal",
        "username": "jerry-normal",
        "email": "jerry-normal@example.com",
        "role": "normal",
        "password": "jerrynormal1234",
        "email_notifications": False}])
def valid_normal_user_data(request):
    """
    Generate valid data that can be imported into tendrl as a new user with
    normal role. `example.com` domain is replaced with hostname `usm_client`
    inventory file role.

    ``params`` parameter takes list of dictionaries where each dictionary
        contains ``username`` and ``password`` as keys.
    """
    request.param["email"] = request.param["email"].replace(
        "@example.com", "@" + CONF.inventory.get_groups_dict()["usm_client"][0])
    return request.param


@pytest.fixture(
    params=[{
        "name": "Jerry Limited",
        "username": "jerry-limited",
        "email": "jerry-limited@example.com",
        "role": "limited",
        "password": "jerrylimited1234",
        "email_notifications": False}])
def valid_limited_user_data(request):
    """
    Generate valid data that can be imported into tendrl as a new user with
    limited role. `example.com` domain is replaced with hostname `usm_client`
    inventory file role.

    ``params`` parameter takes list of dictionaries where each dictionary
        contains ``username`` and ``password`` as keys.
    """
    request.param["email"] = request.param["email"].replace(
        "@example.com", "@" + CONF.inventory.get_groups_dict()["usm_client"][0])
    return request.param


@pytest.fixture
def valid_new_normal_user(valid_normal_user_data):
    """
    Create user from valid_normal_user_data fixture and return these data.
    At the end remove this user.
    """
    create_new_user(valid_normal_user_data)
    yield valid_normal_user_data
    delete_new_user(valid_normal_user_data)


@pytest.fixture
def valid_new_limited_user(valid_limited_user_data):
    """
    Create user from valid_limited_user_data fixture and return these data.
    At the end remove this user.
    """
    create_new_user(valid_limited_user_data)
    yield valid_normal_user_data
    delete_new_user(valid_limited_user_data)


@pytest.fixture(params=[
        "new_password_123",
        "123456789",
        "a" * 128,
        ])
def valid_password(request):
    """
    Return valid password string.
    """
    return request.param


@pytest.fixture(params=[
        "",
        "a",
        "tooshort",
        "a" * 129,
        ])
def invalid_password(request):
    """
    Return invalid password string.
    Password length requirements are described here:
    https://bugzilla.redhat.com/show_bug.cgi?id=1610913
    """
    return request.param


@pytest.fixture(params=[
        "wee4",
        "a2345678901234567890",
        ])
def valid_username(request):
    """
    Return valid username string.
    Password length requirements are described here:
    https://bugzilla.redhat.com/show_bug.cgi?id=1610913
    """
    return request.param


@pytest.fixture(params=[
        "wee",
        "toolong" + "a" * 14,
        "a23456789012345678901",
        ])
def invalid_username(request):
    """
    Return invalid username string.
    Password length requirements are described here:
    https://bugzilla.redhat.com/show_bug.cgi?id=1610913
    """
    return request.param


@pytest.fixture
def os_info():
    """
    Return information from /etc/os-release file about current os distribution.
    """
    SSH = usmssh.get_ssh()
    os_release = 'cat /etc/os-release'
    node_connection = SSH[CONF.config["usmqe"]["cluster_member"]]
    f_content = node_connection.run(
        os_release)
    f_content = f_content[1].decode("utf-8").replace('"', '')
    config = configparser.ConfigParser()
    config.read_string('[os_info]\n' + f_content)
    LOGGER.debug(config['os_info'])
    return dict(config['os_info'])


@pytest.fixture(params=[60, 80, 95], scope="session")
def workload_cpu_utilization(request):
    """
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
            request.param,
            run_time)
        retcode, stdout, stderr = SSH[host].run(stress_cmd)
        if retcode != 0:
            raise OSError(stderr)
        return request.param
    return measure_operation(fill_cpu)


@pytest.fixture(scope="session")
def application():
    url = urlparse(CONF.config["usmqe"]["web_url"])
    app = Application(
        hostname=url.hostname,
        scheme=url.scheme,
        username=CONF.config["usmqe"]["username"],
        password=CONF.config["usmqe"]["password"]
    )
    yield app
    app.web_ui.browser_manager.quit()


@pytest.fixture(scope="session")
def valid_session_credentials(request):
    """
    During setup phase, login default usmqe user account (username and password
    comes from usm.ini config file) and return requests auth object.
    Then during teardown logout the user to close the session.
    """
    auth = login(
        CONF.config["usmqe"]["username"],
        CONF.config["usmqe"]["password"])
    yield auth
    logout(auth=auth)


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
    id_hostname = CONF.config["usmqe"]["cluster_member"]
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


@pytest.fixture(params=[80, 60], scope="session")
def workload_memory_utilization(request):
    """
    Returns:
        dict: contains information about `start` and `stop` time of stress-ng
            command and its `result`
    """
    def fill_memory():
        """
        Use `stress` tool to stress memory for 4 minutes to given percentage
        """
        # stress memory for for 240 seconds
        run_time = 240
        SSH = usmssh.get_ssh()
        host = CONF.config["usmqe"]["cluster_member"]
        stress_cmd = "stress --vm-bytes $(awk '/MemAvailable/{{printf "\
                     "\"%d\\n\" , $2 * ({0}/100);}}' < /proc/meminfo)k "\
                     "--vm-keep -m {1}".format(request.param, 1)
        stress_cmd += " --timeout {}s".format(
            run_time)
        retcode, stdout, stderr = SSH[host].run(stress_cmd)
        if retcode != 0:
            raise OSError(stderr)
        return request.param
    SSH = usmssh.get_ssh()
    host = CONF.config["usmqe"]["cluster_member"]
    meminfo_cmd = "free -b | awk '{if (NR==2) print $2}'"
    retcode, stdout, stderr = SSH[host].run(meminfo_cmd)
    if retcode != 0:
        raise OSError(stderr)
    mem_total = stdout.decode("utf-8")
    return measure_operation(fill_memory, metadata={
        'total_memory': mem_total})


@pytest.fixture(scope="session")
def volume_mount_points():
    """
    Returns dictionary where keys are volume names in gluster and values
    are directory paths to volume mount points.
    """
    SSH = usmssh.get_ssh()
    host = CONF.inventory.get_groups_dict()["usm_client"][0]
    gluster_volume = GlusterVolume()
    volumes = gluster_volume.list()
    mount_points = {}

    for volume in volumes:
        mount_point_cmd = "mount | awk '/{}/ {{print $3}}'".format(volume)
        retcode, mount_point, stderr = SSH[host].run(mount_point_cmd)
        if retcode != 0:
            raise OSError(stderr.decode("utf-8"))
        mount_points[volume] = mount_point.decode("utf-8")
    return mount_points


@pytest.fixture(params=[76, 91], scope="session")
def workload_capacity_utilization(request, volume_mount_points):
    """
    Returns:
        dict: contains information about `start` and `stop` time of dd
            command and `result` as number presenting percentage of disk
            utilization.
    """
    volume_name = list(volume_mount_points.keys())[0]
    mount_point = volume_mount_points[volume_name].strip()
    SSH = usmssh.get_ssh()
    host = CONF.inventory.get_groups_dict()["usm_client"][0]

    def fill_volume():
        """
        Use `dd` command to utilize mounted volume.
        """
        disk_space_cmd = "df {0} | awk '/{1}/ " \
            "{{print $3 \" \" $4}}'".format(
                mount_point,
                mount_point.split("/")[-1])
        retcode, disk_space, stderr = SSH[host].run(disk_space_cmd)
        if retcode != 0:
            raise OSError(stderr.decode("utf-8"))

        # disk values in M
        disk_used, disk_available = [
            int(size.rstrip("\n")) / 1024 for size in disk_space.decode(
                "utf-8").split(" ")]

        # block size = 100M
        block_size = 100
        # compute disk space that is going to be used and number of files
        # to create with regard to already utilized space
        file_count = int((
            (int(disk_available) / 100 * request.param) - int(disk_used)
                ) / block_size)

        stress_cmd = "for x in {{1..{}}}; do dd if=/dev/zero" \
            " of={}/test_file$x count=1 bs={}M; done".format(
                file_count,
                mount_point[:-1] if mount_point.endswith("/") else mount_point,
                block_size)
        retcode, _, stderr = SSH[host].run(stress_cmd)
        if retcode != 0:
            raise OSError(stderr.decode("utf-8"))
        return request.param

    disk_space_cmd = "df {0} | awk '/{1}/ {{print $2}}'".format(
        mount_point,
        mount_point.split("/")[-1])
    retcode, disk_total, stderr = SSH[host].run(disk_space_cmd)
    if retcode != 0:
        raise OSError(stderr.decode("utf-8"))

    time_to_measure = 180
    yield measure_operation(
        fill_volume,
        minimal_time=time_to_measure,
        metadata={
            "volume_name": volume_name,
            "total_capacity": int(disk_total.decode("utf-8").rstrip("\n"))},
        measure_after=True)

    cleanup_cmd = "rm -f {}/test_file*".format(
        mount_point[:-1] if mount_point.endswith("/") else mount_point)
    retcode, _, stderr = SSH[host].run(cleanup_cmd)
    if retcode != 0:
        raise OSError(stderr.decode("utf-8"))


@pytest.fixture(params=[70, 95], scope="session")
def workload_swap_utilization(request):
    """
    Returns:
        dict: contains information about `start` and `stop` time of stress-ng
            command and its `result`
    """
    def fill_memory():
        """
        Use `stress-ng` tool to stress swap memory for 4 minutes to given
        percentage
        """
        run_time = 240
        SSH = usmssh.get_ssh()
        host = CONF.config["usmqe"]["cluster_member"]

        # get total and swap memory of machine via /proc/meminfo file
        meminfo_cmd = """awk '{if ($1=="MemTotal:" || $1=="SwapTotal:") print $2}' /proc/meminfo"""
        _, stdout, _ = SSH[host].run(meminfo_cmd)
        mem_total, swap_total, _ = stdout.decode("utf-8").split("\n")

        # how much memory is going to be consumed considered both normal memory
        # and swap
        memory_percent = 100 + (
            int(swap_total)/int(mem_total) * int(request.param))

        stress_cmd = "stress-ng --vm-method flip --vm {} --vm-bytes {}%".format(
            1,
            int(memory_percent))
        stress_cmd += " --timeout {}s --vm-hang 0 --vm-keep --verify".format(
            run_time)
        stress_cmd += " --syslog"
        retcode, stdout, stderr = SSH[host].run(stress_cmd)
        if retcode != 0:
            raise OSError(stderr)

        teardown_cmd = "sleep 3; swapoff -a && swapon -a; sleep 5"
        SSH[host].run(teardown_cmd)
        return request.param
    return measure_operation(fill_memory)


@pytest.fixture
def workload_stop_nodes():
    """
    Test ran with this fixture have to use fixture `ansible_playbook`
    and markers before this fixture is called:

    @pytest.mark.ansible_playbook_setup("test_setup.stop_tendrl_nodes.yml")
    @pytest.mark.ansible_playbook_teardown("test_teardown.stop_tendrl_nodes.yml")

    Returns:
        dict: contains information about `start` and `stop` time of wait
        procedure and as `result` is used number of nodes.
    """
    LOGGER.info("Wait for tendrl to notice that nodes are down")
    time.sleep(280)

    def wait():
        LOGGER.info("Measure time when tendrl notices that nodes are down.")
        time.sleep(120)
        return len(CONF.inventory.get_groups_dict()["gluster_servers"])
    return measure_operation(wait)


@pytest.fixture()
def gluster_volume(request):
    """
    Use this fixture when a test case needs at least one gluster volume. This
    fixture checks that there is available at least number of volumes
    specified in configuration option `volume_count`. If this option is
    not provided or if it is set to `0` then tests that use this fixture will
    be skipped.
    """
    if 'volume_count' in CONF.config['usmqe'] and CONF.config[
            'usmqe']['volume_count'] > 0:
        gluster_volume = GlusterVolume()
        volumes = gluster_volume.list()
        assert len(volumes) >= CONF.config['usmqe']['volume_count']
    else:
        pytest.skip('Test needs a volume and an option `volume_count`'
                    ' set accordingly.')


@pytest.fixture(scope="session")
def stress_tools(request):
    """
    Install `stress` and `stress-ng` on gluster machines.
    """
    with runner(
            request,
            ["test_setup.stress_tools.yml"],
            ["test_teardown.stress_tools.yml"]):
        yield
