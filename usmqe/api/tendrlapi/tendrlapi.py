"""
Tendrl REST API.
"""

import requests
import time
import pytest
from usmqe.api.base import ApiBase

LOGGER = pytest.get_logger("tendrlapi", module=True)


class ApiCommon(ApiBase):
    """ Common methods for Tendrl REST API.
    """

    def get_job_attribute(self, job_id, attribute="status", section=None):
        """ Get attrubute from job specified by job_id.

        Name:       "get_job_attribute",
        Method:     "GET",
        Pattern     "jobs",

        Args:
            job_id:     id of job
            attribute:  attribute which value is looked for
            section:    section of response in which is attribute located
        """
        pattern = "jobs/{}".format(job_id)
        response = requests.get(pytest.config.getini("usm_api_url") + pattern)
        self.print_req_info(response)
        self.check_response(response)
        if section:
            return response.json()[section][attribute]
        else:
            return response.json()[attribute]

    def wait_for_job_status(self, job_id, max_count=30, status="finished", issue=None):
        """ Repeatedly check if status of job with provided id is in reqquired state.

        Args:
            job_id: id provided by api request
            max_count: maximum of iterations
            status: expected status of job that is checked
            issue: pytest issue message (usually github issue link)
        """
        count = 0
        current_status = ""
        while (current_status != status and count < max_count):
            current_status = self.get_job_attribute(job_id, "status")
            count += 1
            time.sleep(1)
        LOGGER.debug("status: %s" % current_status)
        pytest.check(current_status == status, issue=issue)
        return current_status

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

    def get_volume_attribute(self, cluster, volume, attribute):
        """ Check if provided volume has attribute of given value.

        Args:
            cluster: id of a cluster
            volume: id of a volume
            attribute: name of the searched attribute
        """
        value = [x[attribute] for x in self.get_volume_list(cluster)
                 if x["vol_id"] == volume][0]
        LOGGER.debug("{} = {}".format(attribute, value))
        return value
