
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
        """Get list of slugs that identify dashboards in Grafana.
        For more information about ``slugs`` refer to:
        ``http://docs.grafana.org/http_api/dashboard/#get-dashboard-by-slug``
        """
        pattern = "search"
        response = requests.get(
            pytest.config.getini("grafana_api_url") + pattern)
        self.check_response(response)
        return [
            dashboard["uri"].split("/")[1] for dashboard in response.json()
            if dashboard["type"] == "dash-db"]

    def get_dashboard(self, slug):
        """Get layout of dashboard described in grafana. For dashboard
        reference is used ``slug``. For more information about ``slugs``
        refer to:
        ``http://docs.grafana.org/http_api/dashboard/#get-dashboard-by-slug``

        Args:
            slug: Slug of dashboard uri. Slug is the url friendly version
                  of the dashboard title.
        """
        pattern = "dashboards/db/{}".format(slug)
        response = requests.get(
            pytest.config.getini("grafana_api_url") + pattern)
        self.check_response(response)
        return response.json()
