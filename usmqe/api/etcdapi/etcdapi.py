
"""
SkyRing REST API.
"""

import json
import time
import requests
import pytest

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
    """ Common methods for skyring REST API.
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
#        asserts = Api.default_asserts.copy()
#        asserts.update({
#            "cookies": "session-key",
#            "json": json.loads('''{"message": "Logged in"}'''),
#            })
#        if asserts_in:
#            asserts.update(asserts_in)
#        data = json.dumps({'username': username, 'password': password})
#        req = requests.post(pytest.config.getini("etcd_api_url") + "auth/login",
#                            data, verify=self.verify)
#        Api.print_req_info(req)
#        Api.check_response(req, asserts)
#        if asserts["cookies"]:
#            pytest.check(req.cookies.keys(), "Cookies should not be empty.")
#            if req.cookies.keys():
#                pytest.check(req.cookies.keys().index(asserts["cookies"]) > -1,
#                             "Cookies should contain: %s" % asserts["cookies"])
#
#        pytest.check(req.json(encoding='unicode') == asserts["json"],
#                     "There should be login message in response.")
#        self.cookies.update(req.cookies)
#        return req.json(encoding='unicode')
    pass

    def logout(self, asserts_in=None):
        """ Logout from REST API

        Name:        "logout",
        Method:      "POST",
        Pattern:     "auth/logout",

        Args:
            asserts_in: assert values for this call and this method
        """
#        asserts = Api.default_asserts.copy()
#        asserts.update({
#            "cookies": None,
#            "json": json.loads('''{"message": "Logged out"}'''),
#            })
#        if asserts_in:
#            asserts.update(asserts_in)
#        req = requests.post(pytest.config.getini("etcd_api_url") + "auth/logout",
#                            cookies=self.cookies, verify=self.verify)
#        Api.print_req_info(req)
#        Api.check_response(req, asserts)
#        pytest.check(
#            req.cookies.keys() == [], "There should be empty logout cookie.")
#        pytest.check(req.json(encoding='unicode') == asserts["json"],
#                     "There should be logout message.")
#        return req.json(encoding='unicode')
    pass

    def call(self, pattern=None, json=None, method="GET"):
        """ Call api function with given json.

        Args:
            pattern: string containing api key to given function
            json: json string containing data that will be sent to api server
            method: strigng containing HTTP method for RESTful api
        """

#        client = etcd.Client(host="10.70.43.91", port=2379)
#        client.write("/api_job_queue/job_%s" % job_id1, json.dumps(job))

        if method == "POST":
            req = requests.post(pytest.config.getini("etcd_api_url") + pattern,
                            json=json)
        elif method == "GET":
            req = requests.get(pytest.config.getini("etcd_api_url") + pattern,
                            json=json)
        Api.print_req_info(req)
        return req

    def check_job(self, id):
        response = self.call(pattern="keys/queue/{}".format(id))
        return json.loads(response.json()["node"]["value"])["status"]

    def wait_for_job(self, id):
        count = 0
        status = ""
        while (status!="finished" and count<30):
            status = self.check_job(id)
            count += 1
            time.sleep(1)
        return status
