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
