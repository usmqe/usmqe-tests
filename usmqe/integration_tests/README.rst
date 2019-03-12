===================================
 Integration Tests of usmqe module
===================================

This directory is not a python module. It contains integration tests (written
in pytest framework) of ``usmqe`` module using specific parts of framework.

It is preferred to put tests of this module that require configurated access
to storage node or access to global configuration (via `UsmConfig` class)
into this directory.

Usage
=====

Tests in this directory are executed the same way as `Tendrl integration tests`_.


.. _`Tendrl integration tests`: https://github.com/usmqe/usmqe-tests/blob/master/docs/test_execution.rst
