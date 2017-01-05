
"""
SkyRing REST API.
"""

import json
import time
import requests
import pytest
from usmqe.api.base import ApiBase

LOGGER = pytest.get_logger("etcdapi", module=True)


class ApiCommon(ApiBase):
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
        pytest.check(current_status == status, issue=issue)
        return current_status

    def get_job_attribute(self, cluster_id, attribute):
        """ Get required attribute of given cluster.

        Args:
            cluster_id: tendrl id of cluster
            attribute: attribute that is in given cluster
        """
        pattern = "keys/queue/{}".format(cluster_id)
        response = requests.get(pytest.config.getini("etcd_api_url") + pattern)
        self.check_response(response)
        return json.loads(response.json()["node"]["value"])[attribute]
