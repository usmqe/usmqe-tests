# -*- coding: utf8 -*-


import pytest
import requests

from usmqe.api.tendrlapi.common import TendrlApi
import usmqe.api.base


def test_login(default_session_credentials):
    response = requests.get(
        pytest.config.getini("usm_api_url") + "ping",
        auth=default_session_credentials)
    usmqe.api.base.ApiBase.print_req_info(response)
    usmqe.api.base.ApiBase.check_response(response)


def test_login_invalid():
    asserts = {
        "cookies": None,
        "ok": False,
        "reason": 'Unauthorized',
        "status": 401,
        }
    api = TendrlApi()
    auth = api.login("invalid_user", "invalid_password", asserts_in=asserts)
    response = requests.get(
        pytest.config.getini("usm_api_url") + "ping",
        auth=auth)
    usmqe.api.base.ApiBase.print_req_info(response)
    usmqe.api.base.ApiBase.check_response(response, asserts_in=asserts)


def test_session_invalid(invalid_session_credentials):
    asserts = {
        "cookies": None,
        "ok": False,
        "reason": 'Unauthorized',
        "status": 401,
        }
    response = requests.get(
        pytest.config.getini("usm_api_url") + "ping",
        auth=invalid_session_credentials)
    usmqe.api.base.ApiBase.print_req_info(response)
    usmqe.api.base.ApiBase.check_response(response, asserts_in=asserts)


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
