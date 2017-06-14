
"""
Basic REST API.
"""

import json
import pytest

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
        LOGGER.debug("request.url:  {}".format(resp.request.url))
        LOGGER.debug("request.method:  {}".format(resp.request.method))
        LOGGER.debug("request.body:  {}".format(resp.request.body))
        LOGGER.debug("request.headers:  {}".format(resp.request.headers))
        LOGGER.debug("response.cookies: {}".format(resp.cookies))
        LOGGER.debug("response.content: {}".format(resp.content))
        LOGGER.debug("response.headers: {}".format(resp.headers))
        # try:
        #     LOGGER.debug(
        #         "response.json:    {}".format(resp.json(encoding='unicode')))
        # except ValueError:
        #     LOGGER.debug("response.json:    ")
        LOGGER.debug("response.ok:      {}".format(resp.ok))
        LOGGER.debug("response.reason:  {}".format(resp.reason))
        LOGGER.debug("response.status:  {}".format(resp.status_code))
        LOGGER.debug("response.text:    {}".format(resp.text))

    @staticmethod
    def check_response(resp, asserts_in=None, issue=None):
        """ Check default asserts.

        It checks: *ok*, *status*, *reason*.
        Args:
            resp: response to check
            asserts_in: asserts that are compared with response
            issue: known issue, log WAIVE
        """

        asserts = ApiBase.default_asserts.copy()
        if asserts_in:
            asserts.update(asserts_in)
        try:
            json.dumps(resp.json(encoding='unicode'))
        except ValueError as err:
            pytest.check(
                False,
                "Bad response '{}' json format: '{}'".format(resp, err)
                )
        pytest.check(
            resp.ok == asserts["ok"],
            "There should be ok == {}".format(str(asserts["ok"])),
            issue=issue)
        pytest.check(resp.status_code == asserts["status"],
                     "Status code should equal to {}".format(asserts["status"]),
                     issue=issue)
        pytest.check(resp.reason == asserts["reason"],
                     "Reason should equal to {}".format(asserts["reason"]),
                     issue=issue)

    @staticmethod
    def check_dict(data, schema, issue=None):
        """Check dictionary schema (keys, value types).

        Args:
            data: dictionary to check
            schema: dictionary with keys and value types, e.g.:
                  {'name': str, 'size': int, 'tasks': dict}
            issue: known issue, log WAIVE
        """
        LOGGER.debug("check_dict - data: {}".format(data))
        LOGGER.debug("check_dict - schema: {}".format(schema))
        expected_keys = sorted(schema.keys())
        keys = sorted(data.keys())
        pytest.check(
            keys == expected_keys,
            "Data should contains keys: {}".format(expected_keys))
        for key in keys:
            pytest.check(key in expected_keys,
                         "Unknown key '{}' with value '{}' (type: '{}').".format(
                             key, data[key], type(data[key])),
                         issue=issue)
            if key in expected_keys:
                pytest.check(
                    isinstance(data[key], schema[key]),
                    "{} should be instance of {}".format(data[key],
                                                         schema[key]),
                    issue=issue)
