import pytest

from usmqe.api.tendrlapi.authentication import Authentication

from usmqe.api.tendrlapi.common import TendrlApi

@pytest.fixture(scope="session")
def valid_access_credentials(request):
    """Generate tuple consisting of username and valid access token for
    username and password.

    ``params`` parameter takes list of dictionaries where each dictionary
    contains ``username`` and ``password`` as keys.
    """

    credentials = Authentication()
    credentials.login(
        pytest.config.getini("usm_username"),
        pytest.config.getini("usm_password"))
    return {
        "username": credentials.username,
        "access_token": credentials.access_token,
        "role": credentials.role}


@pytest.fixture(scope="session")
def invalid_access_credentials(request):
    """Generate tuple consisting of username and invalid access token.

    ``params`` parameter takes list of tuples where:
        first value represents username
        second value represents access_token
    """

    return {
        "username": pytest.config.getini("usm_username"),
        "access_token": "invalid00000",
        "role": "admin"}
