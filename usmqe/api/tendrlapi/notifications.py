"""
tendrl REST API.
"""

import requests
import pytest
from usmqe.api.tendrlapi.common import TendrlApi
from plugin.usmqe_config import UsmConfig

LOGGER = pytest.get_logger("tendrlapi.notifications", module=True)
config = UsmConfig()


class ApiNotifications(TendrlApi):
    """ Main class for interact with REST API - notifications.
    """
    def get_notifications(self, asserts_in=None):
        """ Get notifications.

        Name:        "GET_notifications",
        Method:      "GET",
        Pattern:     "notifications",

        Args:
            asserts_in: assert values for this call and this method
        """
        pattern = "notifications"
        request = requests.get(
            config.config["tests"]["usm_api_url"] + pattern,
            auth=self._auth)
        self.print_req_info(request)
        self.check_response(request, asserts_in)
        return request.json(encoding='unicode')
