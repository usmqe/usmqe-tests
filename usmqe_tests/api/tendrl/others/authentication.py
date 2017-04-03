# -*- coding: utf8 -*-


import pytest

from usmqe.api.tendrlapi.common import TendrlApi


def test_login(default_session_credentials):
    api = TendrlApi()
    api.ping(auth=default_session_credentials)


def test_login_invalid():
    asserts = {
        "cookies": None,
        "ok": False,
        "reason": 'Unauthorized',
        "status": 401,
        }
    api = TendrlApi()
    auth = api.login("invalid_user", "invalid_password", asserts_in=asserts)
    api.ping(auth=auth, asserts_in=asserts)


def test_session_invalid(invalid_session_credentials):
    asserts = {
        "cookies": None,
        "ok": False,
        "reason": 'Unauthorized',
        "status": 401,
        }
    api = TendrlApi()
    api.ping(auth=invalid_session_credentials, asserts_in=asserts)


# TODO: find out why xfail doesn't work here
@pytest.mark.xfail(reason='https://github.com/Tendrl/api/issues/118')
def test_multiple_sessions():
    api = TendrlApi()
    auth_one = api.login(
        pytest.config.getini("usm_username"),
        pytest.config.getini("usm_password"))
    auth_two = api.login(
        pytest.config.getini("usm_username"),
        pytest.config.getini("usm_password"))
    api.logout(auth=auth_one)
    api.logout(auth=auth_two)
