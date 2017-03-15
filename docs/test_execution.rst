.. _test-execution-label:

================
 Test Execution
================

This document provides description and examples of integration test execution.

NOTE: Because of commit `Improve the error handling`_, error in the test is catched in mrglog statistics. However there could be a discrepancy with pytest results. If the error/exception originates from the test method code and there is no failed check, pytest says the test ``FAILED`` at the same time mrlog evaluates the result of the test as ``ERROR``.

.. _`Improve the error handling`: https://github.com/Tendrl/usmqe-tests/commit/ef0a30eb5f68f9e32f898b02b0d473dec666660a


Requirements
============

USM QE Tests are executed under ``usmqe`` user account on QE Server machine,
so we expect that:

* QE Server machine has beed deployed as described in :ref:`qe-server-label`
* machines for Tendrl/Ceph/Gluster have beed deployed as described in
  :ref:`test-enviroment-label`
* configuration of USM QE tests has been done as explained in
  :ref:`config-before-testrun-label`


How to run the tests
====================

TODO: add all the details


Examples
========

TODO: provide few examples
