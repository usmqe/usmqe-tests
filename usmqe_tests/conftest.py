import pytest
from itertools import cycle


# initialize usmqe logging module
LOGGER = pytest.get_logger("pytests_test")
pytest.set_logger(LOGGER)

parametrized_tests = {}


def get_name(fname):
    """
    Generate test name from method name.
    """
    # get the node name, function with parameters
    import re
    fname = re.sub(".*'(?P<name>.*)'.*", '\g<name>', str(fname))
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
    LOGGER.testStart(get_name(request.node))
    yield
    LOGGER.testEnd()
