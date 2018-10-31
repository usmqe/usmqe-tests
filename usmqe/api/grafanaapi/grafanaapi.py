
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

    def get_panel(self, panel_title, row_title, dashboard):
        """
        Args:
          panel_title (str): title of desired panel
          row_title (str): title of row containing desired panel
          dashboard (str): stub of dashboard containing desired panel
        """
        layout = self.get_dashboard(dashboard)
        assert len(layout) > 0
        dashboard_rows = layout["dashboard"]["rows"]
        found_rows = [
            row for row in dashboard_rows
            if "title" in row and
            row["title"] == row_title]
        assert len(found_rows) == 1
        panels = found_rows[0]["panels"]
        found_panels = [
            panel for panel in panels
            if "title" in panel and
            panel["title"] == panel_title]
        assert len(found_panels) == 1
        return found_panels[0]

    def get_panel_chart_targets(self, panel, cluster_identifier=""):
        """
        Get all targets from panel. Returns list of lists for each visible line
        in chart.

        Args:
            panel (object): panel object from *get_panel* function
            cluster_identifier (str): identifier of cluster to use withni
                targets
        """
        targets = []
        for target in panel["targets"]:
            if "hide" not in target.keys() or not target["hide"]:
                if "targetFull" in target.keys() and target["targetFull"]:
                    targets.append(target["targetFull"])
                else:
                    targets.append(target["target"])
        output = []
        for target in targets:
            if "$cluster_id" in target:
                target = target.replace("$cluster_id", cluster_identifier)
            if "$host_name" in target:
                target = target.replace("$host_name", pytest.config.getini(
                    "usm_cluster_member").replace(".", "_"))
            targets_split = target.split(", ")

            target_output = []
            for t in targets_split:
                try:
                    t = t.rsplit("(", 1)[1]
                except Exception:
                    pass
                t = t.split(")", 1)[0]
                try:
                    t, target_options = t.rsplit(".{", 1)
                except Exception:
                    target_options = None
                if target_options:
                    target_output.extend(["{}.{}".format(t, x.split("}", 1)[0]) for x
                                          in target_options.split(",")])
                else:
                    # drop target tendrl label
                    if t.startswith("tendrl."):
                        target_output.append(t)
            output.append(target_output)
        LOGGER.debug(
            "targets found in panel {}: {}".format(panel["title"], output))
        return output

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
