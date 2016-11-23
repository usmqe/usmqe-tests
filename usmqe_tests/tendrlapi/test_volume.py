"""
REST API test suite - gluster volume
"""
import pytest

import json

import re

from usmqe.api.tendrlapi import tendrlapi
from usmqe.gluster import gluster


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
    nodes = api.call(pattern="/1.0/GetNodeList")
    """@pylatest api/gluster.cluster_import
    	.. test_step:: 2

    		Send POST request to Tendrl API ``APIURL/1.0/GlusterImportCluster

    	.. test_result:: 2

    		Server should return response in JSON format:

    			{
                  "job_id": job_id
    			}

    		Return code should be **202** with data ``{"message": "Accepted"}``.

    	"""
    test_gluster = gluster.GlusterCommon()
    test_gluster.run_on_node(command="volume info")
    post_data = '''{
    "Node[]":["1b5a0ec3-d660-48cb-bc47-897789a5bc6", "32c96426-9cf5-41b9-84ce-a769c2a1a6f8", "887f9263-414e-480a-8026-4e14b48cfa6a", "007d2e7a-8717-488d-8adb-ffcf58fdab01"],
    "Tendrl_context.sds_name": "gluster",
    "Tendrl_context.sds_version": "3.8.3"
    	 }'''
    #print( json.loads(gluster.actions(1)).items())
    #pytest.check( json.loads(gluster.actions(1)).keys() == json.loads(test_string).keys())
    #pytest.check( test.actions(1) == json.loads(expected_response))

"""@pylatest api/gluster.volume_attributes
    API-gluster: volume_attributes
    ******************************

    .. test_metadata:: author fbalak@redhat.com

    Description
    ===========

    Get list of attributes needed to use in cluster volume creation with given cluster_id.
    """

def test_create_volume():
    """@pylatest api/gluster.create_volume
    	API-gluster: create_volume
    	******************************

    	.. test_metadata:: author fbalak@redhat.com

    	Description
    	===========

    	Get list of attributes needed to use in cluster volume creation with given cluster_id.

    	.. test_step:: 1

    		Connect to Tendrl API via POST request to ``APIURL/cluster/:cluster_id/volume/attributes``
    		Where cluster_id is set to 1.

    	.. test_result:: 1

    		Server should return response in JSON format:

    			{
    			  "volname":{
    				"type":"String"
    			  },
    			  "stripe_count":{
    				"type":"Integer"
    			  },
    			  "replica_count":{
    				"type":"Integer"
    			  },
    			  "disperse_count":{
    				"type":"Integer"
    			  },
    			  "redundancy_count":{
    				"type":"Integer"
    			  },
    			  "transport":{
    				"type":"String"
    			  },
    			  "brickdetails":{
    				"type":"list[brick]"
    			  },
    			  "force":{
    				"type":"Boolean"
    			  },
    			  "directory":{
    				"type":"String"
    			  },
    			  "bitrot":{
    				"type":"Boolean"
    			  },
    			  "scrub-frequency":{
    				"type":"Integer"
    			  },
    			  "scrub-throttle":{
    				"type":"Integer"
    			  }
    			}

    		Return code should be **200** with data ``{"message": "OK"}``.
    		"""
    cluster_id = "147cac1f-fc1f-4ffb-9bff-97ccc95cdcf7"
    api = tendrlapi.ApiCommon()
    post_data = '''{
"Volume.volname":"Vol_test",
"Volume.bricks":["dhcp-126-104.lab.eng.brq.redhat.com:/mnt/gluster2","dhcp-126-107.lab.eng.brq.redhat.com:/mnt/gluster2"]
}'''
    response = api.call(pattern="/1.0/{}/GlusterCreateVolume".format(cluster_id), method="POST", json=json.loads(post_data))

    expected_response = 202
    LOGGER.debug("response: %s" % response.status_code)
    pytest.check( response.status_code == expected_response)

    test_gluster = gluster.GlusterCommon()
    vol_name = test_gluster.run_on_node(command="volume info").findtext(".//name")
    LOGGER.debug("res: %s" % vol_name)

    expected_vol_name = "Vol_test"
    pytest.check( vol_name == expected_vol_name)
