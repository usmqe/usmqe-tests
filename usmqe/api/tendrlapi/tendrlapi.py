"""
SkyRing REST API.
"""

import json

import requests
import pytest
import usmqe.inventory as inventory
from usmqe.gluster import gluster
from usmqe.api.etcdapi import etcdapi

LOGGER = pytest.get_logger("tendrlapi", module=True)


class Api(object):
    """ Basic class for Tendrl REST API.
    """

#    default_asserts = {
#        "cookies": None,
#        "ok": True,
#        "reason": 'OK',
#        "status": 200,
#    }

#    user_info = {"username": "%s", "email": "%s@localhost",
#                 "role": "admin", "groups": []}

    ldap_config = {
        "ldapserver": None, "port": None, "base": None,
        "domainadmin": None, "password": None, "uid": None,
        "firstname": None, "lastname": None,
        "displayname": None, "email": None,
    }

    def __init__(self, copy_from=None):
        #        self.cookies = {}
        self.verify = pytest.config.getini("usm_ca_cert")
        if copy_from:
            #            self.cookies = copy_from.cookies
            self.verify = copy_from.verify

    @staticmethod
    def print_req_info(resp):
        """ Print debug information.

        Args:
            resp: response
        """
        LOGGER.debug("request.url:  %s" % resp.request.url)
        LOGGER.debug("request.method:  %s" % resp.request.method)
        LOGGER.debug("request.body:  %s" % resp.request.body)
        LOGGER.debug("request.headers:  %s" % resp.request.headers)
        LOGGER.debug("response.cookies: %s" % resp.cookies)
        LOGGER.debug("response.content: %s" % resp.content)
        LOGGER.debug("response.headers: %s" % resp.headers)
        try:
            LOGGER.debug(
                "response.json:    %s" % resp.json(encoding='unicode'))
        except ValueError:
            LOGGER.debug("response.json:    ")
        LOGGER.debug("response.ok:      %s" % resp.ok)
        LOGGER.debug("response.reason:  %s" % resp.reason)
        LOGGER.debug("response.status:  %s" % resp.status_code)
        LOGGER.debug("response.text:    %s" % resp.text)

    @staticmethod
    def check_response(resp, asserts_in=None, issue=None):
        """ Check default asserts.

        It checks: *ok*, *status*, *reason*.
        Args:
            resp: response to check
        """

        asserts = Api.default_asserts.copy()
        if asserts_in:
            asserts.update(asserts_in)
        if "cookies" in asserts and asserts["cookies"] is None:
            pytest.check(not(resp.cookies), "Cookies should be empty.")
        pytest.check(
            resp.ok == asserts["ok"],
            "There should be ok == %s." % str(asserts["ok"]))
        pytest.check(resp.status_code == asserts["status"],
                     "Status code should equal to %s" % asserts["status"])
        pytest.check(resp.reason == asserts["reason"],
                     "Reason should equal to %s" % asserts["reason"])

    @staticmethod
    def check_dict(data, schema):
        """
        Check dictionary schema (keys, value types).

        Parameters:
          data - dictionary to check
          schema - dictionary with keys and value types, e.g.:
                  {'name': str, 'size': int, 'tasks': dict}
        """
        LOGGER.debug("check_dict - data: %s", data)
        LOGGER.debug("check_dict - schema: %s", schema)
        expected_keys = sorted(schema.keys())
        keys = sorted(data.keys())
        pytest.check(
            keys == expected_keys,
            "Data should contains keys: %s" % expected_keys)
        for key in keys:
            pytest.check(key in expected_keys,
                         "Unknown key '%s' with value '%s' (type: '%s')." %
                         (key, data[key], type(data[key])))
            if key in expected_keys:
                pytest.check(isinstance(data[key], schema[key]))
                if isinstance(data[key], schema[key]):
                    LOGGER.passed(
                        "Value '%s' (type: %s) for key '%s' should be '%s'." %
                        (data[key], type(data[key]), key, schema[key]))
                else:
                    LOGGER.failed(
                        "Value '%s' (type: %s) for key '%s' should be '%s'." %
                        (data[key], type(data[key]), key, schema[key]))


class ApiCommon(Api):
    """ Common methods for Tendrl REST API.
    """

    def login(self, username, password, asserts_in=None):
        """ Login to REST API

        Name:        "login",
        Method:      "POST",
        Pattern:     "auth/login",

        Args:
            username: username
            password: password
            asserts_in: assert values for this call and this method
        """
    pass

    def logout(self, asserts_in=None):
        """ Logout from REST API

        Name:        "logout",
        Method:      "POST",
        Pattern:     "auth/logout",

        Args:
            asserts_in: assert values for this call and this method
        """
    pass

    def call(self, pattern=None, data=None, method="GET"):
        """ Call api function with given json.

        Args:
            pattern: string containing api key to given function
            json: json string containing data that will be sent to api server
            method: string containing HTTP method for RESTful api
        """

        if method == "POST":
            req = requests.post(pytest.config.getini("usm_api_url") + pattern,
                                json=data)
            LOGGER.debug("post_data: %s" % json.dumps(data))
        elif method == "GET":
            req = requests.get(pytest.config.getini("usm_api_url") + pattern,
                               json=data)
        Api.print_req_info(req)
        return req


class ApiGluster(ApiCommon):
    """ Gluster methods for Tendrl REST API.
    """

    def get_nodes(self):
        """ Get list node ids.

        Name:        "get_nodes",
        Method:      "GET",
        Pattern:     "GetNodeList",
        """
        response = self.call(pattern="GetNodeList", method="GET")
        expected_response = 200
        pytest.check(response.status_code == expected_response)
        return [x["node_id"] for x in response.json()]

    def import_cluster(self, cluster_data):
        """ Import gluster cluster defined by json.

        Name:        "import_cluster",
        Method:      "POST",
        Pattern:     "GlusterImportCluster",

        Args:
            cluster_data: json structure containing data that will be sent to api server
        """
        response = self.call(
            pattern="/GlusterImportCluster",
            method="POST",
            data=cluster_data)
        expected_response = 202
        pytest.check(response.status_code == expected_response)
        etcd_api = etcdapi.ApiCommon()
        job_id = response.json()["job_id"]
        status = etcd_api.wait_for_job(job_id)
        pytest.check(status == "finished")

        response = self.call(pattern="GetClusterList", method="GET")
        expected_response = 200
        pytest.check(response.status_code == expected_response)
        pytest.check(response.status_code is not None)

        cluster_id = etcd_api.get_job_attribute(
            id=job_id, attribute="cluster_id")
        return cluster_id

    def get_brick_addresses(
            self,
            brick="/bricks/fs_gluster01/test",
            role="gluster"):
        """ Get list of host urls from specified role with path to brick.

        Args:
            brick: path where should be placed brick in filesystem
            role: role from inventory file
        """
        return ["{}:{}".format(x, brick) for x in inventory.role2hosts(role)]

    def get_volume_id(self, cluster, name):
        """ Get id of gluster volume specified by name from cluster with given id

        Name:        "get_volume_id",
        Method:      "GET",
        Pattern:     ":cluster_id:/GetVolumeList",

        Args:
            cluster: id of cluster where will be created volume
            name: name of volume
        """
        response = self.call(
            pattern="{}/GetVolumeList".format(cluster),
            method="GET")
        id = False
        for item in response.json():
            if item["name"] == name:
                id = item["vol_id"]
        return id

    def create_volume(self, cluster, volume_data):
        """ Import gluster cluster defined by json.

        Name:        "create_volume",
        Method:      "POST",
        Pattern:     ":cluster_id:/GlusterCreateVolume",

        Args:
            cluster: id of a cluster where will be created volume
            volume_data: json structure containing data that will be sent to api server
        """
        response = self.call(
            pattern="{}/GlusterCreateVolume".format(cluster),
            method="POST",
            data=volume_data)
        expected_response = 202
        pytest.check(response.status_code == expected_response,
                     "Status code should be {}".format(expected_response))

        etcd_api = etcdapi.ApiCommon()
        status = etcd_api.wait_for_job(response.json()["job_id"])
        pytest.check(
            status == "finished",
            "Status of job should be `finished`")

    def delete_volume(self, cluster, post_data):
        """ Import gluster cluster defined by json.

        Name:        "delete_volume",
        Method:      "POST",
        Pattern:     ":cluster_id:/GlusterDeleteVolume",

        Args:
            cluster: id of a cluster where will be created volume
            volume_data: json structure containing data that will be sent to api server
        """
        response = self.call(
            pattern="{}/GlusterDeleteVolume".format(cluster),
            method="POST",
            data=post_data)
        expected_response = 202
        pytest.check(response.status_code == expected_response,
                     "Status code should be {}".format(expected_response))

        etcd_api = etcdapi.ApiCommon()
        status = etcd_api.wait_for_job(response.json()["job_id"])
        pytest.check(
            status == "finished",
            "Status of job should be `finished`")
