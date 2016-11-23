=====================================
 Overview of the directory structure
=====================================

This document contains a brief overview of repository structure of all USM QE
repositories.

usmqe-tests
===========

Upstream: https://github.com/Tendrl/usmqe-tests

This is a main repository, there are the following top level directories:

* ``docs``: documentation (sphinx) of usmqe integration tests and it's setup
  (you are reading it right now)
* ``conf``: configuration files, only examples are commited in the repository
* ``plugin``: custom pytest plugins
* ``usmqe``: main usmqe python module
* ``usmqe_tests``: usmqe tests code (uses pytest framework)

In the root dir of the repository, there are also:

* main pytest ``conftest.py`` file with core configuration of the pytest
  framework (for running tests cases from ``usmqe_tests`` directory)
* ``tox.ini`` and ``setup.py`` (for testing the usmqe module itself, see
  details on unit tests of ``usmqe`` module below)

usmqe-setup
===========

Upstream: https://github.com/Tendrl/usmqe-setup

This repository contains ansible setup automation.
