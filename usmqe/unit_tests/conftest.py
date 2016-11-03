# -*- coding: utf8 -*-
"""
Top level conftest.py file of usmqe unit tests.
"""


import pytest


# only really essential and hardwired plugins needs to be there
pytest_plugins = ('plugin.log_assert')
