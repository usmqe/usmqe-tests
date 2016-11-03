# vim: set colorcolumn=120:

""" REST API test suite - user

"""
import pytest

import json

from usmqe.api.skyringapi import user as skyringapi_user


"""@pylatest default
Setup
=====

Prepare USM cluster accordingly to documentation.

Further mentioned ``APIURL`` points to: ``http://USMSERVER:8080/api/v1``.
"""

"""@pylatest default
Teardown
========
"""


class TestApiUsers():
    """
    Api - User tests
    """

    """@pylatest api/user.login_valid
    API-users: valid login
    **********************

    .. test_metadata:: author mkudlej@redhat.com dahorak@redhat.com

    Description
    ===========
    """
    # @pytest.mark.xfail(reason='proste proto')
    def test_login_valid(self):
        """@usmid api/user.login_valid
        Positive login test.
        """
        test = skyringapi_user.ApiUser()
        """@pylatest api/user.login_valid
        .. test_step:: 1

            Login to USM API via POST request to ``APIURL/auth/login`` with data::

                {'username': 'admin', 'password': 'admin'}

            Where 'admin' is valid username/password.

        .. test_result:: 1

            User should log into USM API.

            Return code should be **200** with data ``{"message": "Logged in"}``.
            It should return session cookie.
        """
        test.login(pytest.config.getini("USM_USERNAME"), pytest.config.getini("USM_PASSWORD"))
        test.logout()

    """@pylatest api/user.login_invalid
    API-users: invalid login
    ************************

    .. test_metadata:: author mkudlej@redhat.com dahorak@redhat.com
    """
    def test_login_invalid(self):
        """@usmid api/user.login_invalid
        Negative login test.
        """
        """@pylatest api/user.login_invalid
        .. test_step:: 1

            Try to login to USM API via POST request to ``APIURL/auth/login`` with
            data::

                {'username': 'admin', 'password': 'wrong'}

            Where 'admin'/'wrong' are invalid usernames or passwords.

        .. test_result:: 1

            User should not be log into USM API.

            Return code should be **401 - Unauthorized** with data::

                {"Error": "password doesn\'t match"}
        """
        test = skyringapi_user.ApiUser()
        # TODO: add more cases - wrong name, password, empty field...
        test.login('admin', 'wrong',
                   {
                       "cookies": None,
                       "json": json.loads('{"Error": "password doesn\'t match"}'),
                       "ok": False,
                       "reason": 'Unauthorized',
                       "status": 401,
                   })

    """@pylatest api/user.logout
    API-users: logout
    *****************

    .. test_metadata:: author mkudlej@redhat.com dahorak@redhat.com
    """
    def test_logout(self):
        """@usmid api/user.logout
        Logout test.
        """
        test = skyringapi_user.ApiUser()
        """@pylatest api/user.logout
        .. test_step:: 1
           :include: api/user.login_valid:1

        .. test_result:: 1
           :include: api/user.login_valid:1
        """
        test.login(pytest.config.getini("USM_USERNAME"), pytest.config.getini("USM_PASSWORD"))
        """@pylatest api/user.logout
        .. test_step:: 2

            FIXME: Get list of users.

        .. test_result:: 2

            FIXME: Get list of users.
        """
        test.users()
        """@pylatest api/user.logout
        .. test_step:: 3

            Logout user from USM API via ``APIURL/auth/logout``.

        .. test_result:: 3

            User should be logged out from USM API.

            Return code should be **200** with data ``{"message": "Logged out"}``.
        """
        test.logout()
        """@pylatest api/user.logout
        .. test_step:: 4

            FIXME: Get list of users.

        .. test_result:: 4

            "Error code **401** with data ``{"Error": "Unauthorized"}`` is returned.
        """
        test.users(asserts_in={
            "cookies": None,
            "json": json.loads('{"Error": "Unauthorized"}'),
            "ok": False,
            "reason": 'Unauthorized',
            "status": 401})

    """@pylatest api/user.get
    API-users: get user
    *******************

    .. test_metadata:: author mkudlej@redhat.com dahorak@redhat.com
    """
    def test_user_get(self):
        """@usmid api/user.get
        Get user admin.
        """
        test = skyringapi_user.ApiUser()
        """@pylatest api/user.get
        .. test_step:: 1
           :include: api/user.login_valid:1

        .. test_result:: 1
           :include: api/user.login_valid:1
        """
        test.login(pytest.config.getini("USM_USERNAME"), pytest.config.getini("USM_PASSWORD"))
        """@pylatest api/user.get
        .. test_step:: 2

            Get user info.

            Send **GET** request to ``APIURL/users/admin``.

        .. test_result:: 2

            User information for user *admin* is returned.
        """
        test.user('admin')
        test.logout()

    """@pylatest api/user.get_nonexistent
    API-users: get nonexistent user
    *******************************

    .. test_metadata:: author dahorak@redhat.com
    """
    def test_user_get_not_found(self):
        """@usmid api/user.get_nonexistent
        Get users.
        """
        test = skyringapi_user.ApiUser()
        """@pylatest api/user.get_nonexistent
        .. test_step:: 1
           :include: api/user.login_valid:1

        .. test_result:: 1
           :include: api/user.login_valid:1
        """
        test.login(pytest.config.getini("USM_USERNAME"), pytest.config.getini("USM_PASSWORD"))

        """@pylatest api/user.get_nonexistent
        .. test_step:: 2

            Try to get information for non existent user.

            For each user, send GET request to ``APIURL/user/USER``

        .. test_result:: 2

            It should return error about unknown user.
        """
        users = (
            'aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee',
            '11111111-2222-3333-4444-555555555555',
            'abcdef01-2345-6789-abcd-ef1234567890')

        for user in users:
            test.user(user, asserts_in={
                "json": json.loads('{"Error": "can\'t find user"}'),
                "cookies": None,
                "ok": False,
                "reason": 'Not Found',
                "status": 404})

        test.logout()

    """@pylatest api/user.add_delete
    API-users: add and delete
    *************************

    .. test_metadata:: author mkudlej@redhat.com dahorak@redhat.com
    """
    def test_user_add_del(self):
        """@usmid api/user.add_delete
        Add and remove *test* user.
        """
        test = skyringapi_user.ApiUser()
        """@pylatest api/user.add_delete
        .. test_step:: 1
           :include: api/user.login_valid:1

        .. test_result:: 1
           :include: api/user.login_valid:1
        """
        test.login(pytest.config.getini("USM_USERNAME"), pytest.config.getini("USM_PASSWORD"))
        """@pylatest api/user.add_delete
        .. test_step:: 2

            Add user test2.

            Send **PUT** request to ``APIURL/users/test2`` with data::

                {
                  "username":"test2",
                  "email":"test2@localhost",
                  "role":"admin",
                  "groups":[]
                }

        .. test_result:: 2

            User should be created.

            Return code should be (FIXME: 201, 202)**???** (current 200).
        """
        # add test user
        test.users_add('test2')
        """@pylatest api/user.add_delete
        .. test_step:: 3
           :include: api/user.get:2

        .. test_result:: 3
           :include: api/user.get:2
        """
        test.user('test2')
        """@pylatest api/user.add_delete
        .. test_step:: 4

            Delete user test2.

            Send **DELETE** request to ``APIURL/users/test2``.

        .. test_result:: 4

            User test2 should be deleted.

            Return code should be (FIXME: 201, 202)**???** (current 200).
        """
        test.user_del('test2')
        """@pylatest api/user.add_delete
        .. test_step:: 5
           :include: api/user.get:2

        .. test_result:: 5

            User test2 is not available.

            Return code should be (FIXME: 4xx)**???** (current 500) with data::

                {"Error": "can't find user"}
        """
        test.user('test2', {
            "cookies": None,
            "json": json.loads('{"Error": "can\'t find user"}'),
            "ok": False,
            "reason": 'Not Found',
            "status": 404,
            })
        """@pylatest api/user.add_delete
        .. test_step:: 6
           :include: api/user.logout:3

        .. test_result:: 6
           :include: api/user.logout:3
        """
        test.logout()
