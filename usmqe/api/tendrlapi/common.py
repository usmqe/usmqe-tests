"""
Tendrl REST API common functions.
"""

import time
import pytest
import requests
from usmqe.api.base import ApiBase

LOGGER = pytest.get_logger("commonapi", module=True)


class ApiCommon(ApiBase):
    """ Common methods for Tendrl REST API.
    """

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
        response = requests.get(pytest.config.getini("usm_api_url") + pattern)
        self.print_req_info(response)
        self.check_response(response)
        if section:
            return response.json()[section][attribute]
        else:
            return response.json()[attribute]

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
