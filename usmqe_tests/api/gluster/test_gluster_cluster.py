
"""
REST API test suite - gluster cluster
"""
import pytest
import time

from usmqe.api.graphiteapi import graphiteapi
from usmqe.api.tendrlapi import glusterapi


LOGGER = pytest.get_logger('cluster_test', module=True)


@pytest.mark.author("fbalak@redhat.com")
@pytest.mark.happypath
@pytest.mark.testready
@pytest.mark.cluster_import_gluster
def test_cluster_import_valid(valid_session_credentials, cluster_reuse, valid_trusted_pool_reuse):
    """
    Positive import gluster cluster.
    """
    """
    :step:
      Check that fqdns of nodes in tendrl correspond with fqdns
      from ``gluster`` command.
    :result:
      Sets of fqdns of nodes in tendrl and from ``gluster`` command
      should be the same.
    """
    api = glusterapi.TendrlApiGluster(auth=valid_session_credentials)
    cluster_id = cluster_reuse["cluster_id"]
    pytest.check(
        cluster_id is not None,
        "Cluster id is: {}".format(cluster_id))
    for _ in range(12):
        cluster = api.get_cluster(cluster_id)
        nodes = [node for node in cluster["nodes"] if node["fqdn"]]
        if len(nodes) == len(valid_trusted_pool_reuse):
            break
        time.sleep(10)
    else:
        pytest.check(
            len(valid_trusted_pool_reuse) == len(cluster["nodes"]),
            "Number of nodes from gluster trusted pool ({}) should be "
            "the same as number of nodes in tendrl ({})".format(len(valid_trusted_pool_reuse),
                                                                len(cluster["nodes"])))
    node_fqdns = [x["fqdn"] for x in nodes]
    pytest.check(
        set(valid_trusted_pool_reuse) == set(node_fqdns),
        "fqdns get from gluster trusted pool ({}) should correspond "
        "with fqdns of nodes in tendrl ({})".format(valid_trusted_pool_reuse,
                                                    node_fqdns))

    """
    :step:
      Send POST request to Tendrl API ``APIURL/clusters/:cluster_id/import``
    :result:
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


@pytest.mark.author("fbalak@redhat.com")
@pytest.mark.gluster
@pytest.mark.negative
@pytest.mark.testready
@pytest.mark.parametrize("cluster_id", [
    "000000-0000-0000-0000-000000000",
    "aaaaaa-aaaa-aaaa-aaaa-aaaaaaaaa",
    "0",
    "0-0",
    "000000-0000--0000-000000000-0000-000-000-0-0-0-000",
    ])
def test_cluster_import_invalid(valid_session_credentials, cluster_id):
    """
    Negative import gluster cluster.
    """
    api = glusterapi.TendrlApiGluster(auth=valid_session_credentials)
    """
    :step:
      Create import cluster job via API with invalid cluster id.
    :result:
      API respons with 404 error, no job id is returned.
    """
    asserts = {
        "ok": False,
        "reason": 'Not Found',
        "status": 404,
        }
    response = api.import_cluster(cluster_id, asserts_in=asserts)
    pytest.check("job_id" not in response, "job id is not returned")
    pytest.check("errors" in response, "there is errors field in response")
    LOGGER.info("errors reported in response: %s", response.get("errors"))


@pytest.mark.author("mbukatov@redhat.com")
@pytest.mark.gluster
@pytest.mark.negative
@pytest.mark.testready
@pytest.mark.parametrize("cluster_id", [
    pytest.param("", marks=pytest.mark.xfail),
    "this is not uuid",
    pytest.param("@#$@#$%!#^#@@", marks=pytest.mark.xfail),
    pytest.param("a"*1000, id="long-cluster-id", marks=pytest.mark.xfail),
    ])
def test_cluster_import_invalid_uuid(valid_session_credentials, cluster_id):
    """
    Negative import gluster cluster using cluster id value which completelly
    breaks criteria for uuid.
    """
    api = glusterapi.TendrlApiGluster(auth=valid_session_credentials)
    """
    :step:
      Create import cluster job via API with broken cluster id.
    :result:
      API returns some error and refuses to process it.
    """
    asserts = {
        "ok": False,
        "status": 400,
        "reason": "Bad Request",
        }
    response = api.import_cluster(cluster_id, asserts_in=asserts)
    pytest.check("job_id" not in response, "job id is not returned")
    pytest.check("errors" in response, "there is errors field in response")
    LOGGER.info("errors reported in response: %s", response.get("errors"))


@pytest.mark.author("mbukatov@redhat.com")
@pytest.mark.gluster
@pytest.mark.negative
@pytest.mark.testready
def test_cluster_import_fail_with_one_nodeagent_down(
        valid_session_credentials,
        cluster_reuse,
        valid_trusted_pool_reuse,
        importfail_setup_nodeagent_stopped_on_one_node):
    """
    Negative import gluster cluster when node agent is not running on one
    storage machine. Import should fail in such case.
    """
    api = glusterapi.TendrlApiGluster(auth=valid_session_credentials)

    # this test can't go on if we don't have proper cluster id at this point
    assert cluster_reuse["cluster_id"] is not None

    # TODO: this comes from test_cluster_import_valid, move this into cluster reuse fixture?
    """
    :step:
      Check that fqdns of nodes in tendrl correspond with fqdns
      from ``gluster`` command.
    :result:
      Sets of fqdns of nodes in tendrl and from ``gluster`` command
      should be the same.
    """
    retry_num = 12
    for i in range(retry_num):
        cluster = api.get_cluster(cluster_reuse["cluster_id"])
        if len(cluster["nodes"]) == len(valid_trusted_pool_reuse):
            LOGGER.debug("cluster (via tendrl API) has expected number of nodes")
            break
        if i != retry_num - 1:
            msg = "cluster (via tendrl API) has unexpected number of nodes, retrying API query"
            LOGGER.info(msg)
            time.sleep(10)
    else:
        assert len(cluster["nodes"]) == len(valid_trusted_pool_reuse)
    node_fqdn_list = [node["fqdn"] for node in cluster["nodes"] if node["fqdn"]]
    assert set(valid_trusted_pool_reuse) == set(node_fqdn_list)

    """
    :step:
      Start import job for the cluster.
    :result:
      The job starts and finishes with failed status after some time.
    """
    LOGGER.info("starting import cluster job")
    import_job = api.import_cluster(cluster_reuse["cluster_id"])
    LOGGER.info(
        "import (job id {}) submited, waiting for completion".format(import_job["job_id"]))
    api.wait_for_job_status(import_job["job_id"], status="failed")

    """
    :step:
      Using integration id from the import job, find cluster we tried to import
      in a cluster list.
    :result:
      There is exactly one such cluster, and it's not managed (aka not imported).
    """
    integration_id = api.get_job_attribute(
        job_id=import_job["job_id"],
        attribute="TendrlContext.integration_id",
        section="parameters")
    LOGGER.debug("integration_id: %s" % integration_id)
    clusters = [x for x in api.get_cluster_list() if x["integration_id"] == integration_id]
    pytest.check(
        len(clusters) == 1,
        "Job list integration_id '{}' should be "
        "present in cluster list.".format(integration_id))
    pytest.check(
        clusters[0]['is_managed'] == 'no',
        'cluster we tried to import should be in unmanaged state')


@pytest.mark.author("fbalak@redhat.com")
@pytest.mark.happypath
@pytest.mark.testready
@pytest.mark.cluster_unmanage_gluster
@pytest.mark.ansible_playbook_setup('test_setup.graphite_access.yml')
@pytest.mark.ansible_playbook_teardown('test_teardown.graphite_access.yml')
def test_cluster_unmanage_valid(
        ansible_playbook,
        valid_session_credentials,
        cluster_reuse,
        valid_trusted_pool_reuse):
    """
    Positive unmanage gluster cluster.
    """
    """
    :step:
      Check that tested cluster is correctly managed by Tendrl.
    :result:
      There is in Tendrl ``"is_managed":"yes"`` for cluster with id [cluster_id].
      Graphite contains data related to health of tested cluster.
    """
    tendrl_api = glusterapi.TendrlApiGluster(auth=valid_session_credentials)
    graphite_api = graphiteapi.GraphiteApi()

    cluster_id = cluster_reuse["cluster_id"]
    pytest.check(
        cluster_id is not None,
        "Cluster id is: {}".format(cluster_id))
    pytest.check(
        cluster_reuse["is_managed"] == "yes",
        "is_managed: {}\nThere should be ``yes``.".format(cluster_reuse["is_managed"]))

    # graphite target uses short name if it is set
    if cluster_reuse["short_name"]:
        cluster_target_id = cluster_reuse["short_name"]
    else:
        cluster_target_id = cluster_reuse["cluster_id"]
    # it takes 15 minutes to refresh data Host status panel
    for i in range(31):
        cluster_health = graphite_api.get_datapoints(
            target="tendrl.clusters.{}.status".format(cluster_target_id))

        if cluster_health:
            break
        else:
            time.sleep(30)
    pytest.check(
        cluster_health,
        """graphite health of cluster {}: {}
        There should be related data.""".format(cluster_id, cluster_health))

    """
    :step:
      Send POST request to Tendrl API ``APIURL/clusters/:cluster_id/unmanage``.
    :result:
      Server should return response in JSON format:

          {
            "job_id": job_id
          }

      Return code should be **202**
          with data ``{"message": "Accepted"}``.
    """
    job_id = tendrl_api.unmanage_cluster(cluster_id)["job_id"]

    tendrl_api.wait_for_job_status(job_id)

    """
    :step:
      Check that tested cluster is correctly managed by Tendrl.
    :result:
      There is in Tendrl ``"is_managed": "no"`` for cluster with id [cluster_id].
      Graphite contains no data related to health of tested cluster.
    """
    # TODO(fbalak) remove this workaround when BZ 1589321 is resolved
    for i in range(15):
        cluster_list = tendrl_api.get_cluster_list()
        if len(cluster_list) > 0:
            break
        else:
            time.sleep(10)
    assert cluster_list
    for cluster in cluster_list:
        if cluster["cluster_id"] == cluster_id:
            unmanaged_cluster = cluster
            break
    pytest.check(
        unmanaged_cluster["is_managed"] == "no",
        "is_managed: {}\nThere should be ``no``.".format(unmanaged_cluster["is_managed"]))

    cluster_health = graphite_api.get_datapoints(
        target="tendrl.clusters.{}.status".format(cluster_target_id))
    pytest.check(
        cluster_health == [],
        """graphite health of cluster {}: `{}`
        There should be `[]`.""".format(cluster_id, cluster_health))

    """
    :step:
      Reimport cluster and check that tested cluster is correctly managed by Tendrl.
    :result:
      There is ``"is_managed": "yes"`` in Tendrl for cluster with id [cluster_id].
    """
    job_id = tendrl_api.import_cluster(cluster_id)["job_id"]
    tendrl_api.wait_for_job_status(job_id)
    for cluster in tendrl_api.get_cluster_list():
        if cluster["cluster_id"] == cluster_id:
            managed_cluster = cluster
            break
    pytest.check(
        managed_cluster["is_managed"] == "yes",
        "is_managed: {}\nThere should be ``yes``.".format(managed_cluster["is_managed"]))
