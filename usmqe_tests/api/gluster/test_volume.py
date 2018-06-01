"""
REST API test suite - gluster volume
"""
import pytest
from usmqe.api.tendrlapi import glusterapi
from usmqe.gluster import gluster


LOGGER = pytest.get_logger('volume_test', module=True)
"""@pylatest default
Setup
=====
"""

"""@pylatest default
Teardown
========
"""


# TODO create negative test case generator
# http://doc.pytest.org/en/latest/parametrize.html#basic-pytest-generate-tests-example
@pytest.mark.gluster
def test_create_volume_invalid(
        valid_cluster_id,
        invalid_volume_name,
        invalid_volume_configuration,
        valid_session_credentials):
    """@pylatest api/gluster.create_volume_invalid
        API-gluster: create_volume
        ******************************

        .. test_metadata:: author fbalak@redhat.com

        Description
        ===========

        Get list of attributes needed to use in cluster volume creation with given cluster_id.

        .. test_step:: 1

                Connect to Tendrl API via POST request to ``APIURL/:cluster_id/GlusterCreateVolume``
                Where cluster_id is set to predefined value.

                When some attribute is set to None then in request json is set to ``null``.
                e.g. {
                    "Volume.replica_count": "2",
                    "Volume.bricks": null,
                    "Volume.volname": "Volume_invalid",
                    "Volume.force": true}

        .. test_result:: 1

                Server should return response in JSON format:

                Return code should be **202** with data ``{"message": "Accepted"}``.
                job should fail.
                """

    api = glusterapi.TendrlApiGluster(auth=valid_session_credentials)

    job_id = api.create_volume(
        valid_cluster_id,
        invalid_volume_configuration)["job_id"]
    # TODO check correctly server response or etcd job status
    api.wait_for_job_status(
            job_id,
            status="failed")


@pytest.mark.gluster
def test_stop_volume_invalid(
        valid_cluster_id,
        invalid_volume_name,
        valid_session_credentials):
    """@pylatest api/gluster.stop_volume_invalid
        API-gluster: stop_volume
        ******************************

        .. test_metadata:: author fbalak@redhat.com

        Description
        ===========

        Try to stop volume with given name and cluster id via API.

        .. test_step:: 1

                Connect to Tendrl API via POST request to ``APIURL/:cluster_id/GlusterStopVolume``
                Where cluster_id is set to predefined value.

        .. test_result:: 1

                Server should return response in JSON format:

                Return code should be **202** with data ``{"message": "Accepted"}``.
                Job should fail.
                """

    api = glusterapi.TendrlApiGluster(auth=valid_session_credentials)
    volume_data = {
        "Volume.volname": invalid_volume_name,
    }

    job_id = api.stop_volume(valid_cluster_id, volume_data)["job_id"]
    # TODO check correctly server response or etcd job status
    api.wait_for_job_status(
            job_id,
            status="failed")


# TODO create negative test case generator
# http://doc.pytest.org/en/latest/parametrize.html#basic-pytest-generate-tests-example
@pytest.mark.gluster
def test_start_volume_invalid(
        valid_cluster_id,
        invalid_volume_name,
        valid_session_credentials):
    """@pylatest api/gluster.start_volume_invalid
        API-gluster: start_volume
        ******************************

        .. test_metadata:: author fbalak@redhat.com

        Description
        ===========

        Try to start volume with given name and cluster id via API.

        .. test_step:: 1

                Connect to Tendrl API via POST request to ``APIURL/:cluster_id/GlusterStartVolume``
                Where cluster_id is set to predefined value.

        .. test_result:: 1

                Server should return response in JSON format:

                Return code should be **202** with data ``{"message": "Accepted"}``.
                job should fail.
                """

    api = glusterapi.TendrlApiGluster(auth=valid_session_credentials)
    volume_data = {
        "Volume.volname": invalid_volume_name
    }

    job_id = api.start_volume(valid_cluster_id, volume_data)["job_id"]
    # TODO check correctly server response or etcd job status
    api.wait_for_job_status(
        job_id,
        status="failed")


@pytest.mark.gluster
def test_delete_volume_invalid(
        valid_cluster_id,
        invalid_volume_id,
        valid_session_credentials):
    """@pylatest api/gluster.delete_volume
        API-gluster: delete_volume
        ******************************

        .. test_metadata:: author fbalak@redhat.com

        Description
        ===========

        Delete gluster volume ``Vol_test`` via API.

        .. test_step:: 1

                Connect to Tendrl API via POST request to ``APIURL/:cluster_id/GlusterDeleteVolume``
                Where cluster_id is set to predefined value.

        .. test_result:: 1

                Server should return response in JSON format:

                Return code should be **202** with data ``{"message": "Accepted"}``.
                job should fail.
                """

    api = glusterapi.TendrlApiGluster(auth=valid_session_credentials)
    volume_data = {
        "Volume.volname": valid_cluster_id,
        "Volume.vol_id": invalid_volume_id
    }

    job_id = api.delete_volume(valid_cluster_id, volume_data)["job_id"]
    # TODO check correctly server response or etcd job status
    api.wait_for_job_status(
            job_id,
            status="failed")


@pytest.mark.happypath
@pytest.mark.testready
@pytest.mark.gluster
def test_volumes_list(
        valid_session_credentials,
        cluster_reuse,
        valid_trusted_pool_reuse):
    """@pylatest api/gluster.volumes_list
        API-gluster: volumes_list
        ******************************

        .. test_metadata:: author dahorak@redhat.com

        Description
        ===========

        List volumes for given cluster via API.

        .. test_step:: 1

                Connect to Tendrl API via GET request to ``APIURL/:cluster_id/volumes``
                Where cluster_id is set to predefined value.

        .. test_result:: 1

                Server should return response in JSON format:

                Return code should be **200** with data ``{"volumes": [{...}, ...]}``.
                """

    api = glusterapi.TendrlApiGluster(auth=valid_session_credentials)
    glv_cmd = gluster.GlusterVolume()

    # list of volumes from Tendrl api
    t_volumes = api.get_volume_list(cluster_reuse['cluster_id'])
    t_volume_names = [volume["name"] for volume in t_volumes["volumes"]]
    t_volume_names.sort()
    # list of volumes from Gluster command output
    g_volume_names = glv_cmd.get_volume_names()
    g_volume_names.sort()

    LOGGER.info("list of volumes from Tendrl api: %s", str(t_volume_names))
    LOGGER.info("list of volumes from gluster: %s", g_volume_names)
    pytest.check(
        t_volume_names == g_volume_names,
        "List of volumes from Gluster should be the same as from Tendrl API.")
