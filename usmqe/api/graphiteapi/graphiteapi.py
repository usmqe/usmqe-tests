
"""
Graphite REST API.
"""

import requests
import pytest
from usmqe.api.base import ApiBase

LOGGER = pytest.get_logger("graphiteapi", module=True)


class GraphiteApi(ApiBase):
    """ Common methods for graphite REST API.
    """

    def get_datapoints(self, target, from_date=None, until_date=None):
        """ Get required datapoints of provided Graphite target. If there
        are no datapoints then return empty list.
        Datapoints are in format:
        ``[[value, epoch-time], [value, epoch-time], ...]``
        Datetime format used by Graphite API is described on:
        ``https://graphite-api.readthedocs.io/en/latest/api.html#from-until``

        Args:
            target: id of Graphite metric.
            from_date: datetime string from which date are records shown
            until_date: datetime string to which date are records shown
        """
        pattern = "render/?target={}&format=json".format(target)
        if from_date:
            pattern += "&from={}".format(from_date)
        if until_date:
            pattern += "&until={}".format(until_date)
        response = requests.get(
            pytest.config.getini("graphite_api_url") + pattern)
        self.print_req_info(response)
        self.check_response(response)
        response_json = response.json()
        if len(response_json) == 1 and "datapoints" in response_json[0]:
            return response_json[0]["datapoints"]
        else:
            return response_json
