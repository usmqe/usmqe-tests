# -*- coding: utf8 -*-

import pytest

from usmqe.api.tendrlapi.common import TendrlAuth
from usmqe.usmqeconfig import UsmConfig

CONF = UsmConfig()


@pytest.fixture(
    scope="session",
    params=[
        "",
        None,
        "this_is_invalid_access_token_00000",
        "4e3459381b5b94fcd642fb0ca30eba062fbcc126a47c6280945a3405e018e824",
        ])
def invalid_session_credentials(request):
    """
    Return invalid access (for testing negative use cases), no login or logout
    is performed during setup or teardown.
    """
    username = CONF.config["usmqe"]["username"]
    invalid_token = request.param
    auth = TendrlAuth(token=invalid_token, username=username)
    return auth
