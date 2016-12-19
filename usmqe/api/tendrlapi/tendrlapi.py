"""
Tendrl REST API.
"""

import requests
import pytest
from usmqe.api.base import ApiBase

LOGGER = pytest.get_logger("tendrlapi", module=True)


class ApiCommon(ApiBase):
    """ Common methods for Tendrl REST API.
    """

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


class ApiGluster(ApiCommon):
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
        pattern = "GlusterImportCluster"
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
        pattern = "GetClusterList"
        response = requests.get(pytest.config.getini("usm_api_url") + pattern)
        self.print_req_info(response)
        self.check_response(response)
        return response.json()

    def find_id_in_list(self, cluster_id, positive=True):
        found = False
        # TODO correct to be more pythonic
        for item in self.get_cluster_list():
            if item["cluster_id"] == cluster_id:
                found = True
        if positive:
            pytest.check(found, "")
        else:
            pytest.check(not found, "")

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
        response = requests.post(pytest.config.getini("usm_api_url") + pattern,
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

    def check_volume_attribute(self, cluster, volume, attribute, value, positive=True):
        pattern = "{}/GetVolumeList".format(cluster)
        response = requests.get(pytest.config.getini("usm_api_url") + pattern)
        self.print_req_info(response)
        self.check_response(response)

        for item in response.json():
            if item["vol_id"] == volume:
                if positive:
                    pytest.check(item[attribute] == value)
                else:
                    pytest.check(item[attribute] != value)
