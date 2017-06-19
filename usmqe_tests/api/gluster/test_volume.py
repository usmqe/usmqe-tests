"""
REST API test suite - gluster volume
"""
import pytest

from usmqe.api.tendrlapi import glusterapi
from usmqe.gluster import gluster
import usmssh


LOGGER = pytest.get_logger('volume_test', module=True)
"""@pylatest default
Setup
=====
"""

"""@pylatest default
Teardown
========
"""


def test_create_brick_valid(
        valid_cluster_id,
        valid_brick_path,
        valid_session_credentials):
    """@pylatest api/gluster.create_brick_valid
        API-gluster: create_brick
        ******************************

        .. test_metadata:: author fbalak@redhat.com

        Description
        ===========

        Create ``GlusterCreateBrick`` job with a ``valid_brick_path`` with nodes from cluster
        with ``valid_cluster_id``

        .. test_step:: 1

                Connect to Tendrl API via POST request to ``APIURL/:cluster_id/GlusterCreateBrick``
                Where cluster_id is set to predefined value.

        .. test_result:: 1

                Server should return response in JSON format:

                Return code should be **202** with data ``{"message": "Accepted"}``.
                job should finish.
                """
    api = glusterapi.TendrlApiGluster(auth=valid_session_credentials)

    cluster_info = [x for x in api.get_cluster_list()
                    if x["integration_id"] == valid_cluster_id]
    nodes = cluster_info[0]["nodes"]

    job_id = api.create_brick(
        valid_cluster_id,
        nodes,
        valid_brick_path)
    api.wait_for_job_status(job_id)["job_id"]
    """@pylatest api/gluster.create_brick_valid
        API-gluster: create_brick
        ******************************

        .. test_metadata:: author fbalak@redhat.com

        Description
        ===========

        Check if the bricks were created on hosts of cluster with ``valid_cluster_id``.

        .. test_step:: 2

                Via ssh check on cluster nodes that there exists
                directory with ``valid_brick_path``:
                    [ -d ``valid_brick_path`` ] && echo "exists"

        .. test_result:: 2

                There should be string ``exists`` in output of ssh.
                """
    SSH = usmssh.get_ssh()
    pytest.check(
        len(nodes) > 0,
        "In cluster have to be at least one node. There are {}".format(len(nodes)))
    cmd_exists = "[ -d {} ] && echo 'exists'".format(valid_brick_path)
    cmd_fs = "df -T {} | awk '{print [}' | tail -n1]".format(valid_brick_path)
    for x in nodes:
        output = SSH[x["fqdn"]].run(cmd_exists)
        pytest.check(
            output == "exists",
            "Output of command {} should be `exists`. Output is: `{}`".format(
                cmd_exists, output))

        """@pylatest api/gluster.create_brick_valid
            API-gluster: create_brick
            ******************************

            .. test_metadata:: author fbalak@redhat.com

            Description
            ===========

            Check if the bricks have ``xfs`` filesystem.

            .. test_step:: 3

                    Via ssh check filesystem of directory with ``valid_brick_path``:
                        df -T ``valid_brick_path`` | awk '{print [}' | tail -n1]

            .. test_result:: 3

                    There should be string ``xfs`` in output of ssh.
                    """
        output = SSH[x["fqdn"]].run(cmd_fs)
        pytest.check(
            output == "xfs",
            "Output of command {} should be `xfs`. Output is: `{}`".format(
                cmd_fs, output))


# TODO create negative test case generator
# http://doc.pytest.org/en/latest/parametrize.html#basic-pytest-generate-tests-example
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


def test_create_volume_valid(
        valid_cluster_id,
        valid_volume_name,
        valid_volume_configuration,
        valid_session_credentials):
    """@pylatest api/gluster.create_volume_valid
        API-gluster: create_volume
        ******************************

        .. test_metadata:: author fbalak@redhat.com

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

    api = glusterapi.TendrlApiGluster(auth=valid_session_credentials)

    job_id = api.create_volume(
        valid_cluster_id,
        valid_volume_configuration)["job_id"]
    api.wait_for_job_status(job_id)
    """@pylatest api/gluster.create_volume
        API-gluster: create_volume
        ******************************

        .. test_metadata:: author fbalak@redhat.com

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
    storage.find_volume_name(valid_volume_name)

    volume = gluster.GlusterVolume(valid_volume_name)
    volume_id = volume.get_volume_id()
    storage_volume_attributes = {
            "name": volume.name,
            "id": volume.id,
            "status": volume.status,
            "stripe_count": volume.stripe_count,
            "replica_count": volume.replica_count,
            "brick_count": volume.brick_count,
            "snapshot_count": volume.snap_count
        }

    volume_tendrl = api.get_volume_list(valid_cluster_id)[0][volume_id]
    tendrl_volume_attributes = {
            "name": volume_tendrl["name"],
            "id": volume_tendrl["vol_id"],
            "status": volume_tendrl["status"],
            "stripe_count": volume_tendrl["stripe_count"],
            "replica_count": volume_tendrl["replica_count"],
            "brick_count": volume_tendrl["brick_count"],
            "snapshot_count": volume_tendrl["snap_count"]
        }
    pytest.check(
        tendrl_volume_attributes == storage_volume_attributes,
        """Storage volume attributes: {}
        Tendrl volume attributes: {}
        These should be the same.""".format(
            tendrl_volume_attributes, storage_volume_attributes))


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


def test_stop_volume_valid(
        valid_cluster_id,
        valid_volume_name,
        valid_volume_id,
        valid_session_credentials):
    """@pylatest api/gluster.stop_volume_valid
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
                job should finish.
                """

    api = glusterapi.TendrlApiGluster(auth=valid_session_credentials)
    volume_data = {
        "Volume.vol_id": valid_volume_id,
        "Volume.volname": valid_volume_name,

    }

    job_id = api.stop_volume(valid_cluster_id, volume_data)["job_id"]
    api.wait_for_job_status(job_id)
    volume = gluster.GlusterVolume(valid_volume_name)
    volume.check_status("Stopped")
    status = api.get_volume_list(valid_cluster_id)[0][valid_volume_id]["status"]
    pytest.check(
        status == "Stopped",
        "Status from API is {}, should be 'Stopped'".format(status),
        issue="https://github.com/Tendrl/tendrl-api/issues/56")


# TODO create negative test case generator
# http://doc.pytest.org/en/latest/parametrize.html#basic-pytest-generate-tests-example
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


def test_start_volume_valid(
        valid_cluster_id,
        valid_volume_name,
        valid_volume_id,
        valid_session_credentials):
    """@pylatest api/gluster.start_volume_valid
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
                job should finish.
                """

    api = glusterapi.TendrlApiGluster(auth=valid_session_credentials)
    volume_data = {
        "Volume.vol_id": valid_volume_id,
        "Volume.volname": valid_volume_name,
    }

    job_id = api.start_volume(valid_cluster_id, volume_data)["job_id"]
    api.wait_for_job_status(job_id)
    volume = gluster.GlusterVolume(valid_volume_name)
    volume.check_status("Started")
    status = api.get_volume_list(valid_cluster_id)[0][valid_volume_id]["status"]
    pytest.check(
        status == "Started",
        "Status from API is {}, should be 'Started'".format(status),
        issue="https://github.com/Tendrl/tendrl-api/issues/55")


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


def test_delete_volume_valid(
        valid_cluster_id,
        valid_volume_name,
        valid_volume_id,
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
    volume_data = {
        "Volume.volname": valid_volume_name,
        "Volume.vol_id": valid_volume_id
    }

    job_id = api.delete_volume(valid_cluster_id, volume_data)["job_id"]
    api.wait_for_job_status(
        job_id)
    """@pylatest api/gluster.create_volume
        API-gluster: create_volume
        ******************************

        .. test_metadata:: author fbalak@redhat.com

        Description
        ===========

        Check if there is created volume on gluster nodes via CLI.

        .. test_step:: 2

            Connect to gluster node machine via ssh and run
            ``gluster volume info command``

        .. test_result:: 2

            There shouldn't be listed gluster volume named ``Vol_test``.

            """
    storage = gluster.GlusterCommon()
    storage.find_volume_name(valid_volume_name, False)
    """@pylatest api/gluster.create_volume
        API-gluster: create_volume
        ******************************

        .. test_metadata:: author fbalak@redhat.com

        Description
        ===========

        Check if there is created volume on gluster nodes via CLI.

        .. test_step:: 3

            Get response from ``hostname/api/1.0/:cluster_id:/GetVolumeList``
            API call.

        .. test_result:: 3

            In response should not be listed gluster volume with ``valid_volume_id``

            """
    volumes = api.get_volume_list(valid_cluster_id)
    pytest.check(valid_volume_id not in list(volumes[0].keys()),
        "volume id {} should not be among volume ids in tendrl: {}".format(
            valid_volume_id, list(volumes[0].keys())))

    # There should be either deleted attribute or record should be removed from database
    # https://github.com/Tendrl/api/issues/78
    #
    # deleted = api.get_volume_list(valid_cluster_id)[0][valid_volume_id]["deleted"]
    # pytest.check(
    #     deleted == "True",
    #     "deleted attribute should be True, is {}".format(deleted),
    #     issue="https://github.com/Tendrl/tendrl-api/issues/33")
