"""
REST API test suite - gluster brick
"""
import pytest
import os.path
from usmqe.api.tendrlapi import glusterapi
import usmqe.usmssh as usmssh


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
        valid_brick_name,
        valid_devices,
        valid_session_credentials):
    """@pylatest api/gluster.create_brick_valid
        API-gluster: create_brick
        ******************************

        .. test_metadata:: author fbalak@redhat.com

        Description
        ===========

        Create ``GlusterCreateBrick`` job with a ``valid_brick_name`` on specified
        ``valid_device`` with nodes from cluster with ``valid_cluster_id``

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

    job_id = api.create_bricks(
        valid_cluster_id,
        nodes,
        valid_devices,
        valid_brick_name
        )["job_id"]
    api.wait_for_job_status(job_id)
    """@pylatest api/gluster.create_brick_valid
        API-gluster: create_brick
        ******************************

        .. test_metadata:: author fbalak@redhat.com

        Description
        ===========

        Check if the bricks were created on hosts of cluster with ``valid_cluster_id``.

        .. test_step:: 2

                Via ssh check on cluster nodes that there exists directory with called
                ``valid_brick_name`` in `/tendrl_gluster_bricks/brick_mount`:
                    [ -d /tendrl_gluster_bricks/brick_mount/``valid_brick_name`` ] && echo "exists"

        .. test_result:: 2

                There should be string ``exists`` in output of ssh.
                """
    brick_path = "/tendrl_gluster_bricks/brick_mount/{}".format(valid_brick_name)
    SSH = usmssh.get_ssh()
    pytest.check(
        len(nodes) > 0,
        "In cluster have to be at least one node. There are {}".format(len(nodes)))
    cmd_fs = 'mount | grep $(df  --output=source {} | tail -1)'.format(brick_path)
    expected_output = '{} type xfs (rw,relatime,seclabel,attr2,inode64,noquota)'.format(brick_path)
    for x in nodes:
        pytest.check(
            os.path.isdir(brick_path),
            "{} should be a directory.".format(
                brick_path))

        """@pylatest api/gluster.create_brick_valid
            API-gluster: create_brick
            ******************************

            .. test_metadata:: author fbalak@redhat.com

            Description
            ===========

            Check if the bricks have ``xfs`` filesystem and set correct device.

            .. test_step:: 3

                    Via ssh check filesystem and deviceof directory with
                    ``valid_brick_path``:
                        mount | grep $(df  --output=source ``valid_brick_path`` | tail -1)

            .. test_result:: 3

                    Output of the command should be:
                        ``device`` type xfs (rw,relatime,seclabel,attr2,inode64,noquota)
                    """
        _, output, _ = SSH[nodes[x]["fqdn"]].run(cmd_fs)
        output = str(output).strip("'b\\n")
        pytest.check(
            output == expected_output,
            "Output of command {} should be `{}`. Output is: `{}`".format(
                cmd_fs, expected_output, output))
