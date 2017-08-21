"""
Tendrl REST API for gluster.
"""

import requests
import pytest
from usmqe.api.tendrlapi.common import TendrlApi

LOGGER = pytest.get_logger("glusterapi", module=True)


class TendrlApiGluster(TendrlApi):
    """ Gluster methods for Tendrl REST API.
    """
    def import_cluster(self, nodes, asserts_in=None):
        """ Import Gluster cluster.

        Args:
            nodes (list): node list of cluster which will be imported
            asserts_in (dict): assert values for this call and this method
        """
        return super().import_cluster(nodes, "gluster", asserts_in)

    def create_cluster(
            self,
            name,
            cluster_id,
            nodes,
            network,
            conf_overrides=None,
            asserts_in=None):
        """ Create Gluster cluster.

        Args:
            name (str): name of cluster
            cluster_id (str): id of cluster
            nodes (list): list of dictionaries containing node identification
                          and node role
            network (str): ip address and mask in prefix format of network with nodes
            conf_overrides (dict): dictionary containing special settings related
                        to specific sds type.
            asserts_in (dict): assert values for this call and this method
        """
        return super().create_cluster(
            name=name,
            cluster_id=cluster_id,
            nodes=nodes,
            public_network=network,
            cluster_network=network,
            node_identifier="ip",
            conf_overrides=conf_overrides,
            sds_type="gluster",
            sds_version=pytest.config.getini("usm_gluster_version"),
            asserts_in=asserts_in)

    def get_volume_list(self, cluster):
        """ Get list of gluster volumes specified by cluster id

        Name:        "get_volume_list",
        Method:      "GET",
        Pattern:     ":cluster_id:/GetVolumeList",

        Args:
            cluster: id of cluster where will be created volume
        """
        pattern = "{}/GetVolumeList".format(cluster)
        response = requests.get(
            pytest.config.getini("usm_api_url") + pattern,
            auth=self._auth)
        self.print_req_info(response)
        self.check_response(response)
        return response.json()

    def create_bricks(self, cluster, nodes, devices, brick_name, asserts_in=None):
        """Create volume bricks on given nodes with specified path.

        Name:        "create_bricks",
        Method:      "POST",
        Pattern:     ":cluster_id:/GlusterCreateBrick",

        Args:
            cluster (str): id of a cluster with nodes
            nodes (list): ids of nodes where should be bricks
            devices (list): pathes to device where should be created bricks
            brick_name (str): name of brick directory
        """
        pattern = "{}/GlusterCreateBrick".format(cluster)
        data = {"Cluster.node_configuration": {
            x: {device: {"brick_name": brick_name} for device in devices} for x in nodes}}
        response = requests.post(
            pytest.config.getini("usm_api_url") + pattern,
            json=data,
            auth=self._auth)
        asserts = asserts_in or {
            "reason": 'Accepted',
            "status": 202,
        }
        self.print_req_info(response)
        self.check_response(response, asserts)
        return response.json()

    def create_volume(self, cluster, volume_data):
        """ Import gluster cluster defined by json.

        Name:        "create_volume",
        Method:      "POST",
        Pattern:     ":cluster_id:/GlusterCreateVolume",

        Args:
            cluster: id of a cluster where will be created volume
            volume_data: json structure containing data that will be
                         sent to api server
        """
        pattern = "{}/GlusterCreateVolume".format(cluster)
        response = requests.post(
            pytest.config.getini("usm_api_url") + pattern,
            json=volume_data,
            auth=self._auth)
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
        Method:      "DElETE",
        Pattern:     ":cluster_id:/GlusterDeleteVolume",

        Args:
            cluster: id of a cluster where will be created volume
            volume_data: json structure containing data that will be
                         sent to api server
        """
        pattern = "{}/GlusterDeleteVolume".format(cluster)
        response = requests.delete(
            pytest.config.getini("usm_api_url") + pattern,
            json=post_data,
            auth=self._auth)

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
            volume_data: json structure containing data that will be
                         sent to api server
        """
        pattern = "{}/GlusterStartVolume".format(cluster)
        response = requests.post(
            pytest.config.getini("usm_api_url") + pattern,
            json=volume_data,
            auth=self._auth)
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
            volume_data: json structure containing data that will be
                         sent to api server
        """
        pattern = "{}/GlusterStopVolume".format(cluster)
        response = requests.post(
            pytest.config.getini("usm_api_url") + pattern,
            json=volume_data,
            auth=self._auth)
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
