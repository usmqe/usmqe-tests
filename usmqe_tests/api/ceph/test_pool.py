"""
REST API test suite - Ceph pool
"""
import pytest

from usmqe.api.tendrlapi import cephapi
from usmqe.ceph import ceph

LOGGER = pytest.get_logger('test_pool', module=True)
"""@pylatest default
Setup
=====
There is Ceph cluster where pools can be managed.
"""

"""@pylatest default
Teardown
========
"""



# TODO create negative test case generator
# http://doc.pytest.org/en/latest/parametrize.html#basic-pytest-generate-tests-example
def test_create_pool_invalid(
        valid_cluster_id,
        invalid_pool_name,
        invalid_pg_num,
        invalid_minsize,
        invalid_size,
        valid_session_credentials):
    """@pylatest api/ceph.create_pool_invalid
        API-ceph: create_volume
        ******************************

        :authors:
            - fbalak@redhat.com
            - mkudlej@redhat.com

        Description
        ===========

        .. test_step:: 1

                Connect to Tendrl API via POST request to ``APIURL/:cluster_id/CephCreatePool``
                Where cluster_id is set to predefined value.

        .. test_result:: 1

                Server should return response in JSON format:

                Return code should be **202** with data ``{"message": "Accepted"}``.
                job should fail.
                """

    api = cephapi.TendrlApiCeph(auth=valid_session_credentials)

    job_id = api.create_pool(valid_cluster_id,
                             invalid_pool_name,
                             invalid_pg_num,
                             invalid_minsize,
                             invalid_size)["job_id"]
    # TODO check correctly server response or etcd job status
    api.wait_for_job_status(
        job_id,
        status="failed",
        issue="https://github.com/Tendrl/tendrl-api/issues/33")


def test_create_pool_valid(
        valid_cluster_id,
        valid_pool_name,
        valid_pg_num,
        valid_minsize,
        valid_size,
        valid_session_credentials):
    """@pylatest api/ceph.create_pool_valid
        API-ceph: create_pool
        ******************************

        :authors:
            - fbalak@redhat.com
            - mkudlej@redhat.com

        Description
        ===========

        .. test_step:: 1

                Connect to Tendrl API via POST request to ``APIURL/:cluster_id/CephCreatePool``
                Where cluster_id is set to predefined value.

        .. test_result:: 1

                Server should return response in JSON format:

                Return code should be **202** with data ``{"message": "Accepted"}``.
                job should finish.
                """

    api = cephapi.TendrlApiCeph(auth=valid_session_credentials)

    job_id = api.create_volume(valid_cluster_id,
                               valid_pool_name,
                               valid_pg_num,
                               valid_minsize,
                               valid_size)["job_id"]
    api.wait_for_job_status(job_id)
    """@pylatest api/ceph.create_pool
        API-ceph: create_pool
        ******************************

        :authors:
            - fbalak@redhat.com
            - mkudlej@redhat.com

        Description
        ===========

        Check if there is created pool in ceph cluster via CLI.

        .. test_step:: 2

            Connect to ceph monitor machine via ssh and run
            ``ceph --cluster *clustername* pool status``

        .. test_result:: 2

            There should be listed ceph pool named ``test_name``.

            """
    #TODO get proper cluster name from configuration
    storage = ceph.CephCluster("test_name")
    pools = [pool for pool in storage.mon.pool_ls(detail=True)
             if pool["poolname"] == valid_pool_name
            ]
    pytest.check(len(pools) == 1,
                 "Pool {} should be created in Ceph \
                 cluster {}.".format(valid_pool_name, "test_name")
                )

    """@pylatest api/ceph.create_pool
        API-ceph: create_pool
        ******************************

        :authors:
            - fbalak@redhat.com
            - mkudlej@redhat.com

        Description
        ===========

        Check if there is created pool in ceph cluster via API.

        .. test_step:: 3

            Connect to Tendrl API via GET request to ``APIURL/:cluster_id/CephPoolList``
            Where cluster_id is set to predefined value.

        .. test_result:: 3

            There should be listed ceph pool named ``test_name``.

            """
#ceph --format json --cluster test_name osd pool ls detail
#    "auid":0,
#    "cache_min_evict_age":0
#    "cache_min_flush_age":0
#    "cache_mode":"none"
#    "cache_target_dirty_high_ratio_micro":0
#    "cache_target_dirty_ratio_micro":0
#    "cache_target_full_ratio_micro":0
#    "crash_replay_interval":0,
#    "crush_ruleset":0,
#    "erasure_code_profile":""
#    "expected_num_objects":0
#    "fast_read":false
#    "flags":1,
#    "flags_names":"hashpspool",
#    "grade_table":[]
#    "hit_set_count":0
#    "hit_set_grade_decay_rate":0
#    "hit_set_params":{"type":"none"}
#    "hit_set_period":0
#    "hit_set_search_last_n":0
#    "last_change":"1",
#    "last_force_op_resend":"0",
#    "min_read_recency_for_promote":0
#    "min_size":2,
#    "min_write_recency_for_promote":0
#    "object_hash":2,
#    "options":{}
#    "pg_num":64,
#    "pg_placement_num":64,
#    "pool_name":"rbd",
#    "pool_snaps":[]
#    "quota_max_bytes":0
#    "quota_max_objects":0
#    "read_tier":-1
#    "removed_snaps":"[]"
#    "size":3,
#    "snap_epoch":0
#    "snap_mode":"selfmanaged",
#    "snap_seq":0,
#    "stripe_width":0
#    "target_max_bytes":0
#    "target_max_objects":0
#    "tier_of":-1
#    "tiers":[]
#    "type":1,
#    "use_gmt_hitset":true
#    "write_tier":-1

    if len(pools) == 1:
        pool = pools[0]
        storage_pool_attributes = {
            "erasure_code_profile": pool["erasure_code_profile"],
            "min_size": pool["min_size"],
            "percent_used": "0", # newly created pool
            "pg_num": pool["pg_num"],
            "pool_id": pool["auid"],
            "pool_name": pool["pool_name"],
            "quota_enabled": pool["quota_max_bytes"] == 0 and pool["quota_max_objects"] == 0,
            "quota_max_bytes": pool["quota_max_bytes"],
            "quota_max_objects": pool["quota_max_objects"],
            "size": pool["size"],
            "type": "replicated" if pool["type"] == 1 else "ecpool", #TODO
            "used": "0" # newly created pool
            }

        pool_tendrl = [pool for pool in api.get_pool_list(valid_cluster_id)
                       if pool["pool_name"] == valid_pool_name
                      ][0]
        # remove Tendrl specific keys
        pool_tendrl.pop("deleted")
        pool_tendrl.pop("hash")
        pool_tendrl.pop("updated_at")

        pytest.check(
            pool_tendrl == storage_pool_attributes,
            """Storage pool attributes: {}
            Tendrl pool attributes: {}
            These should be the same.""".format(
                pool_tendrl, storage_pool_attributes))


#def test_stop_volume_invalid(
#        valid_cluster_id,
#        invalid_volume_name,
#        valid_session_credentials):
#    """@pylatest api/ceph.stop_volume_invalid
#        API-ceph: stop_volume
#        ******************************
#
#        .. test_metadata:: author fbalak@redhat.com
#
#        Description
#        ===========
#
#        Try to stop volume with given name and cluster id via API.
#
#        .. test_step:: 1
#
#                Connect to Tendrl API via POST request to ``APIURL/:cluster_id/GlusterStopVolume``
#                Where cluster_id is set to predefined value.
#
#        .. test_result:: 1
#
#                Server should return response in JSON format:
#
#                Return code should be **202** with data ``{"message": "Accepted"}``.
#                Job should fail.
#                """
#
#    api = cephapi.TendrlApiGluster(auth=valid_session_credentials)
#    volume_data = {
#        "Volume.volname": invalid_volume_name,
#    }
#
#    job_id = api.stop_volume(valid_cluster_id, volume_data)["job_id"]
#    # TODO check correctly server response or etcd job status
#    api.wait_for_job_status(
#            job_id,
#            status="failed",
#            issue="https://github.com/Tendrl/tendrl-api/issues/33")
#
#
#def test_stop_volume_valid(
#        valid_cluster_id,
#        valid_volume_name,
#        valid_volume_id,
#        valid_session_credentials):
#    """@pylatest api/ceph.stop_volume_valid
#        API-ceph: stop_volume
#        ******************************
#
#        .. test_metadata:: author fbalak@redhat.com
#
#        Description
#        ===========
#
#        Try to stop volume with given name and cluster id via API.
#
#        .. test_step:: 1
#
#                Connect to Tendrl API via POST request to ``APIURL/:cluster_id/GlusterStopVolume``
#                Where cluster_id is set to predefined value.
#
#        .. test_result:: 1
#
#                Server should return response in JSON format:
#
#                Return code should be **202** with data ``{"message": "Accepted"}``.
#                job should finish.
#                """
#
#    api = cephapi.TendrlApiGluster(auth=valid_session_credentials)
#    volume_data = {
#        "Volume.volname": valid_volume_name,
#    }
#
#    job_id = api.stop_volume(valid_cluster_id, volume_data)["job_id"]
#    api.wait_for_job_status(job_id)
#    volume = ceph.GlusterVolume(valid_volume_name)
#    volume.check_status("Stopped")
#    status = api.get_volume_list(valid_cluster_id)[0][valid_volume_id]["status"]
#    pytest.check(
#        status == "Stopped",
#        "Status from API is {}, should be 'Stopped'".format(status),
#        issue="https://github.com/Tendrl/tendrl-api/issues/56")
#
#
## TODO create negative test case generator
## http://doc.pytest.org/en/latest/parametrize.html#basic-pytest-generate-tests-example
#def test_start_volume_invalid(
#        valid_cluster_id,
#        invalid_volume_name,
#        valid_session_credentials):
#    """@pylatest api/ceph.start_volume_invalid
#        API-ceph: start_volume
#        ******************************
#
#        .. test_metadata:: author fbalak@redhat.com
#
#        Description
#        ===========
#
#        Try to start volume with given name and cluster id via API.
#
#        .. test_step:: 1
#
#                Connect to Tendrl API via POST request to ``APIURL/:cluster_id/GlusterStartVolume``
#                Where cluster_id is set to predefined value.
#
#        .. test_result:: 1
#
#                Server should return response in JSON format:
#
#                Return code should be **202** with data ``{"message": "Accepted"}``.
#                job should fail.
#                """
#
#    api = cephapi.TendrlApiGluster(auth=valid_session_credentials)
#    volume_data = {
#        "Volume.volname": invalid_volume_name
#    }
#
#    job_id = api.start_volume(valid_cluster_id, volume_data)["job_id"]
#    # TODO check correctly server response or etcd job status
#    api.wait_for_job_status(
#        job_id,
#        status="failed",
#        issue="https://github.com/Tendrl/tendrl-api/issues/33")
#
#
#def test_start_volume_valid(
#        valid_cluster_id,
#        valid_volume_name,
#        valid_volume_id,
#        valid_session_credentials):
#    """@pylatest api/ceph.start_volume_valid
#        API-ceph: start_volume
#        ******************************
#
#        .. test_metadata:: author fbalak@redhat.com
#
#        Description
#        ===========
#
#        Try to start volume with given name and cluster id via API.
#
#        .. test_step:: 1
#
#                Connect to Tendrl API via POST request to ``APIURL/:cluster_id/GlusterStartVolume``
#                Where cluster_id is set to predefined value.
#
#        .. test_result:: 1
#
#                Server should return response in JSON format:
#
#                Return code should be **202** with data ``{"message": "Accepted"}``.
#                job should finish.
#                """
#
#    api = cephapi.TendrlApiGluster(auth=valid_session_credentials)
#    volume_data = {
#        "Volume.volname": valid_volume_name,
#    }
#
#    job_id = api.start_volume(valid_cluster_id, volume_data)["job_id"]
#    api.wait_for_job_status(job_id)
#    volume = ceph.GlusterVolume(valid_volume_name)
#    volume.check_status("Started")
#    status = api.get_volume_list(valid_cluster_id)[0][valid_volume_id]["status"]
#    pytest.check(
#        status == "Started",
#        "Status from API is {}, should be 'Started'".format(status),
#        issue="https://github.com/Tendrl/tendrl-api/issues/55")
#
#
#def test_delete_volume_invalid(
#        valid_cluster_id,
#        invalid_volume_id,
#        valid_session_credentials):
#    """@pylatest api/ceph.delete_volume
#        API-ceph: delete_volume
#        ******************************
#
#        .. test_metadata:: author fbalak@redhat.com
#
#        Description
#        ===========
#
#        Delete ceph volume ``Vol_test`` via API.
#
#        .. test_step:: 1
#
#                Connect to Tendrl API via POST request to ``APIURL/:cluster_id/GlusterDeleteVolume``
#                Where cluster_id is set to predefined value.
#
#        .. test_result:: 1
#
#                Server should return response in JSON format:
#
#                Return code should be **202** with data ``{"message": "Accepted"}``.
#                job should fail.
#                """
#
#    api = cephapi.TendrlApiGluster(auth=valid_session_credentials)
#    volume_data = {
#        "Volume.volname": valid_cluster_id,
#        "Volume.vol_id": invalid_volume_id
#    }
#
#    job_id = api.delete_volume(valid_cluster_id, volume_data)["job_id"]
#    # TODO check correctly server response or etcd job status
#    api.wait_for_job_status(
#            job_id,
#            status="failed",
#            issue="https://github.com/Tendrl/tendrl-api/issues/33")
#
#
#def test_delete_volume_valid(
#        valid_cluster_id,
#        valid_volume_name,
#        valid_volume_id,
#        valid_session_credentials):
#    """@pylatest api/ceph.delete_volume
#        API-ceph: delete_volume
#        ******************************
#
#        .. test_metadata:: author fbalak@redhat.com
#
#        Description
#        ===========
#
#        Delete ceph volume ``Vol_test`` via API.
#
#        .. test_step:: 1
#
#                Connect to Tendrl API via POST request to ``APIURL/:cluster_id/GlusterDeleteVolume``
#                Where cluster_id is set to predefined value.
#
#        .. test_result:: 1
#
#                Server should return response in JSON format:
#
#                Return code should be **202** with data ``{"message": "Accepted"}``.
#                job should finish.
#                """
#
#    api = cephapi.TendrlApiGluster(auth=valid_session_credentials)
#    volume_data = {
#        "Volume.volname": valid_volume_name,
#        "Volume.vol_id": valid_volume_id
#    }
#
#    job_id = api.delete_volume(valid_cluster_id, volume_data)["job_id"]
#    api.wait_for_job_status(
#        job_id,
#        issue="https://github.com/Tendrl/api/issues/33")
#    """@pylatest api/ceph.create_volume
#        API-ceph: create_volume
#        ******************************
#
#        .. test_metadata:: author fbalak@redhat.com
#
#        Description
#        ===========
#
#        Check if there is created volume on ceph nodes via CLI.
#
#        .. test_step:: 1
#
#            Connect to ceph node machine via ssh and run
#            ``ceph volume info command``
#
#        .. test_result:: 1
#
#            There should be listed ceph volume named ``Vol_test``.
#
#            """
#    storage = ceph.GlusterCommon()
#    storage.find_volume_name(valid_volume_name, False)
#
#    # There should be either deleted attribute or record should be removed from database
#    # https://github.com/Tendrl/api/issues/78
#    #
#    # deleted = api.get_volume_list(valid_cluster_id)[0][valid_volume_id]["deleted"]
#    # pytest.check(
#    #     deleted == "True",
#    #     "deleted attribute should be True, is {}".format(deleted),
#    #     issue="https://github.com/Tendrl/tendrl-api/issues/33")
