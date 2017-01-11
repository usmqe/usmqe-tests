"""
REST API test suite - gluster volume
"""
import pytest

from usmqe.api.tendrlapi import tendrlapi
from usmqe.gluster import gluster
from usmqe.api.etcdapi import etcdapi
import usmqe.inventory as inventory


@pytest.fixture
def cluster_id():
    # TODO change
    api = tendrlapi.ApiGluster()
    return api.get_cluster_list()[0]["cluster_id"]


@pytest.fixture
def volume_id():
    # TODO change
    test_gluster = gluster.GlusterCommon()
    xml = test_gluster.run_on_node(command="volume info")
    return xml.findtext("./volInfo/volumes/volume/id")


LOGGER = pytest.get_logger('volume_test', module=True)
"""@pylatest default
Setup
=====
"""

"""@pylatest default
Teardown
========
"""


def test_create_volume_valid(cluster_id):
    """@pylatest api/gluster.create_volume
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
                """
    api = tendrlapi.ApiGluster()

    role = pytest.config.getini("usm_gluster_role")
    try:
        bricks = ["{}:{}".format(x, pytest.config.getini(
            "usm_brick_path")) for x in inventory.role2hosts(role)]
    except TypeError as e:
        print(
            "TypeError({0}): You should probably define usm_brick_path and \
                    usm_gluster_role in usm.ini. {1}".format(
                e.errno,
                e.strerror))

    volume_data = {
        "Volume.volname": pytest.config.getini("usm_volume_name"),
        "Volume.bricks": bricks
    }

    job_id = api.create_volume(cluster_id, volume_data)["job_id"]
    etcd_api = etcdapi.ApiCommon()
    etcd_api.wait_for_job_status(job_id)
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
    test_gluster = gluster.GlusterCommon()
    test_gluster.find_volume_name(pytest.config.getini("usm_volume_name"))

    vol_id = volume_id()
    value = api.get_volume_attribute(cluster_id, vol_id, "name")
    pytest.check(value == pytest.config.getini("usm_volume_name"))


def test_create_volume_invalid(cluster_id):
    """@pylatest api/gluster.create_volume
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
                """
    api = tendrlapi.ApiGluster()

    volume_data = {
        "Volume.volname": None,
        "Volume.bricks": None
    }

    job_id = api.create_volume(cluster_id, volume_data)["job_id"]
    etcd_api = etcdapi.ApiCommon()
    etcd_api.wait_for_job_status(
            job_id,
            status="failed",
            issue="https://github.com/Tendrl/tendrl-api/issues/33")
    # TODO check correctly server response or etcd job status


def test_start_volume_valid(cluster_id):
    api = tendrlapi.ApiGluster()
    volume_data = {
        "Volume.volname": pytest.config.getini("usm_volume_name"),
    }

    job_id = api.start_volume(cluster_id, volume_data)["job_id"]
    etcd_api = etcdapi.ApiCommon()
    etcd_api.wait_for_job_status(job_id)
    test_gluster = gluster.GlusterCommon()
    test_gluster.check_status(pytest.config.getini("usm_volume_name"), "Started")
    value = api.get_volume_attribute(cluster_id, volume_id, "status")
    pytest.check(value == "Started")


def test_start_volume_invalid():
    cluster_id = "incorrect"
    api = tendrlapi.ApiGluster()
    volume_data = {
        "Volume.volname": pytest.config.getini("usm_volume_name"),
    }

    job_id = api.start_volume(cluster_id, volume_data)["job_id"]
    etcd_api = etcdapi.ApiCommon()
    etcd_api.wait_for_job_status(
            job_id,
            status="failed",
            issue="https://github.com/Tendrl/tendrl-api/issues/33")
    # TODO check correctly server response or etcd job status


def test_stop_volume_valid(cluster_id):
    api = tendrlapi.ApiGluster()
    volume_data = {
        "Volume.volname": pytest.config.getini("usm_volume_name"),
    }

    job_id = api.stop_volume(cluster_id, volume_data)["job_id"]
    etcd_api = etcdapi.ApiCommon()
    etcd_api.wait_for_job_status(job_id)
    test_gluster = gluster.GlusterCommon()
    test_gluster.check_status(pytest.config.getini("usm_volume_name"), "Stopped")
    value = api.get_volume_attribute(cluster_id, volume_id, "status")
    pytest.check(value == "Stopped")


def test_stop_volume_invalid():
    cluster_id = "incorrect"
    api = tendrlapi.ApiGluster()
    volume_data = {
        "Volume.volname": pytest.config.getini("usm_volume_name"),
    }

    job_id = api.stop_volume(cluster_id, volume_data)["job_id"]
    etcd_api = etcdapi.ApiCommon()
    etcd_api.wait_for_job_status(
            job_id,
            status="failed",
            issue="https://github.com/Tendrl/tendrl-api/issues/33")
    # TODO check correctly server response or etcd job status


def test_delete_volume_valid(cluster_id, volume_id):
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
                """
    api = tendrlapi.ApiGluster()
    volume_data = {
        "Volume.volname": pytest.config.getini("usm_volume_name"),
        "Volume.vol_id": volume_id
    }

    job_id = api.delete_volume(cluster_id, volume_data)["job_id"]
    etcd_api = etcdapi.ApiCommon()
    etcd_api.wait_for_job_status(job_id)
    """@pylatest api/gluster.create_volume
        API-gluster: create_volume
        ******************************

        .. test_metadata:: author fbalak@redhat.com

        Description
        ===========

        Check if there is created volume on gluster nodes via CLI.

        .. test_step:: 1

            Connect to gluster node machine via ssh and run
            ``gluster volume info command``

        .. test_result:: 1

            There should be listed gluster volume named ``Vol_test``.

            """
    test_gluster = gluster.GlusterCommon()
    test_gluster.find_volume_name(pytest.config.getini("usm_volume_name"), False)
    value = api.get_volume_attribute(cluster_id, volume_id, "deleted")
    pytest.check(value == "True")


def test_delete_volume_invalid(cluster_id, volume_id):
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
                """
    api = tendrlapi.ApiGluster()
    volume_data = {
        "Volume.volname": None,
        "Volume.vol_id": None
    }

    job_id = api.delete_volume(cluster_id, volume_data)["job_id"]
    etcd_api = etcdapi.ApiCommon()
    etcd_api.wait_for_job_status(
            job_id,
            status="failed",
            issue="https://github.com/Tendrl/tendrl-api/issues/33")
    # TODO check correctly server response or etcd job status
