"""
Tendrl REST API.
"""

import requests
import pytest
from usmqe.api.tendrlapi.common import TendrlApi

LOGGER = pytest.get_logger("glusterapi", module=True)


class TendrlApiGluster(TendrlApi):
    """ Gluster methods for Tendrl REST API.
    """

    def get_nodes(self):
        """ Get list node ids.

        Name:        "get_nodes",
        Method:      "GET",
        Pattern:     "GetNodeList",
        """
        pattern = "GetNodeList"
        response = requests.get(pytest.config.getini("usm_api_url") + pattern)
        self.print_req_info(response)
        self.check_response(response)
        return response.json()

    def import_cluster(self, cluster_data):
        """ Import gluster cluster defined by json.

        Name:        "import_cluster",
        Method:      "POST",
        Pattern:     "GlusterImportCluster",

        Args:
            cluster_data: json structure containing data that will be sent to api server
        """
        pattern = "ImportCluster"
        response = requests.post(pytest.config.getini("usm_api_url") + pattern,
                                 json=cluster_data)
        asserts = {
            "reason": 'Accepted',
            "status": 202,
        }
        self.print_req_info(response)
        self.check_response(response, asserts)
        return response.json()

    def get_cluster_list(self):
        """ Get list of clusters

        Name:        "get_cluster_list",
        Method:      "GET",
        Pattern:     "GetClusterList",
        """
        pattern = "GetClusterList"
        response = requests.get(pytest.config.getini("usm_api_url") + pattern)
        self.print_req_info(response)
        self.check_response(response)
        return response.json()["clusters"]

    def get_volume_list(self, cluster):
        """ Get list of gluster volumes specified by cluster id

        Name:        "get_volume_list",
        Method:      "GET",
        Pattern:     ":cluster_id:/GetVolumeList",

        Args:
            cluster: id of cluster where will be created volume
        """
        pattern = "{}/GetVolumeList".format(cluster)
        response = requests.get(pytest.config.getini("usm_api_url") + pattern)
        self.print_req_info(response)
        self.check_response(response)
        return response.json()

    def create_volume(self, cluster, volume_data):
        """ Import gluster cluster defined by json.

        Name:        "create_volume",
        Method:      "POST",
        Pattern:     ":cluster_id:/GlusterCreateVolume",

        Args:
            cluster: id of a cluster where will be created volume
            volume_data: json structure containing data that will be sent to api server
        """
        pattern = "{}/GlusterCreateVolume".format(cluster)
        response = requests.post(pytest.config.getini("usm_api_url") + pattern,
                                 json=volume_data)
        asserts = {
            "reason": 'Accepted',
            "status": 202,
        }
        self.print_req_info(response)
        self.check_response(response, asserts)
        return response.json()

    def delete_volume(self, cluster, post_data):
        """ Import gluster cluster defined by json.

        Name:        "delete_volume",
        Method:      "POST",
        Pattern:     ":cluster_id:/GlusterDeleteVolume",

        Args:
            cluster: id of a cluster where will be created volume
            volume_data: json structure containing data that will be sent to api server
        """
        pattern = "{}/GlusterDeleteVolume".format(cluster)
        response = requests.delete(pytest.config.getini("usm_api_url") + pattern,
                                 json=post_data)
        asserts = {
            "reason": 'Accepted',
            "status": 202,
        }
        self.print_req_info(response)
        self.check_response(response, asserts)
        return response.json()

    def start_volume(self, cluster, volume_data):
        """ Start gluster volume specified by json.

        Name:        "start_volume",
        Method:      "POST",
        Pattern:     ":cluster_id:/GlusterStartVolume",

        Args:
            cluster: id of a cluster where will be created volume
            volume_data: json structure containing data that will be sent to api server
        """
        pattern = "{}/GlusterStartVolume".format(cluster)
        response = requests.post(pytest.config.getini("usm_api_url") + pattern,
                                 json=volume_data)
        asserts = {
            "reason": 'Accepted',
            "status": 202,
        }
        self.print_req_info(response)
        self.check_response(response, asserts)
        return response.json()

    def stop_volume(self, cluster, volume_data):
        """ Stop gluster volume specified by json.

        Name:        "stop_volume",
        Method:      "POST",
        Pattern:     ":cluster_id:/GlusterStartVolume",

        Args:
            cluster: id of a cluster where will be created volume
            volume_data: json structure containing data that will be sent to api server
        """
        pattern = "{}/GlusterStopVolume".format(cluster)
        response = requests.post(pytest.config.getini("usm_api_url") + pattern,
                                 json=volume_data)
        asserts = {
            "reason": 'Accepted',
            "status": 202,
        }
        self.print_req_info(response)
        self.check_response(response, asserts)
        return response.json()
