
"""
Grafana REST API.
"""

import requests
import pytest
from usmqe.api.base import ApiBase

LOGGER = pytest.get_logger("grafanaapi", module=True)


class GrafanaApi(ApiBase):
    """ Common methods for grafana REST API.
    """

    def get_dashboards(self):
        """Get list of dashboards defined in grafana.
        """
        pattern = "search"
        response = requests.get(
            pytest.config.getini("grafana_api_url") + pattern)
        self.check_response(response)
        return [
            dashboard["uri"].split("/")[1] for dashboard in response.json()
            if dashboard["type"] == "dash-db"]

    def get_dashboard(self, slug):
        """Get layout of dashboard described in grafana.

        Args:
            slug: slug of dashboard uri
        """
        pattern = "dashboards/db/{}".format(slug)
        print(pytest.config.getini("grafana_api_url") + pattern)
        response = requests.get(
            pytest.config.getini("grafana_api_url") + pattern)
        self.check_response(response)
        return response.json()
