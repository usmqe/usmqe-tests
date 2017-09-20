"""
REST API test suite - gluster volume acceptance tests
"""
import pytest

from usmqe.api.tendrlapi import glusterapi
from usmqe.gluster import gluster


LOGGER = pytest.get_logger('volume_crud_test', module=True)
"""@pylatest default
Setup
=====
"""

"""@pylatest default
Teardown
========
"""

VOLUME_NAME = "CrudTestVolume3"


@pytest.mark.gluster_volume_crud
def test_create_volume_valid(
        cluster_reuse,
        valid_session_credentials,
        valid_bricks_for_crud_volume,
        volume_conf_2rep):
    """@pylatest api/gluster.create_volume_valid
        API-gluster: create_volume
        ******************************

        .. test_metadata:: author fbalak@redhat.com
        .. test_metadata:: author mkudlej@redhat.com

        Description
        ===========

        Get list of attributes needed to use in cluster volume creation with given cluster_id.

        .. test_step:: 1

                Connect to Tendrl API via POST request to ``APIURL/:cluster_id/GlusterCreateVolume``
                Where cluster_id is set to predefined value.

        .. test_result:: 1

                Server should return response in JSON format:

                Return code should be **202** with data ``{"message": "Accepted"}``.
                job should finish.
                """
    volume_conf_2rep["Volume.volname"] = VOLUME_NAME
    api = glusterapi.TendrlApiGluster(auth=valid_session_credentials)

    job_id = api.create_volume(
        cluster_reuse["cluster_id"],
        volume_conf_2rep)["job_id"]
    if api.wait_for_job_status(job_id) == "finished":
        """@pylatest api/gluster.create_volume
            API-gluster: create_volume
            ******************************

            .. test_metadata:: author fbalak@redhat.com
            .. test_metadata:: author mkudlej@redhat.com

            Description
            ===========

            Check if there is created volume on gluster nodes via CLI.

            .. test_step:: 2

                Connect to gluster node machine via ssh and run
                ``gluster volume info command``

            .. test_result:: 2

                There should be listed gluster volume named ``Vol_test``.

                """
        storage = gluster.GlusterCommon()
        storage.find_volume_name(VOLUME_NAME)

        volume = gluster.GlusterVolume(VOLUME_NAME)
        volume_id = volume.get_volume_id()
        volumes = api.get_volume_list(cluster_reuse["cluster_id"])
        volume_tendrl = [volume_t[volume_id] for volume_t in volumes
                         if volume_id in volume_t]
        pytest.check(
            len(volume_tendrl) == 1,
            """There should be only one volume
            with id == {}""".format(volume_id))

        if len(volume_tendrl) == 1:
            volume_tendrl = volume_tendrl[0]
            for (x, y, z) in [
                 ("name", volume.name, volume_tendrl["name"]),
                 ("id", volume.id, volume_tendrl["vol_id"]),
                 ("status", volume.status, volume_tendrl["status"]),
                 ("stripe_count", volume.stripe_count, volume_tendrl["stripe_count"]),
                 ("replica_count", volume.replica_count, volume_tendrl["replica_count"]),
                 ("brick_count", volume.brick_count, volume_tendrl["brick_count"]),
                 ("snapshot_count", volume.snap_count, volume_tendrl["snap_count"])]:
                pytest.check(
                    y == z,
                    """Volume {} in storage {} and in Tendrl {} are the same.""".format(x, y, z))


# @pytest.mark.gluster_volume_crud
# def test_stop_volume_valid(
#         cluster_reuse,
#         valid_session_credentials):
#     """@pylatest api/gluster.stop_volume_valid
#         API-gluster: stop_volume
#         ******************************
#
#         .. test_metadata:: author fbalak@redhat.com
#
#         Description
#         ===========
#
#         Try to stop volume with given name and cluster id via API.
#
#         .. test_step:: 1
#
#                 Connect to Tendrl API via POST request to ``APIURL/:cluster_id/GlusterStopVolume``
#                 Where cluster_id is set to predefined value.
#
#         .. test_result:: 1
#
#                 Server should return response in JSON format:
#
#                 Return code should be **202** with data ``{"message": "Accepted"}``.
#                 job should finish.
#                 """
#
#     api = glusterapi.TendrlApiGluster(auth=valid_session_credentials)
#     volume_id = gluster.GlusterVolume(VOLUME_NAME).get_volume_id()
#     volume_data = {
#         "Volume.vol_id": volume_id,
#         "Volume.volname": VOLUME_NAME,
#
#     }
#
#     job_id = api.stop_volume(cluster_reuse["cluster_id"], volume_data)["job_id"]
#     api.wait_for_job_status(job_id)
#     volume = gluster.GlusterVolume(VOLUME_NAME)
#     volume.check_status("Stopped")
#     status = api.get_volume_list(cluster_reuse["cluster_id"])[0][volume_id]["status"]
#     pytest.check(
#         status == "Stopped",
#         "Status from API is {}, should be 'Stopped'".format(status),
#         issue="https://github.com/Tendrl/tendrl-api/issues/56")
#
#
# @pytest.mark.gluster_volume_crud
# def test_start_volume_valid(
#         cluster_reuse,
#         valid_session_credentials):
#     """@pylatest api/gluster.start_volume_valid
#         API-gluster: start_volume
#         ******************************
#
#         .. test_metadata:: author fbalak@redhat.com
#
#         Description
#         ===========
#
#         Try to start volume with given name and cluster id via API.
#
#         .. test_step:: 1
#
#                 Connect to Tendrl API via POST request to
#                 ``APIURL/:cluster_id/GlusterStartVolume``
#                 Where cluster_id is set to predefined value.
#
#         .. test_result:: 1
#
#                 Server should return response in JSON format:
#
#                 Return code should be **202** with data ``{"message": "Accepted"}``.
#                 job should finish.
#                 """
#
#     api = glusterapi.TendrlApiGluster(auth=valid_session_credentials)
#     volume_id = gluster.GlusterVolume(VOLUME_NAME).get_volume_id()
#     volume_data = {
#         "Volume.vol_id": volume_id,
#         "Volume.volname": VOLUME_NAME,
#     }
#
#     job_id = api.start_volume(cluster_reuse["cluster_id"], volume_data)["job_id"]
#     api.wait_for_job_status(job_id)
#     volume = gluster.GlusterVolume(VOLUME_NAME)
#     volume.check_status("Started")
#     status = api.get_volume_list(cluster_reuse["cluster_id"])[0][volume_id]["status"]
#     pytest.check(
#         status == "Started",
#         "Status from API is {}, should be 'Started'".format(status),
#         issue="https://github.com/Tendrl/tendrl-api/issues/55")
#

@pytest.mark.gluster_volume_crud
def test_delete_volume_valid(
        cluster_reuse,
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
                job should finish.
                """

    api = glusterapi.TendrlApiGluster(auth=valid_session_credentials)
    volume_id = gluster.GlusterVolume(VOLUME_NAME).get_volume_id()
    volume_data = {
        "Volume.volname": VOLUME_NAME,
        "Volume.vol_id": volume_id
    }

    job_id = api.delete_volume(cluster_reuse["cluster_id"], volume_data)["job_id"]
    api.wait_for_job_status(
        job_id)
    """@pylatest api/gluster.create_volume
        API-gluster: create_volume
        ******************************

        .. test_metadata:: author fbalak@redhat.com

        Description
        ===========

        Check if there is deleted volume on gluster nodes via CLI.

        .. test_step:: 1

            Connect to gluster node machine via ssh and run
            ``gluster volume info command``

        .. test_result:: 1

            There should not be listed gluster volume named ``Vol_test``.

            """
    storage = gluster.GlusterCommon()
    storage.find_volume_name(VOLUME_NAME, False)
    """@pylatest api/gluster.create_volume
        API-gluster: create_volume
        ******************************

        .. test_metadata:: author fbalak@redhat.com

        Description
        ===========

        Check if there is not deleted volume on gluster nodes via CLI.

        .. test_step:: 3

            Get response from ``hostname/api/1.0/:cluster_id:/GetVolumeList``
            API call.

        .. test_result:: 3

            In response should not be listed gluster volume with ``valid_volume_id``

            """
    volumes = api.get_volume_list(cluster_reuse["cluster_id"])
    pytest.check(
        volume_id not in list(volumes),
        "volume id {} should not be among volume ids in tendrl: {}".format(
            volume_id, list(volumes)))
