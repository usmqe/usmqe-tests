
"""
REST API test suite - gluster cluster
"""
import pytest
import json

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


def test_cluster_import_valid(valid_session_credentials):
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
    api = glusterapi.TendrlApiGluster(auth=valid_session_credentials)
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
    nodes = api.get_nodes()
    for cluster in nodes["clusters"]:
        if cluster["sds_name"] == "gluster":
            node_ids = cluster["node_ids"]
            break
    node_fqdns = []
    msg = "`sds_pkg_name` of node {} should be `gluster`, it is {}"
    for node in nodes["nodes"]:
        if node["node_id"] in node_ids:
            pytest.check(node["detectedcluster"]["sds_pkg_name"] == "gluster",
                         msg.format(node["fqdn"], node["detectedcluster"]["sds_pkg_name"]))
            node_fqdns.append(node["fqdn"])
    trusted_pool = storage.get_hosts_from_trusted_pool(node_fqdns[0])
    node_ids = [x["node_id"] for x in nodes["nodes"] if x["fqdn"] in trusted_pool]
    pytest.check(
        len(trusted_pool) == len(node_ids),
        "number of nodes in trusted pool ({}) should correspond \
        with number of imported nodes ({})".format(len(trusted_pool), len(node_ids)))

    job_id = api.import_gluster_cluster(node_ids)["job_id"]

    api.wait_for_job_status(job_id)

    integration_id = api.get_job_attribute(
        job_id=job_id,
        attribute="TendrlContext.integration_id",
        section="parameters")
    LOGGER.debug("integration_id: %s" % integration_id)

    imported_cluster = [x for x in api.get_cluster_list() if x["integration_id"] == integration_id]
    pytest.check(
        imported_cluster is not None,
        "Job list integration_id '{}' should be present in cluster list.".format(integration_id))
    # TODO add test case for checking imported machines
    msg = "In tendrl should be a same machines as from `gluster peer status` command ({})"
    pytest.check(
        [x[0]["fqdn"] in trusted_pool for x in imported_cluster["nodes"].items()],
        msg.format(trusted_pool))


"""@pylatest api/gluster.cluster_import
API-gluster: cluster_import
***************************

.. test_metadata:: author fbalak@redhat.com

Description
===========

Negative import gluster cluster.
"""


@pytest.mark.parametrize("cluster_data,asserts", [
    ({
        "node_ids": ["000000-0000-0000-0000-000000000"],
        "sds_type": "gluster"
    }, {
            "json": json.loads('{"errors": "Node 000000-0000-0000-0000-000000000 not found"}'),
            "cookies": None,
            "ok": False,
            "reason": 'Unprocessable Entity',
            "status": 422,
        })])
def test_cluster_import_invalid(valid_session_credentials, cluster_data, asserts):
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
    api = glusterapi.TendrlApiGluster(auth=valid_session_credentials)
    """@pylatest api/gluster.cluster_import
        .. test_step:: 2

            Send POST request to Tendrl API ``APIURL/GlusterImportCluster

        .. test_result:: 2

            Server should return response in JSON format with message set in
            ``asserts`` test parameter.

        """
    api.import_cluster(cluster_data, asserts_in=asserts)
