
"""
REST API test suite - gluster cluster
"""
import pytest
import uuid

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

"""@pylatest api/gluster.cluster_create
API-gluster: cluster_create
***************************

.. test_metadata:: author fbalak@redhat.com

Description
===========

Positive create gluster cluster.
"""


@pytest.mark.parametrize("cluster_name", ["ClusterName"])
@pytest.mark.cluster_create_gluster
def test_cluster_create_valid(
        valid_session_credentials,
        valid_nodes,
        cluster_name):
    api = glusterapi.TendrlApiGluster(auth=valid_session_credentials)
    """@pylatest api/gluster.cluster_import
        .. test_step:: 1

            Send POST request to Tendrl API ``APIURL/GlusterCreateCluster

        .. test_result:: 1

            Server should return response in JSON format:

                {
                  "job_id": job_id
                }

            Return code should be **202**
                with data ``{"message": "Accepted"}``.

        """
    nodes = []
    provisioner_ip = None
    network = pytest.config.getini("usm_network_subnet")
    node_ids = []
    ips = None
    for x in valid_nodes:
        if "tendrl/server" in x["tags"]:
            continue
        for y in x["networks"]:
            if y["subnet"] == network:
                ips = y["ipv4"]
                break
        pytest.check(
            type(ips) == list,
            "type of ip addresses returned from api have to be list,"
            " it is: {}".format(type(ips)))
        pytest.check(
            len(ips) == 1,
            "length of ipv4 addresses list have to be 1, otherwise it is not valid"
            " configuration for this test, it is: {}".format(len(ips)))
        nodes.append({
            "role": "glusterfs/node",
            "ip": ips[0]})
        node_ids.append(x["node_id"])
        if "provisioner/gluster" in x["tags"]:
            provisioner_ip = ips[0]
    LOGGER.debug("node_ips: %s" % nodes)
    LOGGER.debug("provisioner: %s" % provisioner_ip)
    """@pylatest api/gluster.cluster_create
        .. test_step:: 2

        Check if there is at least one gluster node for cluster creation.

        .. test_result:: 2

        Test passes if there is at least one gluster node.
        """
    api = glusterapi.TendrlApiGluster(auth=valid_session_credentials)
    pytest.check(
        len(nodes) > 0,
        "There have to be at least one gluster node."
        "There are {}".format(len(valid_nodes)))
    job_id = api.create_cluster(
        cluster_name,
        str(uuid.uuid4()),
        nodes,
        provisioner_ip,
        network)["job_id"]

    api.wait_for_job_status(job_id)

    integration_id = api.get_job_attribute(
        job_id=job_id,
        attribute="TendrlContext.integration_id",
        section="parameters")
    LOGGER.debug("integration_id: %s" % integration_id)

    api.get_cluster_list()
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

    imported_nodes = imported_clusters[0]["nodes"]
    pytest.check(
        len(imported_nodes) == len(nodes),
        "In cluster should be the same amount of hosts"
        "(is {}) as is in API call for cluster creation."
        "(is {})".format(len(imported_nodes), len(nodes)))

    pytest.check(
        set(node_ids) == set(imported_nodes.keys()),
        "There should be imported these nodes: {}"
        "There are: {}".format(node_ids, imported_nodes.keys()))


"""@pylatest api/gluster.cluster_import
API-gluster: cluster_import
***************************

.. test_metadata:: author fbalak@redhat.com

Description
===========

Positive import gluster cluster.
"""


@pytest.mark.cluster_import_gluster
def test_cluster_import_valid(valid_session_credentials, cluster_reuse, valid_trusted_pool_reuse):
    """@pylatest api/gluster.cluster_import
        .. test_step:: 1

            Check that fqdns of nodes in tendrl correspond with fqdns
            from ``gluster`` command.

        .. test_result:: 1

            Sets of fqdns of nodes in tendrl and from ``gluster`` command
            should be the same.

        """
    api = glusterapi.TendrlApiGluster(auth=valid_session_credentials)
    cluster_id = cluster_reuse["cluster_id"]
    nodes = cluster_reuse["nodes"]
    pytest.check(
        cluster_id is not None,
        "Cluster id is: {}".format(cluster_id))
    node_fqdns = [x["fqdn"] for x in nodes]
    pytest.check(
        set(valid_trusted_pool_reuse) == set(node_fqdns),
        "fqdns get from gluster trusted pool ({}) should correspond "
        "with fqdns of nodes in tendrl ({})".format(valid_trusted_pool_reuse,
                                                    node_fqdns))

    """@pylatest api/gluster.cluster_import
        .. test_step:: 2

            Send POST request to Tendrl API ``APIURL/clusters/:cluster_id/import``

        .. test_result:: 2

            Server should return response in JSON format:

                {
                  "job_id": job_id
                }

            Return code should be **202**
                with data ``{"message": "Accepted"}``.

        """
    job_id = api.import_cluster(cluster_id)["job_id"]

    api.wait_for_job_status(job_id)

    integration_id = api.get_job_attribute(
        job_id=job_id,
        attribute="TendrlContext.integration_id",
        section="parameters")
    LOGGER.debug("integration_id: %s" % integration_id)

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
        [x["fqdn"] in valid_trusted_pool_reuse
         for x in imported_clusters[0]["nodes"]],
        msg.format(valid_trusted_pool_reuse))


"""@pylatest api/gluster.cluster_import
API-gluster: cluster_import
***************************

.. test_metadata:: author fbalak@redhat.com

Description
===========

Negative import gluster cluster.
"""


@pytest.mark.parametrize("cluster_id, status", [
    ("000000-0000-0000-0000-000000000", "failed")])
@pytest.mark.gluster
def test_cluster_import_invalid(valid_session_credentials, cluster_id, status):
    api = glusterapi.TendrlApiGluster(auth=valid_session_credentials)
    """@pylatest api/gluster.cluster_import
        .. test_step:: 1

            Create import cluster job via API with invalid cluster id.

        .. test_result:: 1

            API returns response with json: `{"job_id":job_id}`
        """
    job_id = api.import_cluster(cluster_id)["job_id"]
    """@pylatest api/gluster.cluster_import
        .. test_step:: 2

            Repeatedly check if job with `job_id` from test_step 1 is
            `finished` or `failed`.

        .. test_result:: 2

            Job status should be in status given by `status` parameter.
        """
    api.wait_for_job_status(job_id, status=status)
