import configparser
import pytest
import usmqe.usmssh as usmssh
import usmqe.inventory


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
    fname = re.sub(".*'(?P<name>.*)'.*", '\g<name>', fname)
    # remove 'test_' from the beginning and
    # replace all underscores with spaces
    return fname[5:].replace('_', ' ')


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
    admin role.

    ``params`` parameter takes list of dictionaries where each dictionary
        contains ``username`` and ``password`` as keys.
    """

    return request.param


@pytest.fixture
def valid_new_admin_user(valid_admin_user_data):
    """
    Create user from valid_admin_user_data fixture and return these data.
    At the end remove this user.
    """
    auth = login(
        pytest.config.getini("usm_username"),
        pytest.config.getini("usm_password"))
    admin = tendrlapi_user.ApiUser(auth=auth)
    admin.add_user(valid_admin_user_data)
    yield valid_admin_user_data
    admin.del_user(valid_admin_user_data["username"])
    logout(auth=auth)


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
    normal role.

    ``params`` parameter takes list of dictionaries where each dictionary
        contains ``username`` and ``password`` as keys.
    """
    return request.param


@pytest.fixture
def valid_new_normal_user(valid_normal_user_data):
    """
    Create user from valid_noramal_user_data fixture and return these data.
    At the end remove this user.
    """
    auth = login(
        pytest.config.getini("usm_username"),
        pytest.config.getini("usm_password"))
    admin = tendrlapi_user.ApiUser(auth=auth)
    admin.add_user(valid_normal_user_data)
    yield valid_normal_user_data
    admin.del_user(valid_normal_user_data["username"])
    logout(auth=auth)


@pytest.fixture(params=[
        "new_password_123"
        ])
def valid_password(request):
    """
    Return valid password string.
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
