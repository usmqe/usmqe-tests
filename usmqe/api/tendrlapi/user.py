"""
tendrl REST API.
"""

import json
import requests
import pytest
from usmqe.api.tendrlapi.common import TendrlApi

LOGGER = pytest.get_logger("tendrlapi.user", module=True)
USERDATA_KEYS = ('email', 'name', 'role', 'username')

class ApiUser(TendrlApi):
    """ Main class for interact with REST API - user.
    """
    def get_users(self, asserts_in=None):
        """ Get users.

        Name:        "GET_users",
        Method:      "GET",
        Pattern:     "users",

        Args:
            asserts_in: assert values for this call and this method
        """
        pattern = "users"
        request = requests.get(
            pytest.config.getini("usm_api_url") + pattern,
            auth=self._auth)
        self.print_req_info(request)
        self.check_response(request, asserts_in)
        if not request.ok:
            return False

        msg = "User {0} should contain: {1}\n\tUser {0} contains: {2}"
        for item in request.json(encoding='unicode'):
            user = item["username"]
            pytest.check(
                item.keys() == USERDATA_KEYS,
                msg.format(user, USERDATA_KEYS, item.keys))
        return request.json(encoding='unicode')

    def edit_user(self, username, data, asserts_in=None):
        """ Edit a single user

        Args:
            username: name of user that is going to be updated
            data: dictionary data about user
                  have to contain: email, username, name, role
            asserts_in: assert values for this call and this method
        """
        pattern = "users/{}".format(username)
        request = requests.put(
            pytest.config.getini("usm_api_url") + pattern,
            json.dumps(data),
            auth=self._auth)
        self.print_req_info(request)
        self.check_response(request, asserts_in)
        return request.json(encoding='unicode')

    def add_user(self, user_in, asserts_in=None):
        """ Add user throught **users**.

        Name:        "POST_users",
        Method:      "POST",
        Pattern:     "users",

        Args:
            user_in: dictionary info about user
                     have to contain: name, username, email, role, password, password_confirmation
            asserts_in: assert values for this call and this method
        """
        asserts_in = asserts_in or {
            "cookies": None,
            "ok": True,
            "reason": 'Created',
            "status": 201}

        pattern = "users"
        request = requests.post(
            pytest.config.getini("usm_api_url") + pattern,
            data=json.dumps(user_in),
            auth=self._auth)
        self.print_req_info(request)
        self.check_response(request, asserts_in)
        sent_user = {k: user_in[k] for k in USERDATA_KEYS}
        stored_user = self.get_user(user_in["username"])
        pytest.check(
            sent_user == stored_user,
            """Information sent: {}, information stored in database: {},
            These should match""".format(sent_user, stored_user))
        return stored_user

    def get_user(self, username, asserts_in=None):
        """ Get user info..

        Name:        "GET_user",
        Method:      "GET",
        Pattern:     "users/{username}",

        Args:
            username: name of user stored in database
            asserts_in: assert values for this call and this method
        """
        pattern = "users/{}".format(username)
        request = requests.get(
            pytest.config.getini("usm_api_url") + pattern,
            auth=self._auth)
        self.print_req_info(request)
        self.check_response(request, asserts_in)

        return request.json(encoding='unicode')

    def check_user(self, user_data, asserts_in=None):
        """ Check if there is stored user with given attributes.

        Args:
            user_data: user data that are going to be checked
            asserts_in: assert values for this call and this method
        """
        stored_data = self.get_user(user_data["username"], asserts_in=asserts_in)
        sent_data = {k: user_data[k] for k in USERDATA_KEYS}
        msg = "Json of stored user: {0}\n\tAnd of checked one: {1}\n\tShould be equal."
        pytest.check(
            stored_data == sent_data,
            msg.format(stored_data, sent_data))

    def del_user(self, username, asserts_in=None):
        """ Delete user.

        Name:        "DELETE_users",
        Method:      "DELETE",
        Pattern:     "users/{username}",

        Args:
            username: name of user that is going to be deleted
            asserts_in: assert values for this call and this method
        """
        pattern = "users/{}".format(username)
        request = requests.delete(
            pytest.config.getini("usm_api_url") + pattern,
            auth=self._auth)
        self.print_req_info(request)
        self.check_response(request, asserts_in)
