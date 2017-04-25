import pytest
from usmqe.api.tendrlapi.common import login, logout
from usmqe.api.tendrlapi import user as tendrlapi_user


# initialize usmqe logging module
log_level = pytest.config.getini("usm_log_level")
LOGGER = pytest.get_logger("pytests_test", level=log_level)
pytest.set_logger(LOGGER)


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


# TODO(fbalak) remove line with `password_confirmation` after
# https://github.com/Tendrl/api/issues/106 is resolved
@pytest.fixture(
    params=[{
        "name": "Tom Hardy",
        "username": "thardy",
        "email": "thardy@tendrl.org",
        "role": "admin",
        "password": "pass1234",
        "password_confirmation": "pass1234"}])
def valid_user_data(request):
    """
    Generate valid data that can be imported into tendrl as a new user.

    ``params`` parameter takes list of dictionaries where each dictionary
        contains ``username`` and ``password`` as keys.
    """

    return request.param


@pytest.fixture
def valid_new_user(valid_user_data):
    """
    Create user from valid_user_data fixture and return these data.
    At the end remove this user.
    """

    auth = login(
        pytest.config.getini("usm_username"),
        pytest.config.getini("usm_password"))
    admin = tendrlapi_user.ApiUser(auth=auth)
    admin.add_user(valid_user_data)
    yield valid_user_data
    admin.del_user(valid_user_data["username"])
    logout(auth=auth)


@pytest.fixture(params=[
        "new_password_123"
        ])
def valid_password(request):
    """
    Return valid password string.
    """
    return request.param
