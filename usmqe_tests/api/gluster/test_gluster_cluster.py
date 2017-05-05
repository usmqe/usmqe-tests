
"""
REST API test suite - gluster cluster
"""
import pytest
import json

from usmqe.api.tendrlapi import glusterapi


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


def test_cluster_import_valid(valid_session_credentials, valid_trusted_pool):
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

            Server should return response in JSON format:

                {
                  "job_id": job_id
                }

            Return code should be **202**
                with data ``{"message": "Accepted"}``.

        """
    nodes = api.get_nodes()
    node_ids = None
    for cluster in nodes["clusters"]:
        if cluster["sds_name"] == "gluster":
            node_ids = cluster["node_ids"]
            break
    node_fqdns = []
    msg = "`sds_pkg_name` of node {} should be `gluster`, it is {}"
    for node in nodes["nodes"]:
        if node["node_id"] in node_ids:
            pytest.check(node["detectedcluster"]["sds_pkg_name"] == "gluster",
                         msg.format(node["fqdn"],
                         node["detectedcluster"]["sds_pkg_name"]))
            node_fqdns.append(node["fqdn"])
    node_ids = [x["node_id"] for x in nodes["nodes"]
                if x["fqdn"] in valid_trusted_pool]
    pytest.check(
        len(valid_trusted_pool) == len(node_ids),
        "number of nodes in trusted pool ({}) should correspond "
        "with number of imported nodes ({})".format(len(valid_trusted_pool),
                                                    len(node_ids)))

    job_id = api.import_cluster(node_ids)["job_id"]

    api.wait_for_job_status(job_id)

    integration_id = api.get_job_attribute(
        job_id=job_id,
        attribute="TendrlContext.integration_id",
        section="parameters")
    LOGGER.debug("integration_id: %s" % integration_id)

    # TODO(fbalak) remove this sleep after
    #              https://github.com/Tendrl/api/issues/159 is resolved.
    import time
    time.sleep(30)

    imported_clusters = [x for x in api.get_cluster_list()
                         if x["integration_id"] == integration_id]
    pytest.check(
        len(imported_clusters) == 1,
        "Job list integration_id '{}' should be "
        "present in cluster list.".format(integration_id))
    # TODO add test case for checking imported machines
    msg = "In tendrl should be a same machines "\
          "as from `gluster peer status` command ({})"
    LOGGER.debug("debug imported clusters: %s" % imported_clusters)
    pytest.check(
        [x["fqdn"] in valid_trusted_pool
         for x in imported_clusters[0]["nodes"].values()],
        msg.format(valid_trusted_pool))


"""@pylatest api/gluster.cluster_import
API-gluster: cluster_import
***************************

.. test_metadata:: author fbalak@redhat.com

Description
===========

Negative import gluster cluster.
"""


@pytest.mark.parametrize("node_ids,asserts", [
    (["000000-0000-0000-0000-000000000"], {
        "json": json.loads(
            '{"errors": "Node 000000-0000-0000-0000-000000000 not found"}'),
        "cookies": None,
        "ok": False,
        "reason": 'Unprocessable Entity',
        "status": 422,
        })])
def test_cluster_import_invalid(valid_session_credentials, node_ids, asserts):
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
    api.import_cluster(node_ids,  asserts_in=asserts)
