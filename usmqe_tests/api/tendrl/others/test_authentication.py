# -*- coding: utf8 -*-


import pytest

from usmqe.api.tendrlapi.common import TendrlApi, login, logout


def test_login_valid(default_session_credentials):
    api = TendrlApi(auth=default_session_credentials)
    api.ping()


def test_login_invalid():
    asserts = {
        "cookies": None,
        "ok": False,
        "reason": 'Unauthorized',
        "status": 401,
        }
    auth = login("invalid_user", "invalid_password", asserts_in=asserts)
    api = TendrlApi(auth)
    api.ping(asserts_in=asserts)


def test_session_unauthorized():
    asserts = {
        "cookies": None,
        "ok": False,
        "reason": 'Unauthorized',
        "status": 401,
        }
    # passing auth=None would result in api requests to be done without Tendrl
    # auth header
    api = TendrlApi(auth=None)
    api.ping(asserts_in=asserts)


def test_session_invalid(invalid_session_credentials):
    asserts = {
        "cookies": None,
        "ok": False,
        "reason": 'Unauthorized',
        "status": 401,
        }
    api = TendrlApi(auth=invalid_session_credentials)
    api.ping(asserts_in=asserts)


# TODO: find out why xfail doesn't work here
@pytest.mark.xfail(reason='https://github.com/Tendrl/api/issues/118')
def test_login_multiple_sessions():
    auth_one = login(
        pytest.config.getini("usm_username"),
        pytest.config.getini("usm_password"))
    auth_two = login(
        pytest.config.getini("usm_username"),
        pytest.config.getini("usm_password"))
    logout(auth=auth_one)
    logout(auth=auth_two)


# TODO: find out why xfail doesn't work here
@pytest.mark.xfail(reason='https://github.com/Tendrl/api/issues/118')
def test_login_multiple_sessions_twisted():
    asserts = {
        "cookies": None,
        "ok": False,
        "reason": 'Unauthorized',
        "status": 401,
        }
    api_one = TendrlApi(auth=login(
        pytest.config.getini("usm_username"),
        pytest.config.getini("usm_password")))
    api_two = TendrlApi(auth=login(
        pytest.config.getini("usm_username"),
        pytest.config.getini("usm_password")))
    api_one.ping()
    api_two.ping()
    logout(auth=api_one._auth)
    api_one.ping(asserts_in=asserts)
    api_two.ping()
    logout(auth=api_two._auth)
    api_one.ping(asserts_in=asserts)
    api_two.ping(asserts_in=asserts)
