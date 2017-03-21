import pytest

from usmqe.api.tendrlapi.authentication import Authentication


@pytest.fixture(params=[{
    "username": pytest.config.getini("username"),
    "password": pytest.config.getini("password")}], scope="module")
def valid_access_credentials(request):
    """Generate tuple consisting of username and valid access token for
    username and password.

    ``params`` parameter takes list of dictionaries where each dictionary
    contains ``username`` and ``password`` as keys.
    """

    credentials = Authentication()
    credentials.login(request.param[0], request.param[1])
    return {
        "username": credentials.username,
        "access_token": credentials.access_token}


@pytest.fixture(params=[{
    "username": pytest.config.getini("username"),
    "access_token": "invalid00000"}], scope="module")
def invalid_access_credentials(request):
    """Generate tuple consisting of username and invalid access token.

    ``params`` parameter takes list of tuples where:
        first value represents username
        second value represents access_token
    """

    return request.param
