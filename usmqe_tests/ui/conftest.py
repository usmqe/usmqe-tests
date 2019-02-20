# -*- coding: utf8 -*-

import time
import pytest

from usmqe.usmqeconfig import UsmConfig
from usmqe.api.tendrlapi import glusterapi
from usmqe.api.tendrlapi.common import login


CONF = UsmConfig()


@pytest.fixture(scope="session")
def imported_cluster_reuse():
    """
    Returns cluster identified by one of machines
    from cluster after importing it into WA.
    """
    auth = login(
        CONF.config["usmqe"]["username"],
        CONF.config["usmqe"]["password"])
    api = glusterapi.TendrlApiGluster(auth=auth)
    id_hostname = CONF.config["usmqe"]["cluster_member"]
    for _ in range(12):
        clusters = api.get_cluster_list()
        clusters = [cluster for cluster in clusters
                    if id_hostname in
                    [node["fqdn"] for node in cluster["nodes"]]
                    ]
        if len(clusters) == 1:
            test_cluster = clusters[0]
        time.sleep(5)
    cluster_id = test_cluster["cluster_id"]
    if test_cluster["is_managed"] != "yes":
        job_id = api.import_cluster(cluster_id, profiling="enable")["job_id"]
        api.wait_for_job_status(job_id)
    clusters = api.get_cluster_list()
    clusters = [cluster for cluster in clusters
                if id_hostname in
                [node["fqdn"] for node in cluster["nodes"]]
                ]
    yield clusters[0]
    job_id = api.unmanage_cluster(cluster_id)["job_id"]
    api.wait_for_job_status(job_id)
    time.sleep(30)
