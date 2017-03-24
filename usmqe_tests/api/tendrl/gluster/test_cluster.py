
"""
REST API test suite - gluster cluster
"""
import pytest

from usmqe.api.tendrlapi import glusterapi
from usmqe.gluster import gluster


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


def test_cluster_import_valid(valid_access_credentials):
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
    api = glusterapi.TendrlApiGluster()
    storage = gluster.GlusterCommon()
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
    nodes = api.get_nodes(valid_access_credentials)
    trusted_pool = storage.get_hosts_from_trusted_pool(nodes["nodes"][0]["fqdn"])
    node_ids = [x["node_id"] for x in nodes["nodes"] if x["fqdn"] in trusted_pool]
    pytest.check(
        len(trusted_pool) == len(node_ids),
        "number of nodes in trusted pool ({}) should correspond \
        with number of imported nodes ({})".format(len(trusted_pool), len(node_ids)))
    cluster_data = {
        "node_ids": node_ids,
        "sds_type": "gluster",
    }

    job_id = api.import_cluster(cluster_data, valid_access_credentials)["job_id"]

    api.wait_for_job_status(job_id, valid_access_credentials)

    integration_id = api.get_job_attribute(
        valid_access_credentials, job_id=job_id, attribute="integration_id", section="parameters")
    LOGGER.debug("integration_id: %s" % integration_id)

    pytest.check(
        [x for x in api.get_cluster_list() if x["integration_id"] == integration_id],
        "Job list integration_id '{}' should be present in cluster list.".format(integration_id))
    # TODO add test case for checking imported machines


"""@pylatest api/gluster.cluster_import
API-gluster: cluster_import
***************************

.. test_metadata:: author fbalak@redhat.com

Description
===========

Negative import gluster cluster.
"""


def test_cluster_import_invalid(valid_access_credentials):
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
    api = glusterapi.TendrlApiGluster()
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
    nodes = api.get_nodes(valid_access_credentials)
    cluster_data = {
        "node_ids": ["000000-0000-0000-0000-000000000" for x in nodes],
        "sds_type": "gluster"
    }

    job_id = api.import_cluster(cluster_data, valid_access_credentials)["job_id"]

    # TODO check true response code of etcd (should be some kind of error)
    api.wait_for_job_status(
        valid_access_credentials,
        job_id,
        status="failed",
        issue="https://github.com/Tendrl/tendrl-api/issues/33")

    integration_id = api.get_job_attribute(
        valid_access_credentials,
        job_id=job_id,
        attribute="integration_id")
    pytest.check(
        not [x for x in api.get_cluster_list() if x["integration_id"] == integration_id],
        "Job list integration_id '{}' should be present in cluster list.".format(integration_id))
