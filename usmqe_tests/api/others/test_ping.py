"""
REST API test suite - ping
"""
import pytest

from usmqe.api.tendrlapi.common import TendrlApi


"""@pylatest default
Setup
=====
"""

"""@pylatest default
Teardown
========
"""


@pytest.mark.stable
def test_ping():
    """@pylatest api/ping
    API: ping
    **********************

    .. test_metadata:: author fbalak@redhat.com

    Description
    ===========

    Positive ping test.
    """
    test = TendrlApi()
    # TODO(fbalak): add valid returned json to docstring and test them
    """@pylatest api/common.ping_valid
    .. test_step:: 1

        Call USM API via GET request with pattern ``APIURL/ping``.

    .. test_result:: 1

        Return code should be **200** with data ``{"status": "OK"}``.
    """
    test.ping()
