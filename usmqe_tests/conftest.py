import configparser
import pytest
import time
import datetime
import usmqe.usmssh as usmssh
from usmqe.api.tendrlapi.common import login, logout, TendrlApi
from usmqe.usmqeconfig import UsmConfig


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


@pytest.fixture(scope="session", autouse=True)
def logger_session():
    """
    Close logger on a session scope.
    """
    log_level = CONF.config["usmqe"]["log_level"]
    LOGGER.setLevel(log_level)
    yield
    LOGGER.close()


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


@pytest.fixture(params=[60, 80], scope="session")
def workload_memory_utilization(request):
    """
    Returns:
        dict: contains information about `start` and `stop` time of stress-ng
            command and its `result`
    """
    def fill_memory():
        """
        Use `stress-ng` tool to stress memory for 4 minutes to given percentage
        """
        # stress memory for for 240 seconds
        run_time = 240
        SSH = usmssh.get_ssh()
        host = CONF.config["usmqe"]["cluster_member"]
        stress_cmd = "stress-ng --vm-method flip --vm {} --vm-bytes {}%".format(
            1,
            request.param)
        stress_cmd += " --timeout {}s --vm-hang 0 --vm-keep --verify".format(
            run_time)
        stress_cmd += " --syslog"
        retcode, stdout, stderr = SSH[host].run(stress_cmd)
        if retcode != 0:
            raise OSError(stderr)
        return request.param
    return measure_operation(fill_memory)


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
