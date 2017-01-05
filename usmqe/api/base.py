
"""
Basic REST API.
"""

import pytest
import json

LOGGER = pytest.get_logger("api_base", module=True)


class ApiBase(object):
    """ Basic class for REST API.
    """

    default_asserts = {
        "cookies": None,
        "ok": True,
        "reason": 'OK',
        "status": 200,
    }

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
    def check_response(resp, asserts_in=None):
        """ Check default asserts.

        It checks: *ok*, *status*, *reason*.
        Args:
            resp: response to check
            asserts_in: asserts that are compared with response
        """

        asserts = ApiBase.default_asserts.copy()
        if asserts_in:
            asserts.update(asserts_in)
        # if "cookies" in asserts and asserts["cookies"] is None:
        #    pytest.check(not(resp.cookies), "Cookies should be empty.")
        try:
            json.dumps(resp.json(encoding='unicode'))
        except ValueError:
            pytest.check(False, issue="Bad response json format.")
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
