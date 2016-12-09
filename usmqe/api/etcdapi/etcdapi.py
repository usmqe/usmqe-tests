
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

    def wait_for_job(self, id, max_count=30):
        count = 0
        status = ""
        while (status != "finished" and count < max_count):
            status = self.get_job_attribute(id, "status")
            count += 1
            time.sleep(1)
        LOGGER.debug("status: %s" % status)
        pytest.check(status == "finished")
        return status

    def get_job_attribute(self, id, attribute):
        pattern = "keys/queue/{}".format(id)
        response = requests.get(pytest.config.getini("etcd_api_url") + pattern)
        # self.print_req_info(response)
        self.check_response(response)
        return json.loads(response.json()["node"]["value"])[attribute]
