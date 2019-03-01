
"""
etcd REST API.
"""

import json
import time
import requests
import pytest
from usmqe.api.base import ApiBase
from usmqe.usmqeconfig import UsmConfig

LOGGER = pytest.get_logger("etcdapi", module=True)
CONF = UsmConfig()


class EtcdApi(ApiBase):
    """ Common methods for etcd REST API.
    """

    # TODO status, defaul finish, +issue parameter
    def wait_for_job_status(self, job_id, max_count=30, status="finished", issue=None):
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
            current_status = self.get_job_attribute(job_id, "status")
            count += 1
            time.sleep(1)
        LOGGER.debug("status: %s" % current_status)
        pytest.check(
            current_status == status,
            msg="Job status is {} and should be {}".format(current_status, status),
            issue=issue)
        return current_status

    def get_job_attribute(self, job_id, attribute):
        """ Get required attribute of given cluster.

        Args:
            job_id: id of created job
            attribute: attribute that is in given cluster
        """
        pattern = "queue/{}".format(job_id)
        response = self.get_key_value(pattern)
        self.print_req_info(response)
        return json.loads(response["node"]["value"])[attribute]

    def get_key_value(self, key):
        """ Get required value of a given key.

        Args:
            key: part of URI that is used in request on etcd
        """

        pattern = "keys/{}".format(key)
        if CONF.config["usmqe"]["etcd_api_url"].startswith("https"):
            response = requests.get(
                CONF.config["usmqe"]["etcd_api_url"] + pattern,
                cert=(
                    '/etc/pki/tls/certs/etcd.crt',
                    '/etc/pki/tls/private/etcd.key'),
                verify='/etc/pki/tls/certs/ca-usmqe.crt')
        else:
            response = requests.get(CONF.config["usmqe"]["etcd_api_url"] + pattern)
        self.print_req_info(response)
        self.check_response(response)
        return response.json()
