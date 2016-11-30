"""
SkyRing REST API.
"""

import json

import requests
import pytest

from usmqe.api.skyringapi import skyringapi

LOGGER = pytest.get_logger("skyringapi.user", module=True)


class ApiUser(skyringapi.ApiCommon):
    """ Main class for interact with REST API - user.
    """
    def users(self, asserts_in=None):
        """ Get users.

        Name:        "GET_users",
        Method:      "GET",
        Pattern:     "users",

        Args:
            asserts_in: assert values for this call and this method
        """
        asserts = ApiUser.default_asserts.copy()
        asserts.update({
            "users": ["admin"],
            })
        if asserts_in:
            asserts.update(asserts_in)
        req = requests.get(pytest.config.getini("usm_api_url") + "users/",
                           cookies=self.cookies, verify=self.verify)
        ApiUser.print_req_info(req)
        ApiUser.check_response(req, asserts)
        json_v = {}
        for user in asserts["users"]:
            temp = ApiUser.user_info.copy()
            temp["username"] %= user
            temp["email"] %= user
            json_v[user] = temp
        if req.ok:
            for item in req.json(encoding='unicode'):
                user = item["username"]
                pytest.check(
                    all(key in item and json_v[user][key] == item[key]
                        for key in json_v[user].keys()),
                    "User {0} should contain: {1}\n\tUser {0} contains: {2}".
                    format(user, json_v[user], item))
            return req.json(encoding='unicode')

    def users_replace(self, users, asserts_in=None):
        """ Replace all users by another list of users.

        It uses **PUT** method.
        FIXME: is this still valid?

        Args:
            users: new user list
            asserts_in: assert values for this call and this method
        """
        asserts = ApiUser.default_asserts.copy()
        if asserts_in:
            asserts.update(asserts_in)
        data = []
        for usr in users:
            data.append(ApiUser.user_info.copy())
            data[-1]["username"] %= usr
            data[-1]["email"] %= usr
            data[-1]["password"] = usr
        data = json.dumps(data)
        req = requests.put(pytest.config.getini("usm_api_url") + "users",
                           data, cookies=self.cookies, verify=self.verify)
        ApiUser.print_req_info(req)
        ApiUser.check_response(req, asserts)
# TODO check json comparision
        return req.json(encoding='unicode')

    def users_add(self, user_in, asserts_in=None):
        """ Add user throught **users**.

        Name:        "POST_users",
        Method:      "POST",
        Pattern:     "users",

        Args:
            user_in: new user name or user info
            asserts_in: assert values for this call and this method

        Returns:
            Function returns known issue if there is any.
        """
        asserts = ApiUser.default_asserts.copy()
        if asserts_in:
            asserts.update(asserts_in)
        data = None
        if isinstance(user_in, str):
            data = ApiUser.user_info.copy()
            data["username"] %= user_in
            data["email"] %= user_in
            data["password"] = user_in
        elif isinstance(user_in, dict):
            data = user_in
        issue = None
        if data:
            data = json.dumps(data)
            req = requests.post(pytest.config.getini("usm_api_url") + "users",
                                data, cookies=self.cookies, verify=self.verify)
            ApiUser.print_req_info(req)
            if req.status_code == 500 and \
               req.text == '{"Error":"no email given"}':
                issue = "https://bugzilla.redhat.com/show_bug.cgi?id=1311920"
                ApiUser.check_response(req, asserts, issue=issue)
            else:
                ApiUser.check_response(req, asserts)
        else:
            pytest.check(
                0, "No valid input data for creating user.", hard=True)
        return issue

    def user(self, user_in, asserts_in=None):
        """ Get user info..

        Name:        "GET_user",
        Method:      "GET",
        Pattern:     "users/{username}",

        Args:
            user_in: user name
            asserts_in: assert values for this call and this method
        """
        asserts = ApiUser.default_asserts.copy()
        if asserts_in:
            asserts.update(asserts_in)
        req = requests.get(
            pytest.config.getini("usm_api_url") + "users/%s" % user_in,
            cookies=self.cookies, verify=self.verify)
        ApiUser.print_req_info(req)
        ApiUser.check_response(req, asserts)
        if "json" not in asserts:
            asserts["json"] = ApiUser.user_info.copy()
            asserts["json"]["email"] %= user_in
            asserts["json"]["username"] %= user_in
        real_vals = req.json(encoding='unicode')
        pytest.check(
            all(key in real_vals and asserts["json"][key] == real_vals[key]
                for key in asserts["json"].keys()),
            "Json of added user should contain: {0}\n\tIt contains: {1}".
            format(asserts["json"], real_vals))
        return req.json(encoding='unicode')

    def user_add(self, user_in, asserts_in=None):
        """ Add user.

        Name:        "PUT_users",
        Method:      "PUT",
        Pattern:     "users/{username}",

        Args:
            user_in: new user name
            asserts_in: assert values for this call and this method
        """
        asserts = ApiUser.default_asserts.copy()
        if asserts_in:
            asserts.update(asserts_in)
        data = None
        if isinstance(user_in, str):
            data = ApiUser.user_info.copy()
            data["email"] %= user_in
            data["username"] %= user_in
            data["password"] = user_in
        elif isinstance(user_in, dict):
            data = user_in
        req = requests.put(
            pytest.config.getini("usm_api_url") + "users/%s" % data["username"],
            json.dumps(data), cookies=self.cookies, verify=self.verify)
        ApiUser.print_req_info(req)
        ApiUser.check_response(req, asserts)
        return req.json(encoding='unicode') if req.text else None

    def user_del(self, user_in, asserts_in=None):
        """ Delete user.

        Name:        "DELETE_users",
        Method:      "DELETE",
        Pattern:     "users/{username}",

        Args:
            user_in: new user name
            asserts_in: assert values for this call and this method
        """
        asserts = ApiUser.default_asserts.copy()
        if asserts_in:
            asserts.update(asserts_in)
        req = requests.delete(
            pytest.config.getini("usm_api_url") + "users/%s" % user_in,
            cookies=self.cookies, verify=self.verify)
        ApiUser.print_req_info(req)
        ApiUser.check_response(req, asserts)
