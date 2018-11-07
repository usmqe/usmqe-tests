# -*- coding: utf8 -*-
"""
Top level conftest.py file of usmqe tests project.
"""


import pytest


# list custom usmqe plugins here
pytest_plugins = (
    'plugin.log_assert',
    )
