
"""
Graphite REST API.
"""

import requests
import pytest
from usmqe.api.base import ApiBase
from usmqe.usmqeconfig import UsmConfig

LOGGER = pytest.get_logger("graphiteapi", module=True)
CONF = UsmConfig()


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
            CONF.config["usmqe"]["graphite_api_url"] + pattern)
        self.print_req_info(response)
        self.check_response(response)
        response_json = response.json()
        if len(response_json) == 1 and "datapoints" in response_json[0]:
            return response_json[0]["datapoints"]
        else:
            return response_json

    def compare_data_mean(
            self,
            expected_result,
            targets,
            from_date=None,
            until_date=None,
            divergence=10,
            sample_rate=1,
            operation='sum'):
        """
        Compare expected result with sum of means from graphite data from given targets.

        Args:
            expected_result (num): numeric value that is basis for comparison.
            targets (iterable): targets used for calculation of data mean
            from_date: datetime string or timestamp from which date are records shown
            until_date: datetime string or timestamp to which date are records shown
            divergence (num): numeric value of divergence used in final comparison
            sample_rate (int): number of samples per minute
            operation (str): this specifies operation that is done with data
                when there are more targets available:
                sum - summation of data
                diff - subtraction of data
        """
        graphite_data_mean_all = 0
        if from_date and not isinstance(from_date, int):
            from_date = int(from_date.timestamp())
        if until_date and not isinstance(until_date, int):
            until_date = int(until_date.timestamp())

        for idx, target in enumerate(targets):
            graphite_data = self.get_datapoints(
                target, from_date=from_date, until_date=until_date)
            # drop empty data points
            graphite_data = [x for x in graphite_data if x[0]]
            # process data from graphite
            graphite_data_mean = sum(
                [x[0] for x in graphite_data]) / max(
                    len(graphite_data), 1)
            # check for expected number of datapoints only when data are time bound
            if from_date and until_date:
                workload_time_range = until_date - from_date
                expected_number_of_datapoints = round(workload_time_range / 60) * sample_rate
                pytest.check(
                    (len(graphite_data) == expected_number_of_datapoints) or
                    (len(graphite_data) == expected_number_of_datapoints - 1),
                    "Number of samples of used data should be {}, is {}.".format(
                        expected_number_of_datapoints, len(graphite_data)))
            LOGGER.debug("mean of data from `{}` in Graphite: {}".format(
                target, graphite_data_mean))
            if operation == 'sum' or idx == 0:
                graphite_data_mean_all += graphite_data_mean
            elif operation == 'diff':
                graphite_data_mean_all -= graphite_data_mean
            else:
                raise ValueError("Operation '{0}' is not supported.".format(
                    operation))
        LOGGER.info("mean of all used data from Graphite: {}".format(
            graphite_data_mean_all))
        LOGGER.info("used operation: {}".format(operation))
        minimal_expected_result = expected_result - divergence
        maximal_expected_result = expected_result + divergence
        msg = "Data mean should be {}, data mean in Graphite is: {}, ".format(
            expected_result,
            graphite_data_mean_all)
        msg += "applicable divergence is {}".format(divergence)
        pytest.check(
            minimal_expected_result <
            graphite_data_mean_all < maximal_expected_result,
            msg)
