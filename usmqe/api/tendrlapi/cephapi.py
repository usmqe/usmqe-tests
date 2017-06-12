"""
Tendrl REST API for ceph.
"""
import pytest
import requests
from usmqe.api.tendrlapi.common import TendrlApi

LOGGER = pytest.get_logger("tendrlapi_ceph", module=True)


class TendrlApiCeph(TendrlApi):
    """ Ceph methods for Tendrl REST API.
    """
    def import_cluster(self, nodes, asserts_in=None):
        """ Import Ceph cluster.

        Args:
            nodes (list): node list of cluster which will be imported
            asserts_in (dict): assert values for this call and this method
        """
        return super().import_cluster(nodes, "ceph", asserts_in)

    def create_pool(self,
                    cluster,
                    name,
                    pg_num,
                    min_size,
                    size,
                    pool_type=None,
                    erasure_code_profile=None,
                    quota_enabled=None,
                    quota_max_objects=None,
                    quota_max_bytes=None,
                    asserts_in=None):
        """ Create Ceph pool.

        Name:        "create_pool",
        Method:      "POST",
        Pattern:     ":cluster_id:/CephCreatePool",

        Args:
            cluster (str): Cluster ID
            name (str): Pool name.
            pg_num (int): Number of placement groups.
            min_size (int): Minimum number of replicas required for I/O
                      in degraded state
            size (int): Number of replicas required for I/O.
            pool_type (str): Type of the Ceph pool (ec or replicated)
            erasure_code_profile (str): For erasure pools only. It must be
                                  an existing profile.
            quota_enabled (bool): Enable quota for the pool.
            quota_max_objects (int): Maximum number of object in pool.
            quota_max_bytes (int): Maximum number of bytes in pool.
            asserts_in (dict): assert values for this call and this method
        """
        pattern = "{}/CephCreatePool".format(cluster)
        pool_data = {
            "Pool.poolname": name,
            "Pool.pg_num": pg_num,
            "Pool.min_size": min_size,
            "Pool.size": size,
            }
        if pool_type:
            pool_data["Pool.type"] = pool_type
        if erasure_code_profile:
            pool_data["Pool.erasure_code_profile"] = erasure_code_profile
        if quota_enabled is not None:
            pool_data["Pool.quota_enabled"] = quota_enabled
        if quota_max_objects:
            pool_data["Pool.quota_max_objects"] = quota_max_objects
        if quota_max_bytes:
            pool_data["Pool.quota_max_bytes"] = quota_max_bytes
        response = requests.post(
            pytest.config.getini("usm_api_url") + pattern,
            json=pool_data,
            auth=self._auth)
        asserts_in = asserts_in or {
            "cookies": None,
            "ok": True,
            "reason": 'Accepted',
            "status": 202}
        self.print_req_info(response)
        self.check_response(response, asserts_in)
        return response.json()

    def update_pool(self,
                    cluster,
                    pool_id,
                    name=None,
                    size=None,
                    min_size=None,
                    pg_num=None,
                    quota_enabled=None,
                    quota_max_objects=None,
                    quota_max_bytes=None,
                    asserts_in=None):
        """ Update Ceph pool.

        Name:        "update_pool",
        Method:      "PUT",
        Pattern:     ":cluster_id:/CephUpdatePool",

        Args:
            cluster (str): Cluster ID
            pool_id (str): Pool ID
            name (str): Pool name.
            size (int): Number of replicas required for I/O.
            min_size (int): Minimum number of replicas required for I/O
                      in degraded state
            pg_num (int): Number of placement groups.
            quota_enabled (bool): Enable quota for the pool.
            quota_max_objects (int): Maximum number of object in pool.
            quota_max_bytes (int): Maximum number of bytes in pool.
            asserts_in (dict): assert values for this call and this method
        """
        pattern = "{}/CephUpdatePool".format(cluster)
        pool_data = {"Pool.pool_id": pool_id}

        if name:
            pool_data["Pool.poolname"] = name
        if size:
            pool_data["Pool.size"] = size
        if min_size:
            pool_data["Pool.min_size"] = min_size
        if pg_num:
            pool_data["Pool.pg_num"] = pg_num
        if quota_enabled is not None:
            pool_data["Pool.quota_enabled"] = quota_enabled
        if quota_max_objects:
            pool_data["Pool.quota_max_objects"] = quota_max_objects
        if quota_max_bytes:
            pool_data["Pool.quota_max_bytes"] = quota_max_bytes

        response = requests.put(
            pytest.config.getini("usm_api_url") + pattern,
            json=pool_data,
            auth=self._auth)
        asserts_in = asserts_in or {
            "cookies": None,
            "ok": True,
            "reason": 'Accepted',
            "status": 202}

        self.print_req_info(response)
        self.check_response(response, asserts_in)
        return response.json()

    def get_pool_list(self, cluster, asserts_in=None):
        """ Get pool list for specific Ceph cluster.

        Name:        "get_pool_list",
        Method:      "GET",
        Pattern:     ":cluster_id:/GetPoolList",

        Args:
            cluster (str): Cluster ID.
            asserts_in (dict): assert values for this call and this method
        """
        pattern = "{}/GetPoolList".format(cluster)
        response = requests.get(
            pytest.config.getini("usm_api_url") + pattern,
            auth=self._auth)
        self.print_req_info(response)
        self.check_response(response, asserts_in)
        return response.json()

    def delete_pool(self, cluster, pool_id, asserts_in=None):
        """ Delete Ceph pool.

        Name:        "delete_pool",
        Method:      "DELETE",
        Pattern:     ":cluster_id:/CephDeletePool",

        Args:
            cluster (str): Cluster ID
            pool_id (str): Pool ID
            asserts_in (dict): assert values for this call and this method
        """
        pattern = "{}/CephDeletePool".format(cluster)
        pool_data = {"Pool.pool_id": pool_id}
        response = requests.delete(
            pytest.config.getini("usm_api_url") + pattern,
            json=pool_data,
            auth=self._auth)
        asserts_in = asserts_in or {
            "cookies": None,
            "ok": True,
            "reason": 'Accepted',
            "status": 202}
        self.print_req_info(response)
        self.check_response(response, asserts_in)
        return response.json()

    def create_rbd(self, cluster, pool_id, name, size, asserts_in=None):
        """ Create RBD in Ceph pool.

        Name:        "create_rbd",
        Method:      "POST",
        Pattern:     ":cluster_id:/CephCreateRbd",

        Args:
            cluster (str): Cluster ID
            pool_id (str): Pool ID
            name (str): RBD name
            size (int): RBD size
            asserts_in (dict): assert values for this call and this method
        """
        pattern = "{}/CephCreateRbd".format(cluster)
        pool_data = {"Rbd.pool_id": pool_id,
                     "Rbd.name": name,
                     "Rbd.size": size
                     }
        response = requests.post(
            pytest.config.getini("usm_api_url") + pattern,
            json=pool_data,
            auth=self._auth)
        asserts_in = asserts_in or {
            "cookies": None,
            "ok": True,
            "reason": 'Accepted',
            "status": 202}
        self.print_req_info(response)
        self.check_response(response, asserts_in)
        return response.json()

    def update_rbd(self, cluster, pool_id, name, size, asserts_in=None):
        """ Update RBD in Ceph pool.

        Name:        "update_rbd",
        Method:      "PUT",
        Pattern:     ":cluster_id:/CephResizeRbd",

        Args:
            cluster (str): Cluster ID
            pool_id (str): Pool ID
            name (str): RBD name
            size (int): RBD size
            asserts_in (dict): assert values for this call and this method
        """
        pattern = "{}/CephResizeRbd".format(cluster)
        pool_data = {"Rbd.pool_id": pool_id,
                     "Rbd.name": name,
                     "Rbd.size": size
                     }
        response = requests.put(
            pytest.config.getini("usm_api_url") + pattern,
            json=pool_data,
            auth=self._auth)
        asserts_in = asserts_in or {
            "cookies": None,
            "ok": True,
            "reason": 'Accepted',
            "status": 202}
        self.print_req_info(response)
        self.check_response(response, asserts_in)
        return response.json()

    def delete_rbd(self, cluster, pool_id, name, asserts_in=None):
        """ Delete RBD in Ceph pool.

        Name:        "delete_rbd",
        Method:      "DELETE",
        Pattern:     ":cluster_id:/CephDeleteRbd",

        Args:
            cluster (str): Cluster ID
            pool_id (str): Pool ID
            name (str): RBD name
            asserts_in (dict): assert values for this call and this method
        """
        pattern = "{}/CephDeleteRbd".format(cluster)
        pool_data = {"Rbd.pool_id": pool_id, "Rbd.name": name}
        response = requests.delete(
            pytest.config.getini("usm_api_url") + pattern,
            json=pool_data,
            auth=self._auth)
        asserts_in = asserts_in or {
            "cookies": None,
            "ok": True,
            "reason": 'Accepted',
            "status": 202}
        self.print_req_info(response)
        self.check_response(response, asserts_in)
        return response.json()

    def create_ecprofile(self, cluster, name, k_ec, m_ec,
                         plugin=None,
                         directory=None,
                         ruleset_fail_dom=None,
                         asserts_in=None):
        """ Create EC profile.

        Name:        "create_ecprofile",
        Method:      "POST",
        Pattern:     ":cluster_id:/CephCreateECProfile",

        Args:
            cluster (str): Cluster ID
            name (str): EC profile name
            k_ec (int): k value for ec profile
            m_ec (int): m value for ec profile
            plugin (str): EC profile plugin
            directory (str): directory for EC profile
            ruleset_fail_dom (str): rule set failure domain for EC profile
            asserts_in (dict): assert values for this call and this method
        """
        pattern = "{}/CephCreateECProfile".format(cluster)
        pool_data = {"ECProfile.name": name,
                     "ECProfile.k": k_ec,
                     "ECProfile.m": m_ec,
                     "ECProfile.plugin": plugin,
                     "ECProfile.directory": directory,
                     "ECProfile.ruleset_failure_domain": ruleset_fail_dom,
                     }
        response = requests.post(
            pytest.config.getini("usm_api_url") + pattern,
            json=pool_data,
            auth=self._auth)
        asserts_in = asserts_in or {
            "cookies": None,
            "ok": True,
            "reason": 'Accepted',
            "status": 202}
        self.print_req_info(response)
        self.check_response(response, asserts_in)
        return response.json()

    def delete_ecprofile(self, cluster, name, asserts_in=None):
        """ Delete EC profile.

        Name:        "delete_ecprofile",
        Method:      "DELETE",
        Pattern:     ":cluster_id:/CephDeleteECProfile",

        Args:
            cluster (str): Cluster ID
            name (str): EC profile name
            asserts_in (dict): assert values for this call and this method
        """
        pattern = "{}/CephDeleteECProfile".format(cluster)
        pool_data = {"ECProfile.name": name}
        response = requests.delete(
            pytest.config.getini("usm_api_url") + pattern,
            json=pool_data,
            auth=self._auth)
        asserts_in = asserts_in or {
            "cookies": None,
            "ok": True,
            "reason": 'Accepted',
            "status": 202}
        self.print_req_info(response)
        self.check_response(response, asserts_in)
        return response.json()
