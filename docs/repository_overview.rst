=================================
 Overview of USM QE repositories
=================================

This document contains a brief overview of structure and purpose of all USM QE
repositories.

usmqe-tests
===========

Upstream: https://github.com/usmqe/usmqe-tests

This repository is most important, because it contains python code of automated
integration test cases. There are the following top level directories:

* ``docs``: sphinx based documentation of usmqe integration tests and it's
  setup (you are reading it right now)
* ``conf``: configuration files, only examples are commited in the repository
* ``plugin``: custom pytest plugins
* ``usmqe``: main usmqe python module
* ``usmqe_tests``: usmqe tests code (uses pytest framework)

In the root dir of the repository, there are also:

* main pytest ``conftest.py`` file with core configuration of the pytest
  framework (for running tests cases from ``usmqe_tests`` directory)
* ``tox.ini`` and ``setup.py`` (for testing the usmqe module itself, see
  :ref:`unit-tests-label` for details)

usmqe-testdoc
=============

Upstream: https://github.com/usmqe/usmqe-testdoc

Here you find description of usmqe testing strategy, environment and test
cases.

usmqe-setup
===========

Upstream: https://github.com/usmqe/usmqe-setup

This repository contains ansible setup automation.

usmqe-centos-ci
===============

Upstream: https://github.com/usmqe/usmqe-centos-ci

Machine deployment for Tendrl project in CentOS CI.
