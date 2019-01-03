# -*- coding: utf-8 -*-
import pytest
import time

from usmqe.usmscheduler import Scheduler
import usmqe.usmssh as usmssh
from usmqe.usmqeconfig import UsmConfig

LOGGER = pytest.get_logger('scheduler', module=True)

def test_scheduler_workflow():
    conf = UsmConfig()
    nodes = conf.inventory.get_groups_dict()["gluster_servers"]
    scheduler = Scheduler(nodes)
    scheduler.run_at("echo '1' > /tmp/test_task")
    jobs = scheduler.jobs()
    LOGGER.info("Jobs: {}".format(jobs))
    assert len(jobs) == len(nodes)
    time.sleep(60)
    for node in nodes:
        SSH = usmssh.get_ssh()
        _, message, _ = SSH[node].run("cat /tmp/test_task")
        assert message.decode("utf-8").rstrip("\n") == "1"
