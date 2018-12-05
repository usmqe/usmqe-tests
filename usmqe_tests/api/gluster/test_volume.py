"""
REST API test suite - gluster volume
"""
import pytest
from usmqe.api.tendrlapi import glusterapi
from usmqe.gluster import gluster


LOGGER = pytest.get_logger('volume_test', module=True)


@pytest.mark.author("dahorak@redhat.com")
@pytest.mark.happypath
@pytest.mark.testready
@pytest.mark.gluster
def test_volumes_list(
        valid_session_credentials,
        cluster_reuse,
        valid_trusted_pool_reuse):
    """
    List volumes for given cluster via API.

    :step:
      Connect to Tendrl API via GET request to ``APIURL/:cluster_id/volumes``
      Where cluster_id is set to predefined value.
    :result:
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


@pytest.mark.author("dahorak@redhat.com")
@pytest.mark.happypath
@pytest.mark.testready
@pytest.mark.gluster
def test_volume_brick_list(
        valid_session_credentials,
        cluster_reuse,
        valid_trusted_pool_reuse):
    """
    List bricks for given volume via API.

    :step:
      Connect to Tendrl API via GET request to
      ``APIURL/:cluster_id/volumes/:volume_id/bricks``
      Where cluster_id is set to predefined value.
    :result:
      Server should return response in JSON format:
      Return code should be **200** with data ``{"bricks": [{...}, ...]}``.
    """

    # get list of volumes from Tendrl
    api = glusterapi.TendrlApiGluster(auth=valid_session_credentials)
    t_volumes = api.get_volume_list(cluster_reuse['cluster_id'])

    # perform brick list test for each volume
    for t_volume in t_volumes["volumes"]:
        LOGGER.info("Compare bricks for volume: %s", t_volume["name"])
        gl_volume = gluster.GlusterVolume(volume_name=t_volume["name"])
        gl_volume.info()

        t_bricks = api.get_brick_list(cluster_reuse['cluster_id'], t_volume["vol_id"])
        t_brick_list = {brick["brick_path"] for brick in t_bricks["bricks"]}

        g_brick_list = set(gl_volume.bricks)

        LOGGER.info("list of bricks for '%s' from Tendrl api: %s",
                    t_volume["name"], str(t_brick_list))
        LOGGER.info("list of bricks for '%s' from gluster: %s",
                    t_volume["name"], g_brick_list)
        pytest.check(
            t_brick_list == g_brick_list,
            "List of bricks for '{}' from Tendrl API should be the same "
            "as from Gluster.".format(t_volume["name"]))
