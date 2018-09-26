# Dummy setup.py file for tox to be happy enough to run unit tests.
# It's actually not used for installation or anything else.

from setuptools import setup

setup(setup_requires=["setuptools_scm>=3.0.0"], use_scm_version=True)
