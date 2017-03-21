"""
Tendrl REST API.
"""

import json

import requests

import pytest

from usmqe.api.tendrlapi import tendrlgapi

LOGGER = pytest.get_logger("tendrlapi.authentication", module=True)


class Authentication(tendrlapi.ApiCommon):
    """ Main class for interact with REST API - authentication."""

    def login(self, username, password, asserts_in=None):
        """ Login user.

        Name:        "login",
        Method:      "GET",
        Pattern:     "login",

        Args:
            username: name of user that is going logged in
            password: password for username
            asserts_in: assert values for this call and this method
        """
        pattern = "login"
        request = requests.get(
            pytest.config.getini("USM_APIURL") + pattern)
        ApiUser.print_req_info(request)
        ApiUser.check_response(request, asserts_in)
        return {"username": username, "access_token": response.json()["access_token"]}

    def logout(self, asserts_in=None):
        """ Logout user.

        Name:        "logout",
        Method:      "DELETE",
        Pattern:     "logout",

        Args:
            asserts_in: assert values for this call and this method
        """
        pattern = "logout"
        request = requests.delete(
            pytest.config.getini("USM_APIURL") + pattern)
        ApiUser.print_req_info(request)
        ApiUser.check_response(request, asserts_in)
