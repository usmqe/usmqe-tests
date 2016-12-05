"""
REST API test suite - gluster volume
"""
import pytest

import json

import re

import usmqe

from usmqe.api.tendrlapi import tendrlapi
from usmqe.gluster import gluster
from usmqe.api.etcdapi import etcdapi

@pytest.fixture
def cluster_id():
    api = tendrlapi.ApiCommon()
    response = api.call(pattern="GetClusterList", method="GET")

    expected_response = 200
    pytest.check( response.status_code == expected_response)

    return response.json()[0]["cluster_id"]

@pytest.fixture
def volume_id():
    test_gluster = gluster.GlusterCommon()
    xml = test_gluster.run_on_node(command="volume info")
    vol_name = xml.findtext("./volInfo/volumes/volume/id")

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
    api = tendrlapi.ApiCommon()
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
    response = api.call(pattern="GetNodeList", method="GET")

    expected_response = 200
    LOGGER.debug("response: %s" % response.status_code)
    pytest.check( response.status_code == expected_response)

    nodes = [ x["node_id"] for x in response.json() ]
    post_data = {
        "Node[]": nodes,
        "Tendrl_context.sds_name": "gluster",
        "Tendrl_context.sds_version": "3.8.3"
        }

    response = api.call(pattern="/GlusterImportCluster", method="POST", json=post_data)

    expected_response = 202
    pytest.check( response.status_code == expected_response)

    etcd_api = etcdapi.ApiCommon()
    status = etcd_api.wait_for_job(response.json()["job_id"])
    LOGGER.debug("status: %s" % status)
    pytest.check( status == "finished")

    response = api.call(pattern="GetClusterList", method="GET")

    expected_response = 200
    pytest.check( response.status_code == expected_response)

    pytest.check( response.status_code != None)

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
    api = tendrlapi.ApiCommon()
    bricks = [ "{}:/mnt/gluster".format(x) for x in usmqe.inventory.role2hosts("gluster") ]
    post_data = {
        "Volume.volname":"Vol_test",
        "Volume.bricks":bricks
    }
    response = api.call(pattern="{}/GlusterCreateVolume".format(cluster_id), method="POST", json=post_data)

    expected_response = 202
    LOGGER.debug("post_data: %s" % json.dumps(post_data))
    LOGGER.debug("response: %s" % response.status_code)
    pytest.check( response.status_code == expected_response)

    etcd_api = etcdapi.ApiCommon()
    status = etcd_api.wait_for_job(response.json()["job_id"])
    LOGGER.debug("status: %s" % status)
    pytest.check( status == "finished")
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
    xml = test_gluster.run_on_node(command="volume info")
    vol_name = xml.findtext("./volInfo/volumes/volume/name")
    LOGGER.debug("res: %s" % vol_name)

    expected_vol_name = "Vol_test"
    pytest.check( vol_name == expected_vol_name)

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
    api = tendrlapi.ApiCommon()
    post_data = {
            "Volume.volname":"Vol_test",
            "Volume.vol_id":volume_id
            }
    response = api.call(pattern="{}/GlusterDeleteVolume".format(cluster_id), method="POST", json=post_data)

    expected_response = 202
    LOGGER.debug("post_data: %s" % post_data)
    LOGGER.debug("response: %s" % response.status_code)
    pytest.check( response.status_code == expected_response)

    etcd_api = etcdapi.ApiCommon()
    status = etcd_api.wait_for_job(response.json()["job_id"])
    LOGGER.debug("status: %s" % status)
    pytest.check( status == "finished")
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
    vol_name = test_gluster.run_on_node(command="volume info").findtext("./volInfo/volumes/volume/name")
    LOGGER.debug("res: %s" % vol_name)

    expected_vol_name = "Vol_test"
    pytest.check( vol_name != expected_vol_name)
