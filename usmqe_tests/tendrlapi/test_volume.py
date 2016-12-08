"""
REST API test suite - gluster volume
"""
import pytest

import json

import re

from usmqe.api.tendrlapi import tendrlapi
from usmqe.gluster import gluster
from usmqe.api.etcdapi import etcdapi
import usmqe.inventory as inventory


@pytest.fixture
def cluster_id():
    api = tendrlapi.ApiGluster()
    return api.get_cluster_list()[0]["cluster_id"]


@pytest.fixture
def volume_id(cluster_id):
    api = tendrlapi.ApiGluster()
    volumes = api.get_volume_list(cluster_id)
    volume_id = False
    for item in volumes:
        if item["name"] == name:
            id = item["vol_id"]
    return volume_id

LOGGER = pytest.get_logger('volume_test', module=True)
"""@pylatest default
Setup
=====

Further mentioned ``APIURL`` points to: ``http://USMSERVER:8080``.
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

Import gluster cluster.
"""


def test_cluster_import():
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
    api = tendrlapi.ApiGluster()
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
    cluster_data = {
        "Node[]": [x["node_id"] for x in nodes],
        "Tendrl_context.sds_name": "gluster",
        "Tendrl_context.sds_version": "3.8.3"
    }

    job_id = api.import_cluster(cluster_data)["job_id"]

    etcd_api = etcdapi.ApiCommon()
    status = etcd_api.wait_for_job(job_id)
    pytest.check(status == "finished")

    cluster_id = etcd_api.get_job_attribute(
        id=job_id, attribute="cluster_id")
    return cluster_id


"""@pylatest api/gluster.volume_attributes
    API-gluster: volume_attributes
    ******************************

    .. test_metadata:: author fbalak@redhat.com

    Description
    ===========

    Get list of attributes needed to use in cluster volume creation with given cluster_id.
    """


def test_create_volume(cluster_id):
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
    except typeError as e:
        print(
            "TypeError({0}): You should probably define usm_brick_path and usm_gluster_role in usm.ini. {1}".format(
                e.errno,
                e.strerror))

    volume_data = {
        "Volume.volname": "Vol_test",
        "Volume.bricks": bricks
    }
    api.create_volume(cluster_id, volume_data)
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
    test_gluster.find_volume_name("Vol_test")


def test_delete_volume(cluster_id, volume_id):
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
    list = api.get_volume_list(cluster_id)
    volume_id = False
    for item in list:
        if item["name"] == name:
            id = item["vol_id"]
    volume_data = {
        "Volume.volname": "Vol_test",
        "Volume.vol_id": volume_id
    }
    api.delete_volume(cluster_id, volume_data)

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
    test_gluster.find_volume_name("Vol_test", False)
