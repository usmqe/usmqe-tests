
"""
Grafana REST API.
"""

import json
import requests
import pytest
from difflib import Differ
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
            slug (str): Slug of dashboard uri. Slug is the url friendly version
                  of the dashboard title.
        """
        pattern = "dashboards/db/{}".format(slug)
        response = requests.get(
            pytest.config.getini("grafana_api_url") + pattern)
        self.check_response(response)
        return response.json()

    def compare_structure(self, structure, slug):
        """Compare provided data structure with layout defined in Grafana.

        Args:
            structure (object): structure of grafana dashboard for comparison
            slug (str): Slug of dashboard uri. Slug is the url friendly version
                  of the dashboard title.
        """
        layout = self.get_dashboard(slug)
        pytest.check(
            len(layout) > 0,
            "{} dashboard should not be empty".format(slug))
        structure_grafana = {}
        for row in layout["dashboard"]["rows"]:
            structure_grafana[row["title"]] = []
            for panel in row["panels"]:
                if panel["title"]:
                    structure_grafana[row["title"]].append(panel["title"])
                elif "displayName" in panel.keys() and panel["displayName"]:
                    structure_grafana[row["title"]].append(panel["displayName"])

        LOGGER.debug("defined layout structure = {}".format(structure))
        LOGGER.debug("layout structure in grafana = {}".format(structure_grafana))
        d = Differ()
        LOGGER.debug("reduced diff between the layouts: {}".format(
            "".join([x.strip() for x in d.compare(
                json.dumps(structure, sort_keys=True),
                json.dumps(structure_grafana, sort_keys=True))])))
        pytest.check(
            structure == structure_grafana,
            "defined structure of panels should be equal to structure in grafana")
