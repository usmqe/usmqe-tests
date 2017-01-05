
"""
REST API test suite - gluster cluster
"""
import pytest

from usmqe.api.tendrlapi import tendrlapi
from usmqe.api.etcdapi import etcdapi


LOGGER = pytest.get_logger('cluster_test', module=True)
"""@pylatest default
Setup
=====
"""

"""@pylatest default
Teardown
========
"""

"""@pylatest api/gluster.cluster_import
API-gluster: cluster_import
***************************

.. test_metadata:: author fbalak@redhat.com

Description
===========

Positive import gluster cluster.
"""


def test_cluster_import_valid():
    """@pylatest api/gluster.cluster_import
        .. test_step:: 1

        Get list of ids of availible nodes.

        .. test_result:: 1

                Server should return response in JSON format:

                        {
                ...
                  {
                  "fqdn": hostname,
                  "machine_id": some_id,
                  "node_id": node_id
                  },
                ...
                        }

                Return code should be **200** with data ``{"message": "OK"}``.

        """
    api = tendrlapi.ApiGluster()
    """@pylatest api/gluster.cluster_import
        .. test_step:: 2

            Send POST request to Tendrl API ``APIURL/GlusterImportCluster

        .. test_result:: 2

            Server should return response in JSON format:

                {
                  "job_id": job_id
                }

            Return code should be **202** with data ``{"message": "Accepted"}``.

        """
    nodes = api.get_nodes()
    cluster_data = {
        "Node[]": [x["node_id"] for x in nodes],
        "Tendrl_context.sds_name": "gluster",
        "Tendrl_context.sds_version": pytest.config.getini("usm_gluster_version")
    }

    job_id = api.import_cluster(cluster_data)["job_id"]

    etcd_api = etcdapi.ApiCommon()
    etcd_api.wait_for_job_status(job_id)

    cluster_id = etcd_api.get_job_attribute(
        cluster_id=job_id, attribute="cluster_id")
    pytest.check([x for x in api.get_cluster_list() if x["cluster_id"] == cluster_id])
    # TODO add test case for checking imported machines


"""@pylatest api/gluster.cluster_import
API-gluster: cluster_import
***************************

.. test_metadata:: author fbalak@redhat.com

Description
===========

Negative import gluster cluster.
"""


def test_cluster_import_invalid():
    """@pylatest api/gluster.cluster_import
        .. test_step:: 1

        Get list of ids of availible nodes.

        .. test_result:: 1

                Server should return response in JSON format:

                        {
                ...
                  {
                  "fqdn": hostname,
                  "machine_id": some_id,
                  "node_id": node_id
                  },
                ...
                        }

                Return code should be **200** with data ``{"message": "OK"}``.

        """
    api = tendrlapi.ApiGluster()
    """@pylatest api/gluster.cluster_import
        .. test_step:: 2

            Send POST request to Tendrl API ``APIURL/GlusterImportCluster

        .. test_result:: 2

            Server should return response in JSON format:

                {
                  "job_id": job_id
                }

            Return code should be **202** with data ``{"message": "Accepted"}``.

        """
    nodes = api.get_nodes()
    cluster_data = {
        "Node[]": ["000000-0000-0000-0000-000000000" for x in nodes],
        "Tendrl_context.sds_name": "gluster",
        "Tendrl_context.sds_version": pytest.config.getini("usm_gluster_version")
    }

    job_id = api.import_cluster(cluster_data)["job_id"]

    # TODO check true response code of etcd (should be some kind of error)
    etcd_api = etcdapi.ApiCommon()
    etcd_api.wait_for_job_status(job_id)

    cluster_id = etcd_api.get_job_attribute(
        cluster_id=job_id, attribute="cluster_id")
    pytest.check(not [x for x in api.get_cluster_list() if x["cluster_id"] == cluster_id])
