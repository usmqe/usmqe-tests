import pytest


# initialize usmqe logging module
LOGGER = pytest.get_logger('rest_api_test')
pytest.set_logger(LOGGER)


def get_name(fname):
    """
    Generate test name from method name.
    """
    return fname.lstrip('test_').replace('_', ' ')


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
    LOGGER.testStart(get_name(request.function.__name__))
    yield
    LOGGER.testEnd()
