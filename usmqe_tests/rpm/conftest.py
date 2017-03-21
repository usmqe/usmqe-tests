# -*- coding: utf8 -*-

import pytest
import requests


@pytest.fixture
def rpm_repo():
    """
    Check if we can connect to the repo. If not, this issue will be immediately
    reported during setup so that the test case will end up in ERROR state
    (instead of FAILED if we were checking this during test itself).
    """
    baseurl = pytest.config.getini("usm_rpm_baseurl")
    reg = requests.get(baseurl)
    pytest.check(reg.status_code == 200)
    return baseurl
