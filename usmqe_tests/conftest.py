import configparser
import datetime
import pytest
import time

import usmqe.usmssh as usmssh
import usmqe.inventory
from usmqe.gluster.gluster import GlusterVolume


# initialize usmqe logging module
LOGGER = pytest.get_logger("pytests_test")
pytest.set_logger(LOGGER)


# NOTE beware any usmqe import has to be after LOGGER is initialized not before
#      all import lines must have NOQA flag to be ignored by flake,
#        because all imports have to be at the begginning of the file
#      other possibility is to have imports where they are really needed
from usmqe.api.tendrlapi.common import login, logout  # NOQA flake8
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


def measure_operation(operation, minimal_time=None):
    """
    Get dictionary with keys 'start', 'end' and 'result' that contain
    information about start and stop time of given function and its result.

    Args:
        operation (function): function to be performed.
        minimal_time (int): minimal number of seconds to run, it can be more
            based on given operation

    Returns:
        dict: contains information about `start` and `stop` time of given
            function and its `result`
    """
    start_time = datetime.datetime.now()
    result = operation()
    passed_time = datetime.datetime.now() - start_time
    if minimal_time:
        additional_time = minimal_time - passed_time.total_seconds()
        if additional_time > 0:
            time.sleep(additional_time)
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
    log_level = pytest.config.getini("usm_log_level")
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
        "@example.com", "@" + usmqe.inventory.role2hosts("usm_client")[0])
    return request.param


def create_new_user(user_data):
    """
    Create user from given user_data.
    """
    auth = login(
        pytest.config.getini("usm_username"),
        pytest.config.getini("usm_password"))
    admin = tendrlapi_user.ApiUser(auth=auth)
    admin.add_user(user_data)

    if user_data['email'].endswith(
            usmqe.inventory.role2hosts("usm_client")[0]):
        SSH = usmssh.get_ssh()
        useradd = 'useradd {}'.format(user_data['username'])
        node_connection = SSH[usmqe.inventory.role2hosts("usm_client")[0]]
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
        pytest.config.getini("usm_username"),
        pytest.config.getini("usm_password"))
    admin = tendrlapi_user.ApiUser(auth=auth)
    if user_data['email'].endswith(
            usmqe.inventory.role2hosts("usm_client")[0]):
        SSH = usmssh.get_ssh()
        node_connection = SSH[usmqe.inventory.role2hosts("usm_client")[0]]
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
        "@example.com", "@" + usmqe.inventory.role2hosts("usm_client")[0])
    return request.param


@pytest.fixture
def valid_new_normal_user(valid_normal_user_data):
    """
    Create user from valid_noramal_user_data fixture and return these data.
    At the end remove this user.
    """
    create_new_user(valid_normal_user_data)
    yield valid_normal_user_data
    delete_new_user(valid_normal_user_data)


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
    node_connection = SSH[pytest.config.getini("usm_cluster_member")]
    f_content = node_connection.run(
        os_release)
    f_content = f_content[1].decode("utf-8").replace('"', '')
    config = configparser.ConfigParser()
    config.read_string('[os_info]\n' + f_content)
    LOGGER.debug(config['os_info'])
    return dict(config['os_info'])


@pytest.fixture(params=[60, 80, 95])
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


@pytest.fixture(params=[60, 80])
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
        SSH = usmqe.usmssh.get_ssh()
        host = pytest.config.getini("usm_cluster_member")
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


@pytest.fixture
def volume_mount_points():
    """
    Returns dictionary where keys are volume names in gluster and values
    are directory paths to volume mount points.
    """
    SSH = usmssh.get_ssh()
    # todo(fbalak): use new config
    import usmqe.inventory
    host = usmqe.inventory.role2hosts("usm_client")[0]
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


@pytest.fixture(params=[10])
def workload_capacity_utilization(request, volume_mount_points):
    """
    Returns:
        dict: contains information about `start` and `stop` time of dd
            command and `result` as number presenting percentage of disk
            utilization.
    """
    mount_point = list(volume_mount_points.values())[0].strip()
    SSH = usmssh.get_ssh()
    # todo(fbalak): use new config
    import usmqe.inventory
    host = usmqe.inventory.role2hosts("usm_client")[0]
    def fill_volume():
        """
        Use `dd` command to utilize mounted volume.
        """
        disk_space_cmd = "df {0} --block-size=M | awk '/{1}/ {{print $3 \" \" $4}}'".format(
            mount_point,
            mount_point.split("/")[-1])
        retcode, disk_space, stderr = SSH[host].run(disk_space_cmd)
        if retcode != 0:
            raise OSError(stderr.decode("utf-8"))

        disk_used, disk_available = [size.rstrip("\n").rstrip("M") for size in disk_space.decode("utf-8").split(" ")]

        # block size = 10M
        block_size = 10
        # compute disk space that is going to be used and number of files
        # to create with regard to already utilized space
        file_count = int((
            (int(disk_available) / 100 * request.param)
            - int(disk_used)) / block_size)

        stress_cmd = "for x in {{1..{}}}; do dd if=/dev/null of={}/test_file$x count=1 bs={}M; done".format(
            file_count,
            mount_point[:-1] if mount_point.endswith("/") else mount_point,
            block_size)
        retcode, _, stderr = SSH[host].run(stress_cmd)
        if retcode != 0:
            raise OSError(stderr.decode("utf-8"))
        return request.param

    yield measure_operation(fill_volume)

    cleanup_cmd = "rm -f {}/test_file*".format(
        mount_point[:-1] if mount_point.endswith("/") else mount_point)
    retcode, _, stderr = SSH[host].run(cleanup_cmd)
    if retcode != 0:
        raise OSError(stderr.decode("utf-8"))
