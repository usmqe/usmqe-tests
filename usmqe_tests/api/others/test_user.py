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
"""
Setup
=====

Prepare USM cluster accordingly to documentation.

Further mentioned ``APIURL`` points to: ``http://USMSERVER/api/1.0``.
"""


@pytest.mark.author("mkudlej@redhat.com")
@pytest.mark.author("dahorak@redhat.com")
@pytest.mark.author("fbalak@redhat.com")
@pytest.mark.happypath
@pytest.mark.testready
def test_user_get(valid_session_credentials, valid_new_normal_user):
    """
    Get user from ``valid_new_normal_user`` fixture.
    """
    test = tendrlapi_user.ApiUser(auth=valid_session_credentials)
    """
    :step:
      Send **GET** request to ``APIURL/users``.
    :result:
      List of users in database is returned
    """
    test.get_users()
    """
    :step:
      Get user info.
      Send **GET** request to ``APIURL/users/{user}``.
    :result:
      User information for user from ``valid_new_normal_user`` fixture is returned.
    """
    test.check_user(valid_new_normal_user)


@pytest.mark.author("fbalak@redhat.com")
@pytest.mark.happypath
@pytest.mark.testready
def test_user_change_password(valid_new_normal_user, valid_password):
    """
    Change password and email of user and login with new password.
    """
    auth = login(
        valid_new_normal_user["username"],
        valid_new_normal_user["password"])
    test = tendrlapi_user.ApiUser(auth=auth)
    """
    :step:
      Send **PUT** request to ``APIURL/users``.
      During this step is set email to `testmail@example.com` because
      user can not be edited if he does not have set email. (e.g. admin)
    :result:
       Edited user data are returned.
    """
    new_email = "testmail@example.com"
    edit_data = {
        "email": new_email,
        "password": valid_password,
        "password_confirmation": valid_password}
    test.edit_user(valid_new_normal_user["username"], edit_data)
    """
    :step:
      Login
      Send **POST** request to ``APIURL/login``.
    :result:
      User is logged with new credentials.
    """
    logout(auth=auth)
    auth = login(valid_new_normal_user["username"], valid_password)
    test = tendrlapi_user.ApiUser(auth=auth)

    """
    :step:
      Check if user have edited email.
      Send **GET** request to ``APIURL/users/{user}``.
    :result:
      User information is checked if email was correctly changed.
    """
    valid_new_normal_user["email"] = new_email
    test.check_user(valid_new_normal_user)
    logout(auth=auth)


@pytest.mark.author("ebondare@redhat.com")
@pytest.mark.negative
@pytest.mark.testready
def test_user_change_password_to_invalid(valid_new_normal_user, invalid_password):
    """
    Attempt to change password to invalid - either too long or too short.
    Checks on 8-symbol password and on an extremely long password fail due to bug
    https://bugzilla.redhat.com/show_bug.cgi?id=1610947
    """
    auth = login(
        valid_new_normal_user["username"],
        valid_new_normal_user["password"])
    test = tendrlapi_user.ApiUser(auth=auth)
    """
    :step:
      Send **PUT** request to ``APIURL/users``.
      During this step is set email to `testmail@example.com` because
      user can not be edited if he does not have set email. (e.g. admin)
    :result:
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
    """
    :step:
      Check if the response to the request in test_step 1 returned the expected error.
      If it didn't, change the password back to original.
    :result:
      User password is the same as it was before test_step 1

    """
    if not pass_length_error:
        edit_back_data = {
            "email": new_email,
            "password": valid_new_normal_user["password"],
            "password_confirmation": valid_new_normal_user["password"]}
        test.edit_user(valid_new_normal_user["username"], edit_back_data)


@pytest.mark.author("ebondare@redhat.com")
@pytest.mark.negative
@pytest.mark.testready
def test_add_user_invalid_password(valid_session_credentials,
                                   valid_normal_user_data, invalid_password):
    """
    Attempt to add a user with invalid password
    """
    test = tendrlapi_user.ApiUser(auth=valid_session_credentials)
    """
    :step:
      Attempt to add user using an invalid password, either too long or too short.
      Send **POST** request to ``APIURL/users`` with data from fixture
      valid_normal_user_data with user password substituted with invalid password.
    :result:
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

    """
    :step:
      Check that the user doesn't exist
    :result:
      User can not be found.
      Return code should be 404.
      This check might fail due to https://bugzilla.redhat.com/show_bug.cgi?id=1610947

    """
    asserts = {
        "ok": False,
        "reason": 'Not Found',
        "status": 404}
    not_found = test.get_user(user_data_password_invalid["username"], asserts_in=asserts)

    """
    :step:
      If the user was found, the user is deleted
    :result:
      If a new user was created during step 1 the user is deleted.
    """
    if "Not found" not in str(not_found):
        test.del_user(user_data_password_invalid["username"])


@pytest.mark.author("ebondare@redhat.com")
@pytest.mark.negative
@pytest.mark.testready
def test_add_user_invalid_username(valid_session_credentials,
                                   valid_normal_user_data, invalid_username):
    """
    Attempt to add a user with invalid username
    """
    test = tendrlapi_user.ApiUser(auth=valid_session_credentials)
    """
    :step:
      Attempt to add user using an invalid username, either too long or too short.
      Send **POST** request to ``APIURL/users`` with data from fixture
      valid_normal_user_data with valid username substituted with an invalid one
    :result:
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

    """
    :step:
      Check that the user doesn't exist
    :result:
      User can not be found.
      Return code should be 404.
      This check might fail due to https://bugzilla.redhat.com/show_bug.cgi?id=1610947
    """
    asserts = {
        "ok": False,
        "reason": 'Not Found',
        "status": 404}
    not_found = test.get_user(user_data_username_invalid["username"], asserts_in=asserts)

    """
    :step:
      If the user was found, the user is deleted
    :result:
      If a new user was created during step 1 the user is deleted.
    """
    if "Not found" not in str(not_found):
        test.del_user(user_data_username_invalid["username"])


@pytest.mark.author("ebondare@redhat.com")
@pytest.mark.negative
@pytest.mark.testready
def test_delete_admin(valid_session_credentials):
    """
    Attempt to delete the admin user
    """
    test = tendrlapi_user.ApiUser(auth=valid_session_credentials)

    """
    :step:
      Attempt to delete the admin user
    :result:
      Admin user is not deleted.
    """
    asserts = {
         "ok": False,
         "reason": 'Forbidden',
         "status": 403}

    test.del_user("admin", asserts_in=asserts)

    """
    :step:
      Check if user admin still exists
    :result:
      User admin still exists.
    """
    pytest.check(test.get_user("admin")["name"] == "Admin")


@pytest.mark.author("mkudlej@redhat.com")
@pytest.mark.author("dahorak@redhat.com")
@pytest.mark.author("fbalak@redhat.com")
@pytest.mark.happypath
@pytest.mark.testready
def test_user_add_del(
        valid_session_credentials,
        valid_normal_user_data,
        valid_username,
        valid_password):
    """
    Add and remove *test* user.
    """
    valid_normal_user_data["username"] = valid_username
    valid_normal_user_data["password"] = valid_password
    test = tendrlapi_user.ApiUser(auth=valid_session_credentials)
    """
    :step:
      Add user test2.
      Send **PUT** request to ``APIURL/users/test2`` with data from fixture
      valid_normal_user_data where are specified keys: email, username, name, role
    :result:
      User should be created.
      Return code should be 201.
    """
    # add test user

    added_user = test.add_user(valid_normal_user_data)
    """
    :step:
      :include: api/user.get:2
    :result:
      :include: api/user.get:2
    """
    test.check_user(added_user)
    """
    :step:
      Delete user test2.
      Send **DELETE** request to ``APIURL/users/test2``.
    :result:
      User test2 should be deleted.
      Return code should be 200.
    """
    test.del_user(valid_normal_user_data["username"])
    """
    :step:
      :include: api/user.get:2
    :result:
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
    """
    :step:
      :include: api/user.logout:3
    :result:
      :include: api/user.logout:3
    """


@pytest.mark.author("ebondare@redhat.com")
@pytest.mark.negative
@pytest.mark.testready
def test_change_username_and_email(valid_session_credentials, valid_new_normal_user):
    """
    Try to change user's username and e-mail. It is not allowed.
    Tests reproducer from BZ 1610660
    https://bugzilla.redhat.com/show_bug.cgi?id=1610660
    """
    test = tendrlapi_user.ApiUser(auth=valid_session_credentials)
    """
    :step:
      Try to update a user's username and e-mail.
    :result:
      User's username and e-mail are not changed.
      Return code should be 422.
    """
    new_email = "testmail@example.com"
    new_username = "newusername"
    edit_data = {
        "email": new_email,
        "username": new_username}
    asserts = {
         "ok": False,
         "reason": 'Unprocessable Entity',
         "status": 422}

    test.edit_user(valid_new_normal_user["username"], edit_data, asserts_in=asserts)

    """
    :step:
      Check there's no user with the new username
    :result:
      User with the new username is not available.
      Return code should be 404.
    """
    asserts = {
         "json": json.loads('{"Error": "Not found"}'),
         "cookies": None,
         "ok": False,
         "reason": 'Not Found',
         "status": 404}
    test.get_user(edit_data["username"], asserts_in=asserts)
