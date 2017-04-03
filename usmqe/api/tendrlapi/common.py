"""Tendrl REST API common functions."""

import json
import time

import pytest
import requests

from usmqe.api.base import ApiBase

LOGGER = pytest.get_logger("commonapi", module=True)


class TendrlAuth(requests.auth.AuthBase):
    """
    Implementation of Tendrl Auth Method (Bearer Token) for requests
    library, based on upstream documentation:

    https://github.com/Tendrl/api/blob/master/docs/authentication.adoc

    This way, auth. implementation is stored in a single place and it also
    makes possible to omit auth object entrirely (thanks to design of
    requests library) for testing purposes (eg. checks of corner cases to make
    sure that security is not compromised) no matter if it makes sense from
    Tendrl user perspective.

    See also: http://docs.python-requests.org/en/master/user/authentication/
    """

    def __init__(self, token, username=None):
        self._bearer_token = token
        # metadata attributes for easier debugging, we need to trust login
        # function to store correct values there
        self.username = username

    def __call__(self, r):
        """Add Tendl Bearer Token into header of the request."""
        headers = {
            "Authorization": "Bearer {}".format(self._bearer_token),
            }
        r.prepare_headers(headers)
        return r


class TendrlApi(ApiBase):
    """ Common methods for Tendrl REST API.
    """

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
        post_data = {"username": username, "password": password}
        request = requests.post(
            pytest.config.getini("usm_api_url") + pattern,
            data=json.dumps(post_data))
        self.print_req_info(request)
        self.check_response(request, asserts_in)
        LOGGER.debug("access_token: {}".format(request.json()))
        token = request.json().get("access_token")
        auth = TendrlAuth(token, username)
        return auth

    def logout(self, asserts_in=None, auth=None):
        """ Logout user.

        Name:        "logout",
        Method:      "DELETE",
        Pattern:     "logout",

        Args:
            asserts_in: assert values for this call and this method
            auth: TendrlAuth object (defines bearer token header)
        """
        pattern = "logout"
        request = requests.delete(
            pytest.config.getini("usm_api_url") + pattern,
            auth=auth)
        self.print_req_info(request)
        self.check_response(request, asserts_in)

    def get_job_attribute(self, job_id, auth=None, attribute="status", section=None):
        """ Get attrubute from job specified by job_id.

        Name:       "get_job_attribute",
        Method:     "GET",
        Pattern     "jobs",

        Args:
            job_id:     id of job
            attribute:  attribute which value is looked for
            section:    section of response in which is attribute located
        """
        pattern = "jobs/{}".format(job_id)
        response = requests.get(
            pytest.config.getini("usm_api_url") + pattern,
            auth=auth,)
        self.print_req_info(response)
        self.check_response(response)
        if section:
            return response.json()[section][attribute]
        else:
            return response.json()[attribute]

    def wait_for_job_status(
            self,
            job_id,
            auth,
            max_count=30,
            status="finished",
            issue=None):
        """ Repeatedly check if status of job with provided id is in reqquired state.

        Args:
            job_id: id provided by api request
            max_count: maximum of iterations
            status: expected status of job that is checked
            issue: pytest issue message (usually github issue link)
        """

        count = 0
        current_status = ""
        while (current_status != status and count < max_count):
            current_status = self.get_job_attribute(
                job_id,
                auth=auth,
                attribute="status")
            count += 1
            time.sleep(1)
        LOGGER.debug("status: %s" % current_status)
        pytest.check(
            current_status == status,
            msg="Job status is {} and should be {}".format(current_status, status),
            issue=issue)
        return current_status

    def ping(self, auth, asserts_in=None):
        """ Ping REST API
        Name:        "ping",
        Method:      "GET",
        Pattern:     "ping",
        """
        pattern = "ping"
        response = requests.get(
            pytest.config.getini("usm_api_url") + pattern,
            auth=auth,)
        self.print_req_info(response)
        self.check_response(response, asserts_in)
        return response.json()
