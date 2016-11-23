"""
REST API test suite - gluster volume
"""
import pytest

import json

import re

from usmqe.gluster import gluster


"""@pylatest default
Setup
=====

Further mentioned ``APIURL`` points to: ``http://USMSERVER:8080/api/v1``.
"""

"""@pylatest default
Teardown
========
"""

"""@pylatest api/gluster.volume_actions
API-gluster: volume_actions
***************************

.. test_metadata:: author fbalak@redhat.com

Description
===========

Get list of actions available to cluster volume with given cluster_id.
"""
def test_actions_response():
    """@pylatest api/gluster.volume_actions
    	.. test_step:: 1

    		Connect to Tendrl API via GET request to ``APIURL/cluster/:cluster_id/volume/actions``
    		Where cluster_id is set to 1.

    	.. test_result:: 1

    		Server should return response in JSON format:

    			{
    			  "info":{
    				"type":"get"
    				"url":"/cluster/:cluster_id/volume/:volume_id/info",
    				"method":"GET"
    			  },
    			  "create":{
    				"type":"create",
    				"url":"/cluster/:cluster_id/volume/create",
    				"method":"POST"
    			  },
    			  "start":{
    				"type":"action",
    				"url":"/cluster/:cluster_id/volume/:volume_id/start",
    				"method":"PUT"
    			  },
    			  "stop":{
    				"type":"action",
    				"url":"/cluster/:cluster_id/volume/:volume_id/stop",
    				"method":"PUT"
    			  },
    			  "remove_brick":{
    				"type":"action",
    				"url":"/cluster/:cluster_id/volume/:volume_id/remove_brick",
    				"method":"DELETE"
    			  },
    			  "replace_brick":{
    				"type":"action",
    				"url":"/cluster/:cluster_id/volume/:volume_id/replace_brick",
    				"method":"PUT"
    			  }
    			}

    		Return code should be **200** with data ``{"message": "OK"}``.

    	"""
    test = gluster.GlusterVolume()
    expected_response = '''{
    	   "info":{
    		 "type":"get",
    		 "url":"/cluster/:cluster_id/volume/:volume_id/info",
    		 "method":"GET"
    	   },
    	   "create":{
    		 "type":"create",
    		 "url":"/cluster/:cluster_id/volume/create",
    		 "method":"POST"
    	   },
    	   "start":{
    		 "type":"action",
    		 "url":"/cluster/:cluster_id/volume/:volume_id/start",
    		 "method":"PUT"
    	   },
    	   "stop":{
    		 "type":"action",
    		 "url":"/cluster/:cluster_id/volume/:volume_id/stop",
    		 "method":"PUT"
    	   },
    	   "remove_brick":{
    		 "type":"action",
    		 "url":"/cluster/:cluster_id/volume/:volume_id/remove_brick",
    		 "method":"DELETE"
    	   },
    	   "replace_brick":{
    		 "type":"action",
    		 "url":"/cluster/:cluster_id/volume/:volume_id/replace_brick",
    		 "method":"PUT"
    	   }
    	 }'''
    #print( json.loads(gluster.actions(1)).items())
    #pytest.check( json.loads(gluster.actions(1)).keys() == json.loads(test_string).keys())
    pytest.check( test.actions(1) == json.loads(expected_response))

"""@pylatest api/gluster.volume_attributes
    API-gluster: volume_attributes
    ******************************

    .. test_metadata:: author fbalak@redhat.com

    Description
    ===========

    Get list of attributes needed to use in cluster volume creation with given cluster_id.
    """

def test_attributes_response(self):
    """@pylatest api/gluster.volume_attributes
    	API-gluster-volume: attributes
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
    gluster = tendrl_gluster.Gluster()
    expected_response = '''{
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
    		}'''
    print(gluster.attributes(1))
    pytest.check( gluster.attributes(1) == json.loads(expected_response))


# @pytest.mark.xfail(reason='proste proto')
def test_create_volume():
    """@pylatest api/gluster.create_volume
    API-gluster: create_volume
    **********************

    .. test_metadata:: author fbalak@redhat.com

    Description
    ===========

    Positive gluster volume test. Tests if there is created volume on gluster
    node after api call.
    """
    test = gluster.GlusterVolume()
    """@pylatest api/gluster.create_volume
    .. test_step:: 1

        Connect to gluster node via ssh and run api command to create volume:

        {
            volname: 'Volume 1',
            stripe_count: 1,
            replica_count: 3,
            disperse_count: 3
        }

    .. test_result:: 1

        Api server should return response:
        {
            "job_id":new_job_id,
            "status":"processing",
            "sds_nvr":"gluster-3.8.3",
            "action":"create",
            "object_type":"volume"
        }
    """

    """@pylatest api/gluster.create_volume
    .. test_step:: 2

        Run ``gluster volume status all`` command on target machine.

    .. test_result:: 2

        There should be listed 2 bricks with mount points on /mnt/gluster.
    """

    result = test.info()
    pytest.check( bool(re.search("^Status: Started"), result) )

# @pytest.mark.xfail(reason='proste proto')
def test_create_brick():
    """@pylatest api/gluster.create_brick
    API-gluster: create_brick
    **********************

    .. test_metadata:: author fbalak@redhat.com

    Description
    ===========

    Positive gluster brick test. Tests if there is brick on gluster node.
    """
    test = gluster.GlusterVolume()

    """@pylatest api/gluster.create_brick
    .. test_step:: 1

        Run ``gluster volume info`` command on target machine.

    .. test_result:: 1

        There should be listed 2 bricks with mount points on /mnt/gluster.
    """

    result = test.info()
    pytest.check( bool(re.search("^Brick2"), result) )


# @pytest.mark.xfail(reason='proste proto')
def test_volume_start():
    """@pylatest api/gluster.volume_start
    API-gluster: volume_start
    **********************

    .. test_metadata:: author fbalak@redhat.com

    Description
    ===========

    Positive test for gluster volume startup.
    """
    test = gluster.GlusterVolume()

    """@pylatest api/gluster.volume_start
    .. test_step:: 1

        Run ``gluster volume info`` command on target machine.

    .. test_result:: 1

        There should be volume ``Volume 1`` with listed 2 bricks with mount
        points on /mnt/gluster.
    """
    pytest.check( bool(re.search("Volume 1"), result) )

# @pytest.mark.xfail(reason='proste proto')
def test_volume_delete():
    """@pylatest api/gluster.volume_delete
    API-gluster: volume_start
    **********************

    .. test_metadata:: author fbalak@redhat.com

    Description
    ===========

    Positive test for gluster volume removal.
    """
    test = gluster.GlusterVolume()

    """@pylatest api/gluster.volume_delete
    .. test_step:: 1

        Call api method for for removing gluster volume.

    .. test_result:: 1

        There should be message: `` ``
    """

    """@pylatest api/gluster.volume_delete
    .. test_step:: 2

        Run ``gluster volume info`` command on target machine.

    .. test_result:: 2

        There should be message: ``No volumes present``
    """
    pytest.check( bool(re.search("No volumes present"), result) )

# @pytest.mark.xfail(reason='proste proto')
def test_volume_remove_brick():
    """@pylatest api/gluster.volume_remove_brick
    API-gluster: volume_start
    **********************

    .. test_metadata:: author fbalak@redhat.com

    Description
    ===========

    Positive test for removing gluster brick
    """
    test = gluster.GlusterVolume()

    """@pylatest api/gluster.volume_remove_brick
    .. test_step:: 1

        Call api method for removing gluster brick from volume.

    .. test_result:: 1

        There should be message: `` ``
    """

    """@pylatest api/gluster.volume_delete
    .. test_step:: 2

        Run ``gluster volume info`` command on target machine.

    .. test_result:: 2

        There should be listed Brick1
    """
    pytest.check( bool(re.search("^Brick1"), result) )

    """@pylatest api/gluster.volume_delete
    .. test_step:: 3

        Run ``gluster volume info`` command on target machine.

    .. test_result:: 3

        There shouldn't be listed Brick2
    """
    pytest.check( not bool(re.search("^Brick2"), result) )

# @pytest.mark.xfail(reason='proste proto')
def test_volume_replace_brick():
    """@pylatest api/gluster.volume_replace_brick
    API-gluster: volume_replace_brick
    **********************

    .. test_metadata:: author fbalak@redhat.com

    Description
    ===========

    Positive test for replacing gluster volume startup.
    """
    test = gluster.GlusterVolume()

    """@pylatest api/gluster.volume_remove_brick
    .. test_step:: 1

        Call api method for removing gluster brick from volume.

    .. test_result:: 1

        There should be message: `` ``
    """

    """@pylatest api/gluster.volume_delete
    .. test_step:: 2

        Run ``gluster volume info`` command on target machine.

    .. test_result:: 2

        There should be listed
    """
    pytest.check( bool(re.search(""), result) )

# @pytest.mark.xfail(reason='proste proto')
def test_peer_probe():
    """@pylatest api/gluster.peer_probe
    API-gluster: peer_probe
    **********************

    .. test_metadata:: author fbalak@redhat.com

    Description
    ===========

    Positive test for gluster peer probe.
    """
    test = gluster.GlusterVolume()

    """@pylatest api/gluster.peer_probe
    .. test_step:: 1

        Run ``gluster peer status`` command on target machine.

    .. test_result:: 1

        On first line there should be "Number of Peers: 1"
    """
    pytest.check( bool(re.search("^Number of Peers: 1"), result) )

# @pytest.mark.xfail(reason='proste proto')
def test_peer_detach():
    """@pylatest api/gluster.peer_detach
    API-gluster: peer_detach
    **********************

    .. test_metadata:: author fbalak@redhat.com

    Description
    ===========

    Positive test for gluster peer detach.
    """
    test = gluster.GlusterVolume()

    """@pylatest api/gluster.volume_start
    .. test_step:: 1

        Run ``gluster peer status`` command on target machine.

    .. test_result:: 1

        On first line there should be "Number of Peers: 0"
    """
    pytest.check( bool(re.search("^Number of Peers: 0"), result) )
