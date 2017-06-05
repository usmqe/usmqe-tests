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
        """
        Args:
            token (str): tendrl ``access_token`` string
            username (str): username of account associated with the token
        """
        self.__bearer_token = token
        # metadata attributes for easier debugging, we need to trust login
        # function to store correct values there
        self.username = username

    def __repr__(self):
        return "TendrlAuth(token={})".format(self.__bearer_token)

    def __call__(self, r):
        """
        Add Tendl Bearer Token into header of the request.

        For full description, see requests documentation:
        http://docs.python-requests.org/en/master/user/authentication/
        """
        headers = {
            "Authorization": "Bearer {}".format(self.__bearer_token),
            }
        r.prepare_headers(headers)
        return r


def login(username, password, asserts_in=None):
    """
    Login Tendrl user.

    Args:
        username: name of user that is going logged in
        password: password for username
        asserts_in: assert values for this call and this method

    Returns requests auth object (instance of TendrlAuth)
    """
    pattern = "login"
    post_data = {"username": username, "password": password}
    request = requests.post(
        pytest.config.getini("usm_api_url") + pattern,
        data=json.dumps(post_data))
    ApiBase.print_req_info(request)
    ApiBase.check_response(request, asserts_in)
    token = request.json().get("access_token")
    LOGGER.info("access_token: {}".format(token))
    auth = TendrlAuth(token, username)
    return auth


def logout(auth, asserts_in=None):
    """
    Logout Tendrl user.

    Args:
        asserts_in: assert values for this call and this method
        auth: TendrlAuth object (defines bearer token header)
    """
    pattern = "logout"
    request = requests.delete(
        pytest.config.getini("usm_api_url") + pattern,
        auth=auth)
    ApiBase.print_req_info(request)
    ApiBase.check_response(request, asserts_in)


class TendrlApi(ApiBase):
    """ Common methods for Tendrl REST API.
    """

    def __init__(self, auth=None):
        """
        Args:
            auth: TendrlAuth object (defines bearer token header), when auth is
               None, requests are send without athentication header
        """
        # requests auth object with so called tendrl bearer token
        self._auth = auth

    def get_job_attribute(self, job_id, attribute="status", section=None):
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
            auth=self._auth,)
        self.print_req_info(response)
        self.check_response(response)
        if section:
            return response.json()[section][attribute]
        else:
            return response.json()[attribute]

    def wait_for_job_status(
            self,
            job_id,
            max_count=100,
            status="finished",
            issue=None,
            sleep_time=10):
        """ Repeatedly check if status of job with provided id is in required state.

        Args:
            job_id: id provided by api request
            max_count: maximum of iterations
            status: expected status of job that is checked
            issue: pytest issue message (usually github issue link)
            sleep_time: time in seconds between 2 job status function calls
        """

        count = 0
        current_status = ""
        while current_status not in (status, "finished", "failed") and\
                count < max_count:
            current_status = self.get_job_attribute(
                job_id,
                attribute="status")
            count += 1
            time.sleep(sleep_time)
        LOGGER.debug("status: %s" % current_status)
        pytest.check(
            current_status == status,
            msg="Job status is {} and should be {}".format(
                current_status,
                status),
            issue=issue)
        return current_status

    def ping(self, asserts_in=None):
        """ Ping REST API
        Name:        "ping",
        Method:      "GET",
        Pattern:     "ping",
        """
        pattern = "ping"
        response = requests.get(
            pytest.config.getini("usm_api_url") + pattern,
            auth=self._auth,)
        self.print_req_info(response)
        self.check_response(response, asserts_in)
        return response.json()

    def flows(self, asserts_in=None):
        """
        Provides list of flows which can be performed either globally or on a
        specific resource.

        See: https://github.com/Tendrl/api/blob/master/docs/overview.adoc#flows

        Name:        "flows",
        Method:      "GET",
        Pattern:     "Flows",
        """
        pattern = "Flows"
        response = requests.get(
            pytest.config.getini("usm_api_url") + pattern,
            auth=self._auth,)
        self.print_req_info(response)
        self.check_response(response, asserts_in)
        # TODO: some minimal validation of flows response?
        return response.json()

    def get_nodes(self):
        """ Get list node ids.

        Name:        "get_nodes",
        Method:      "GET",
        Pattern:     "GetNodeList",
        """
        pattern = "GetNodeList"
        response = requests.get(
            pytest.config.getini("usm_api_url") + pattern,
            auth=self._auth)
        self.print_req_info(response)
        self.check_response(response)
        return response.json()

    def import_cluster(self, nodes, sds_type=None, asserts_in=None):
        """ Import cluster.

        Name:        "import_cluster",
        Method:      "POST",
        Pattern:     "ImportCluster",

        Args:
            sds_type (str): ceph or glusterfs
            nodes (list): node list of cluster which will be imported
            asserts_in (dict): assert values for this call and this method
        """
        asserts_in = asserts_in or {
            "cookies": None,
            "ok": True,
            "reason": 'Accepted',
            "status": 202}
        pattern = "ImportCluster"
        data = {"node_ids": nodes}
        if sds_type:
            data["sds_type"] = sds_type
        response = requests.post(
            pytest.config.getini("usm_api_url") + pattern,
            data=json.dumps(data),
            auth=self._auth)
        self.print_req_info(response)
        self.check_response(response, asserts_in)
        return response.json()

    def get_cluster_list(self):
        """ Get list of clusters

        Name:        "get_cluster_list",
        Method:      "GET",
        Pattern:     "GetClusterList",
        """
        pattern = "GetClusterList"
        response = requests.get(
            pytest.config.getini("usm_api_url") + pattern,
            auth=self._auth)
        self.print_req_info(response)
        self.check_response(response)
        return response.json()["clusters"]
