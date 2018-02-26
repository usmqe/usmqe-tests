
"""
Graphite REST API.
"""

import requests
import pytest
from usmqe.api.base import ApiBase

LOGGER = pytest.get_logger("graphiteapi", module=True)


class ApiCommon(ApiBase):
    """ Common methods for graphite REST API.
    """

    def get_datapoints(self, target, from_date=None, until_date=None):
        """ Get required datapoints of provided Graphite target.
        Datapoints are in format:
        ``[[value, epoch-time], [value, epoch-time], ...]``

        Args:
            target: id of Graphite metric.
        """
        pattern = "render/?target={}&format=json".format(target)
        if from_date:
            pattern += "&from={}".format(from_date)
        if until_date:
            pattern += "&until={}".format(until_date)
        response = requests.get(
            pytest.config.getini("graphite_api_url") + pattern)
        self.check_response(response)
        return response.json()[0]["datapoints"]
