"""
REST API test suite - Ceph pool
"""
import pytest

from usmqe.api.tendrlapi import cephapi
from usmqe.ceph import ceph_cluster

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
        API-ceph: create_pool
        ******************************

        :authors:
            - fbalak@redhat.com
            - mkudlej@redhat.com

        Description
        ===========
        Negative Create from CRUD for pools.

        .. test_step:: 1

                Connect to Tendrl API via POST request
                to ``APIURL/:cluster_id/CephCreatePool``
                Where cluster_id is set to predefined value.

        .. test_result:: 1

                Server should return response in JSON format:

                Return code should be **202** with data
                ``{"message": "Accepted"}``.
                Job should fail.
                """

    api = cephapi.TendrlApiCeph(auth=valid_session_credentials)

    job_id = api.create_pool(valid_cluster_id,
                             invalid_pool_name,
                             invalid_pg_num,
                             invalid_minsize,
                             invalid_size)
    LOGGER.info("Create pool job_id: {}".format(job_id))
    # TODO check correctly server response or etcd job status
    api.wait_for_job_status(job_id["job_id"], status="failed")


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
        Positive Create and Read from CRUD for pools.

        .. test_step:: 1

                Connect to Tendrl API via POST request
                to ``APIURL/:cluster_id/CephCreatePool``
                Where cluster_id is set to predefined value.

        .. test_result:: 1

                Server should return response in JSON format:

                Return code should be **202** with data
                ``{"message": "Accepted"}``.
                job should finish.
                """

    api = cephapi.TendrlApiCeph(auth=valid_session_credentials)

    job_id = api.create_pool(valid_cluster_id,
                             valid_pool_name,
                             valid_pg_num,
                             valid_minsize,
                             valid_size)["job_id"]
    LOGGER.info("Create pool job_id: {}".format(job_id))
    api.wait_for_job_status(job_id)
    """@pylatest api/ceph.create_pool_valid
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
            ``ceph --format json --cluster *clustername* osd pool ls detail``

        .. test_result:: 2

            There should be listed ceph pool named ``valid_pool_name``.

            """
# TODO get proper cluster name from configuration
    storage = ceph_cluster.CephCluster(pytest.config.getini("usm_ceph_cl_name"))
    pools = storage.osd.pool_ls(detail=True)
    LOGGER.info("List of Ceph pools:{}".format(pools))
    selected_pools = [pool for pool in pools
                      if pool["pool_name"] == valid_pool_name
                      ]
    pytest.check(len(selected_pools) == 1,
                 "Pool {} should be created in Ceph cluster {}.".format(
                    valid_pool_name,
                    pytest.config.getini("usm_ceph_cl_name"))
                 )

    """@pylatest api/ceph.create_pool_valid
        API-ceph: create_pool
        ******************************

        :authors:
            - fbalak@redhat.com
            - mkudlej@redhat.com

        Description
        ===========

        Check if there is created pool in ceph cluster via API.

        .. test_step:: 3

            Connect to Tendrl API via GET request
            to ``APIURL/:cluster_id/CephPoolList``
            Where cluster_id is set to predefined value.

        .. test_result:: 3

            There should be listed ceph pool named ``valid_pool_name``.

            """

    if len(selected_pools) == 1:
        pool = selected_pools[0]
        storage_pool_attributes = {
            "erasure_code_profile": pool["erasure_code_profile"],
            "min_size": pool["min_size"],
            "percent_used": "0",  # newly created pool
            "pg_num": pool["pg_num"],
            "pool_id": pool["auid"],
            "pool_name": pool["pool_name"],
            "quota_enabled":
                pool["quota_max_bytes"] == 0 and
                pool["quota_max_objects"] == 0,
            "quota_max_bytes": pool["quota_max_bytes"],
            "quota_max_objects": pool["quota_max_objects"],
            "size": pool["size"],
            "type": "replicated" if pool["type"] == 1 else "ecpool",  # TODO
            "used": "0"  # newly created pool
            }

        pool_tendrl = [pool_t for pool_t in api.get_pool_list(valid_cluster_id)
                       if pool_t["pool_name"] == valid_pool_name
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

# # TODO This testcase is useless with current API because there is no
# # function to get pool according its name or ID
# def test_read_pool_invalid(valid_cluster_id,
#         invalid_pool_id,
#         valid_session_credentials):
#     """@pylatest api/ceph.read_pool_invalid
#         API-ceph: read_pool
#         ******************************
#
#         :authors:
#             - fbalak@redhat.com
#             - mkudlej@redhat.com
#
#         Description
#         ===========
#         Negative Read from CRUD for pools.
#
#         Check if there is not pool in Ceph cluster via API.
#
#         .. test_step:: 1
#
#             Connect to Tendrl API via GET request to ``APIURL/:cluster_id/CephPoolList``
#             Where cluster_id is set to predefined value.
#
#         .. test_result:: 1
#
#             There should not be listed ceph pool named ``invalid_pool_name``.
#
#             """
#
#     pools = api.get_pool_list(valid_cluster_id)


def test_update_pool_invalid(valid_cluster_id,
                             valid_pool_id,
                             valid_session_credentials,
                             invalid_pool_name,
                             invalid_size,
                             invalid_minsize,
                             invalid_pg_num):
    # TODO add quota support
    """@pylatest api/ceph.update_pool_invalid
        API-ceph: update_pool
        ******************************

        :authors:
            - fbalak@redhat.com
            - mkudlej@redhat.com

        Description
        ===========
        Negative Update from CRUD for pools.

        Update existing pool with invalid data via API.

        .. test_step:: 1

            Connect to Tendrl API via GET request
            to ``APIURL/:cluster_id/CephUpdatePool``
            Where cluster_id is set to predefined value.

        .. test_result:: 1

           Update should be declined.
            """

    api = cephapi.TendrlApiCeph(auth=valid_session_credentials)
    job_id = api.update_pool(valid_cluster_id, valid_pool_id,
                             invalid_pool_name, invalid_size, invalid_minsize,
                             invalid_pg_num)["job_id"]
    api.wait_for_job_status(job_id, status="failed")


def test_update_pool_name_valid(valid_cluster_id,
                                valid_pool_id,
                                valid_session_credentials,
                                valid_pool_name):
    """@pylatest api/ceph.update_pool_name_valid
        API-ceph: update_pool
        ******************************

        :authors:
            - fbalak@redhat.com
            - mkudlej@redhat.com

        Description
        ===========
        Negative Update from CRUD for pools.

        Update existing pool with valid pool name via API.

        .. test_step:: 1

            Connect to Tendrl API via GET request
            to ``APIURL/:cluster_id/CephUpdatePool``
            Where cluster_id is set to predefined value.

        .. test_result:: 1

           Update job should pass.
            """
    valid_pool_name = valid_pool_name + "_updated"
    api = cephapi.TendrlApiCeph(auth=valid_session_credentials)
    job_id = api.update_pool(valid_cluster_id, valid_pool_id,
                             valid_pool_name)["job_id"]
    api.wait_for_job_status(
        job_id,
        issue="https://github.com/Tendrl/ceph-integration/issues/225"
    )
    """@pylatest api/ceph.update_pool_name_valid
        API-ceph: update_pool
        ******************************

        :authors:
            - fbalak@redhat.com
            - mkudlej@redhat.com

        .. test_step:: 2

            Check if changes are made in Ceph pool.

        .. test_result:: 2

           Updates are done in pool.
            """

    storage = ceph_cluster.CephCluster(pytest.config.getini("usm_ceph_cl_name"))
    pools = storage.osd.pool_ls(detail=True)
    LOGGER.info("List of Ceph pools:{}".format(pools))
    selected_pools = [pool for pool in pools
                      if pool["pool_name"] == valid_pool_name
                      ]
    pytest.check(len(selected_pools) == 1,
                 "Pool {} should be updated in Ceph cluster {}.".format(
                    valid_pool_name,
                    pytest.config.getini("usm_ceph_cl_name")),
                 issue="https://github.com/Tendrl/ceph-integration/issues/225"
                 )


def test_update_pool_valid(valid_cluster_id,
                           valid_pool_id,
                           valid_session_credentials,
                           valid_pool_name,
                           valid_size,
                           valid_minsize,
                           valid_pg_num):
    # TODO add quota support
    """@pylatest api/ceph.update_pool_valid
        API-ceph: update_pool
        ******************************

        :authors:
            - fbalak@redhat.com
            - mkudlej@redhat.com

        Description
        ===========
        Negative Update from CRUD for pools.

        Update existing pool with valid data via API.

        .. test_step:: 1

            Connect to Tendrl API via GET request
            to ``APIURL/:cluster_id/CephUpdatePool``
            Where cluster_id is set to predefined value.

        .. test_result:: 1

           Update job should pass.
            """
    valid_pool_name = valid_pool_name + "_updated"
    valid_size = valid_size + 1
    valid_minsize = valid_minsize + 1
    valid_pg_num = valid_pg_num * 2
    api = cephapi.TendrlApiCeph(auth=valid_session_credentials)
    job_id = api.update_pool(valid_cluster_id, valid_pool_id,
                             size=valid_size, min_size=valid_minsize,
                             pg_num=valid_pg_num)["job_id"]
    api.wait_for_job_status(
        job_id,
        issue="https://github.com/Tendrl/ceph-integration/issues/225"
        )
    """@pylatest api/ceph.update_pool_valid
        API-ceph: update_pool
        ******************************

        :authors:
            - fbalak@redhat.com
            - mkudlej@redhat.com

        .. test_step:: 2

            Check if changes are made in Ceph pool.

        .. test_result:: 2

           Pool is updated.
            """

    storage = ceph_cluster.CephCluster(pytest.config.getini("usm_ceph_cl_name"))
    pools = storage.osd.pool_ls(detail=True)
    LOGGER.info("List of Ceph pools:{}".format(pools))
    selected_pools = [pool for pool in pools
                      if pool["pool_name"] == valid_pool_name
                      ]
    pytest.check(len(selected_pools) == 1,
                 "Pool {} should be updated in Ceph cluster {}.".format(
                    valid_pool_name,
                    pytest.config.getini("usm_ceph_cl_name")),
                 issue="https://github.com/Tendrl/ceph-integration/issues/225"
                 )

    """@pylatest api/ceph.update_pool_valid
        API-ceph: update_pool
        ******************************

        :authors:
            - fbalak@redhat.com
            - mkudlej@redhat.com

        Description
        ===========

        Check if there is updated pool in ceph cluster via API.

        .. test_step:: 3

            Connect to Tendrl API via GET request
            to ``APIURL/:cluster_id/CephPoolList``
            Where cluster_id is set to predefined value.

        .. test_result:: 3

            There should be listed ceph pool named ``valid_pool_name``.

            """

    if len(selected_pools) == 1:
        pool = selected_pools[0]
        storage_pool_attributes = {
            "erasure_code_profile": pool["erasure_code_profile"],
            "min_size": pool["min_size"],
            "percent_used": "0",  # newly created pool
            "pg_num": pool["pg_num"],
            "pool_id": pool["auid"],
            "pool_name": pool["pool_name"],
            "quota_enabled":
                pool["quota_max_bytes"] == 0 and
                pool["quota_max_objects"] == 0,
            "quota_max_bytes": pool["quota_max_bytes"],
            "quota_max_objects": pool["quota_max_objects"],
            "size": pool["size"],
            "type": "replicated" if pool["type"] == 1 else "ecpool",  # TODO
            "used": "0"  # newly created pool
            }

        pool_tendrl = [pool_t for pool_t in api.get_pool_list(valid_cluster_id)
                       if pool_t["pool_name"] == valid_pool_name
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


def test_delete_pool_invalid(
        valid_cluster_id,
        invalid_pool_id,
        valid_session_credentials):
    """@pylatest api/ceph.delete_pool_invalid
        API-ceph: delete_pool
        ******************************

        :authors:
            - fbalak@redhat.com
            - mkudlej@redhat.com

        Description
        ===========
        Negative Delete from CRUD for pools.

        Delete ceph pool ``invalid_pool_id`` via API.

        .. test_step:: 1

                Connect to Tendrl API via DELETE request
                to ``APIURL/:cluster_id/CephDeletePool``
                Where cluster_id is set to predefined value.

        .. test_result:: 1

                Server should return response in JSON format:

                Return code should be **200** with data ``{"job_id":"_id_"}``.
                And then joib should fail.
                """

    api = cephapi.TendrlApiCeph(auth=valid_session_credentials)
    job_id = api.delete_pool(valid_cluster_id, invalid_pool_id)["job_id"]
    api.wait_for_job_status(job_id, status="failed")


def test_delete_pool_valid(
        valid_cluster_id,
        valid_pool_id,
        valid_session_credentials):

    api = cephapi.TendrlApiCeph(auth=valid_session_credentials)
    """@pylatest api/ceph.delete_pool
        API-ceph: delete_pool
        ******************************

        :authors:
            - fbalak@redhat.com
            - mkudlej@redhat.com

        Description
        ===========

        Get pool name from API because it was changed in *update* test.

        .. test_step:: 1

            Connect to Tendrl API via GET request
            to ``APIURL/:cluster_id/CephPoolList``
            Where cluster_id is set to predefined value.

        .. test_result:: 1

            There should be listed ceph pool with id == ``valid_pool_id``.

            """

    api_pool_name = [list(pool_t.values())[0]["pool_name"]
                     for pool_t in api.get_pool_list(valid_cluster_id)
                     if "1" in pool_t.keys()
                     ][0]
    """@pylatest api/ceph.delete_pool
        API-ceph: delete_pool
        ******************************

        :authors:
            - fbalak@redhat.com
            - mkudlej@redhat.com

        Description
        ===========
        Positive Delete from CRUD for pools.

        Delete ceph pool ``valid_pool_id`` via API.

        .. test_step:: 2

                Connect to Tendrl API via POST request
                to ``APIURL/:cluster_id/CephDeletePool``
                Where cluster_id is set to predefined value.

        .. test_result:: 2

                Server should return response in JSON format:

                Return code should be **200** with data ``{"job_id":"_id_"}``.
                And then job should finish.
                """

    job_id = api.delete_pool(valid_cluster_id, valid_pool_id)["job_id"]
    LOGGER.info("Delete pool job_id: {}".format(job_id))
    api.wait_for_job_status(job_id, issue="https://github.com/Tendrl/ceph-integration/issues/224")
    """@pylatest api/ceph.delete_pool
        API-ceph: delete_pool
        ******************************

        :authors:
            - fbalak@redhat.com
            - mkudlej@redhat.com

        Description
        ===========

        Check if there is not deleted pool in ceph cluster via CLI.

        .. test_step:: 3

            Connect to ceph monitor machine via ssh and run
            ``ceph --cluster *clustername* pool status``

        .. test_result:: 3

            There should not be listed ceph pool named ``api_pool_name``.

            """
    storage = ceph_cluster.CephCluster(pytest.config.getini("usm_ceph_cl_name"))
    pytest.check(api_pool_name not in storage.osd.pool_ls(),
                 "Pool {} should not be in Ceph \
                 cluster {} after deletion.".format(
                     api_pool_name,
                     pytest.config.getini("usm_ceph_cl_name")),
                 issue="https://github.com/Tendrl/ceph-integration/issues/224"
                 )
