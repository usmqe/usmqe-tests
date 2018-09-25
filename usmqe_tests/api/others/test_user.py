# -*- coding: utf8 -*-
"""
REST API test suite - user
"""

import json
import pytest
import copy
from usmqe.api.tendrlapi import user as tendrlapi_user
from usmqe.api.tendrlapi.common import login, logout


LOGGER = pytest.get_logger('user_test', module=True)
"""@pylatest default
Setup
=====

Prepare USM cluster accordingly to documentation.

Further mentioned ``APIURL`` points to: ``http://USMSERVER/api/1.0``.
"""

"""@pylatest default
Teardown
========
"""


@pytest.mark.happypath
@pytest.mark.testready
def test_user_get(valid_session_credentials, valid_new_normal_user):
    """@pylatest api/user.get
    API-users: get user
    *******************

    .. test_metadata:: author mkudlej@redhat.com dahorak@redhat.com fbalak@redhat.com

    Description
    ===========

    Get user from ``valid_new_normal_user`` fixture.
    """
    test = tendrlapi_user.ApiUser(auth=valid_session_credentials)
    """@pylatest api/user.get
    .. test_step:: 2

        Send **GET** request to ``APIURL/users``.

    .. test_result:: 2

        List of users in database is returned
    """
    test.get_users()
    """@pylatest api/user.get
    .. test_step:: 3

        Get user info.

        Send **GET** request to ``APIURL/users/{user}``.

    .. test_result:: 3

        User information for user from ``valid_new_normal_user`` fixture is returned.
    """
    test.check_user(valid_new_normal_user)


@pytest.mark.happypath
@pytest.mark.testready
def test_user_change_password(valid_new_normal_user, valid_password):
    """@pylatest api/user.edit
    API-users: edit user
    *******************

    .. test_metadata:: author fbalak@redhat.com

    Description
    ===========

    Change password and email of user and login with new password.
    """
    auth = login(
        valid_new_normal_user["username"],
        valid_new_normal_user["password"])
    test = tendrlapi_user.ApiUser(auth=auth)
    """@pylatest api/user.get
    .. test_step:: 1

        Send **PUT** request to ``APIURL/users``.

        During this step is set email to `testmail@example.com` because
        user can not be edited if he does not have set email. (e.g. admin)

    .. test_result:: 1

        Edited user data are returned.
    """
    new_email = "testmail@example.com"
    edit_data = {
        "email": new_email,
        "password": valid_password,
        "password_confirmation": valid_password}
    test.edit_user(valid_new_normal_user["username"], edit_data)
    """@pylatest api/user.get
    .. test_step:: 2

        Login

        Send **POST** request to ``APIURL/login``.

    .. test_result:: 2

        User is logged with new credentials.
    """
    logout(auth=auth)
    auth = login(valid_new_normal_user["username"], valid_password)
    test = tendrlapi_user.ApiUser(auth=auth)

    """@pylatest api/user.get
    .. test_step:: 3

        Check if user have edited email.

        Send **GET** request to ``APIURL/users/{user}``.

    .. test_result:: 3

        User information is checked if email was correctly changed.
    """
    valid_new_normal_user["email"] = new_email
    test.check_user(valid_new_normal_user)
    logout(auth=auth)


@pytest.mark.xfail
@pytest.mark.negative
def test_user_change_password_to_invalid(valid_new_normal_user, invalid_password):
    """@pylatest api/user.edit
    API-users: edit user
    *******************

    .. test_metadata:: author ebondare@redhat.com

    Description
    ===========

    Attempt to change password to invalid - either too long or too short.
    Checks on 8-symbol password and on an extremely long password fail due to bug
    https://bugzilla.redhat.com/show_bug.cgi?id=1610947
    """
    auth = login(
        valid_new_normal_user["username"],
        valid_new_normal_user["password"])
    test = tendrlapi_user.ApiUser(auth=auth)
    """@pylatest api/user.get
    .. test_step:: 1

        Send **PUT** request to ``APIURL/users``.

        During this step is set email to `testmail@example.com` because
        user can not be edited if he does not have set email. (e.g. admin)

    .. test_result:: 1

        Error 422 Unprocessable Entity is returned. The response includes words
        "is too long" or "is too short" depending on the invalid password length.
        This check might fail due to https://bugzilla.redhat.com/show_bug.cgi?id=1610947
    """
    new_email = "testmail@example.com"
    edit_data = {
        "email": new_email,
        "password": invalid_password,
        "password_confirmation": invalid_password}
    asserts = {
        "ok": False,
        "reason": 'Unprocessable Entity',
        "status": 422}

    response = test.edit_user(valid_new_normal_user["username"], edit_data, asserts_in=asserts)
    if len(invalid_password) > 10:
        pass_length_error = "is too long" in str(response)
    else:
        pass_length_error = "is too short" in str(response)
    pytest.check(pass_length_error, issue='https://bugzilla.redhat.com/show_bug.cgi?id=1610947')
    """@pylatest api/user.get
    .. test_step:: 2

        Check if the response to the request in test_step 1 returned the expected error.
        If it didn't, change the password back to original.

    .. test_result:: 2

        User password is the same as it was before test_step 1

    """
    if not pass_length_error:
        edit_back_data = {
            "email": new_email,
            "password": valid_new_normal_user["password"],
            "password_confirmation": valid_new_normal_user["password"]}
        test.edit_user(valid_new_normal_user["username"], edit_back_data)


@pytest.mark.xfail
@pytest.mark.negative
def test_add_user_invalid_password(valid_session_credentials,
                                   valid_normal_user_data, invalid_password):
    """@pylatest api/user.add_delete
    API-users: add and delete
    *************************

    .. test_metadata:: author ebondare@redhat.com

    Description
    ===========

    Attempt to add a user with invalid password
    """
    test = tendrlapi_user.ApiUser(auth=valid_session_credentials)
    """@pylatest
    .. test_step:: 1 api/user.add_delete

        Attempt to add user using an invalid password, either too long or too short.

        Send **POST** request to ``APIURL/users`` with data from fixture
        valid_normal_user_data with user password substituted with invalid password.

    .. test_result:: 1

        User should not be created.

        Return code should be 422.

        This check might fail due to https://bugzilla.redhat.com/show_bug.cgi?id=1610947
    """
    user_data_password_invalid = copy.deepcopy(valid_normal_user_data)
    user_data_password_invalid["password"] = invalid_password
    asserts = {
        "ok": False,
        "reason": 'Unprocessable Entity',
        "status": 422}
    test.add_user(user_data_password_invalid, asserts_in=asserts)

    """@pylatest api/user.get
    .. test_step:: 2

        Check that the user doesn't exist

    .. test_result:: 2

        User can not be found.

        Return code should be 404.

        This check might fail due to https://bugzilla.redhat.com/show_bug.cgi?id=1610947

    """
    asserts = {
        "ok": False,
        "reason": 'Not Found',
        "status": 404}
    not_found = test.get_user(user_data_password_invalid["username"], asserts_in=asserts)

    """@pylatest api/user.add_delete
    .. test_step:: 3

        If the user was found, the user is deleted

    .. test_result:: 3

        If a new user was created during step 1 the user is deleted.

    """
    if "Not found" not in str(not_found):
        test.del_user(user_data_password_invalid["username"])


@pytest.mark.negative
def test_add_user_invalid_username(valid_session_credentials,
                                   valid_normal_user_data, invalid_username):
    """@pylatest api/user.add_delete
    API-users: add and delete
    *************************

    .. test_metadata:: author ebondare@redhat.com

    Description
    ===========

    Attempt to add a user with invalid username
    """
    test = tendrlapi_user.ApiUser(auth=valid_session_credentials)
    """@pylatest
    .. test_step:: 1 api/user.add_delete

        Attempt to add user using an invalid username, either too long or too short.

        Send **POST** request to ``APIURL/users`` with data from fixture
        valid_normal_user_data with valid username substituted with an invalid one

    .. test_result:: 1

        User should not be created.

        Return code should be 422.

        This check might fail due to https://bugzilla.redhat.com/show_bug.cgi?id=1610947
    """
    user_data_username_invalid = copy.deepcopy(valid_normal_user_data)
    user_data_username_invalid["username"] = invalid_username
    asserts = {
        "ok": False,
        "reason": 'Unprocessable Entity',
        "status": 422}
    test.add_user(user_data_username_invalid, asserts_in=asserts)

    """@pylatest api/user.get
    .. test_step:: 2

        Check that the user doesn't exist

    .. test_result:: 2

        User can not be found.

        Return code should be 404.

        This check might fail due to https://bugzilla.redhat.com/show_bug.cgi?id=1610947

    """
    asserts = {
        "ok": False,
        "reason": 'Not Found',
        "status": 404}
    not_found = test.get_user(user_data_username_invalid["username"], asserts_in=asserts)

    """@pylatest api/user.add_delete
    .. test_step:: 3

        If the user was found, the user is deleted

    .. test_result:: 3

        If a new user was created during step 1 the user is deleted.

    """
    if "Not found" not in str(not_found):
        test.del_user(user_data_username_invalid["username"])


@pytest.mark.negative
def test_delete_admin(valid_session_credentials):
    """@pylatest api/user.add_delete
    API-users: add and delete
    *************************

    .. test_metadata:: author ebondare@redhat.com

    Description
    ===========

    Attempt to delete the admin user
    """
    test = tendrlapi_user.ApiUser(auth=valid_session_credentials)

    """@pylatest api/user.add_delete
    .. test_step:: 1

        Attempt to delete the admin user

    .. test_result:: 1

        Admin user is not deleted.

    """
    asserts = {
         "ok": False,
         "reason": 'Forbidden',
         "status": 403}

    test.del_user("admin", asserts_in=asserts)

    """@pylatest api/user.get
     .. test_step:: 2

         Check if user admin still exists

     .. test_result:: 2

         User admin still exists.

    """
    pytest.check(test.get_user("admin")["name"] == "Admin")


@pytest.mark.happypath
@pytest.mark.testready
def test_user_add_del(valid_session_credentials, valid_normal_user_data):
    """@pylatest api/user.add_delete
    API-users: add and delete
    *************************

    .. test_metadata:: author mkudlej@redhat.com dahorak@redhat.com fbalak@redhat.com

    Description
    ===========

    Add and remove *test* user.
    """
    test = tendrlapi_user.ApiUser(auth=valid_session_credentials)
    """@pylatest api/user.add_delete
    .. test_step:: 2

        Add user test2.

        Send **PUT** request to ``APIURL/users/test2`` with data from fixture
        valid_normal_user_data where are specified keys: email, username, name, role

    .. test_result:: 2

        User should be created.

        Return code should be 201.
    """
    # add test user

    added_user = test.add_user(valid_normal_user_data)
    """@pylatest api/user.add_delete
    .. test_step:: 3
       :include: api/user.get:2

    .. test_result:: 3
       :include: api/user.get:2
    """
    test.check_user(added_user)
    """@pylatest api/user.add_delete
    .. test_step:: 4

        Delete user test2.

        Send **DELETE** request to ``APIURL/users/test2``.

    .. test_result:: 4

        User test2 should be deleted.

        Return code should be 200.
    """
    test.del_user(valid_normal_user_data["username"])
    """@pylatest api/user.add_delete
    .. test_step:: 5
       :include: api/user.get:2

    .. test_result:: 5

        User test2 is not available.

        Return code should be 404.
    """
    asserts = {
        "json": json.loads('{"Error": "Not found"}'),
        "cookies": None,
        "ok": False,
        "reason": 'Not Found',
        "status": 404}
    test.get_user(valid_normal_user_data["username"], asserts_in=asserts)
    """@pylatest api/user.add_delete
    .. test_step:: 6
       :include: api/user.logout:3

    .. test_result:: 6
       :include: api/user.logout:3
    """


@pytest.mark.xfail
def test_user_change_username_and_email(valid_session_credentials, valid_new_normal_user):
    """@pylatest api/user.add_delete
    API-users: add and delete
    *************************

    .. test_metadata:: author ebondare@redhat.com

    Description
    ===========

    Change user's username and e-mail. New user shouldn't be created.
    https://bugzilla.redhat.com/show_bug.cgi?id=1610660
    """
    test = tendrlapi_user.ApiUser(auth=valid_session_credentials)
    original_users_number = len(test.get_users())
    """@pylatest api/user.get
    .. test_step:: 1

        Update a user's username and e-mail.

    .. test_result:: 1

        User's username and e-mail are updated.
    """
    new_email = "testmail@example.com"
    new_username = "newusername"
    edit_data = {
        "email": new_email,
        "username": new_username}
    test.edit_user(valid_new_normal_user["username"], edit_data)
    """@pylatest api/user.get
    .. test_step:: 2

        Check if the number of users changed as a result of updating a user.
        Change all the users to their original state.

    .. test_result:: 2

        Fail if the number of users changed as a result of updating a user.
        All the users are changed back to their original state.

    """
    if len(test.get_users()) == original_users_number:
        edit_back_data = {
            "email": valid_new_normal_user["email"],
            "username": valid_new_normal_user["username"]}
        test.edit_user(new_username, edit_back_data)
    else:
        test.del_user(new_username)
        pytest.check(False,
                     issue='https://bugzilla.redhat.com/show_bug.cgi?id=1610660')
