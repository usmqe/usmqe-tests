==================
 Test Development
==================

.. image:: https://travis-ci.org/Tendrl/usmqe-tests.svg?branch=master
    :target: https://travis-ci.org/Tendrl/usmqe-tests

TODO: include all the details

Code style
==========

All python code in this project must be `python 3`_ compatible. Moreover
no python 2 compatibility layers or extensions should be added into the
code, with the exceptions of pytest plugins (code in ``plugin`` directory).

We follow `PEP 8`_ with a single exception regarding the maximum line
length: we use 80 character as a soft limit so that one could break this
rule if readability is affected, assuming the line length doesn't go over
100 characters (the hard limit).


.. _config-devel-label:

Reading Configuration Values
============================

To access data from the host inventory, use functions provided by
``usmqe.inventory`` module:

.. code-block:: python

    import usmqe.inventory as inventory

    for host in inventory.role2hosts("ceph_osd"):
        print("check storage server {0}".format(host))

To access USM QE configuration, use standard pytest configuration functions:

.. code-block:: python

    import pytest

    pytest.config.getini("usm_username")

Obviously this assumes that the ``usm_username`` option has been specified in
USM QE config file (which is referenced via ``usm_config`` option). The minimal
ini file for the previous example to work would look like this::

    [usmqepytest]
    usm_username = admin

Reading of both *USM QE config file* and *host inventory file* is implemented
in ``plugin/usmqe_config.py`` module, while management of *host inventory file*
is handled by ``usmqe/inventory.py`` module.


.. _unit-tests-label:

Unit Tests
==========

We have unit tests of ``usmqe-tests`` project itself, which covers some code in
``usmqe`` module and runs flake8 checks on this module and the test code. One
is encouraged to add unit tests when adding code into ``usmqe`` module and to
run the tests before submitting a pull request.

Code related to unit testing:

* `usmqe/unit_tests`_ directory which contains pytest configuration
  (``pytest.ini``, ``conftest.py``) and the code of unit tests itself
* `tox.ini`_ file
* `.travis.yml`_ config for Travis CI integration, uses tox

Unit test execution
```````````````````

To execute the unit tests, just run ``tox`` command in root directory of
``usmqe-tests`` repo.

Moreover the unit tests are executed for `each new pull request via Travis
CI`_.


Functional Tests
====================

Functional API tests are stored in logical chunks in files. Tests are tagged by tags.
So it is possible to run for example just Ceph tests. All tests should have
fixture for proper ``setup`` and ``teardown``. All objects created during testing
should be removed after test run. There should not be any remains after test run.

There are *only* 2 exceptions:
* CRUD *happy path* tests which are stored in one file where they share
  object created and deleted during testing tests from file. These tests should run
  in same order like they are written in the file. CRUD tests **are not** tagged.

* create or import cluster tests which run at the same beginning of testing because
  they left created/imported clusters for further testing. This exception exists
  because cluster creating and importing have extremly big resource needs.

Files with tests example:

* crud_ceph_pool.py - contents create/read/update/delete Ceph pool tests.
  Tests should run in exact order. Tests share ``pool`` object which is
  created in 1st test, read in 2nd test, update in 3rd test and deleted
  in last test. This kind of tests are usually run in CI 
  for smoke/reggression/acceptance testing. Sharing of ``pool`` object
  saves resources. These tests are only *positive* or *happy path*.
  All mentioned tests for one object are stored in one file
  with prefix crud + [storage type] + tested object.

* create_ceph_cluster.py - In file with name in form (create|import) + [storage type]
  are stored *positive* or *happy path* tests for importing or creating cluster
  for one storage type. These tests are run before any other tests because
  they create or import cluster which is used during further testing.
  Cluster identification is stored in configuration so it can be used in other tests.
  Cluster is identified by one of its machine during import process. Once it is imported
  or created it is identified by ``cluster id``. This will change once Tendrl can
  internally identify clusters by their names.

Test uses fixtures for getting ``cluster`` object:

* cluster_reuse_(storage_type) - fixture loads cluster ID from configuration and
  returns ``cluster`` object which can be used for testing. Cluster should already
  exist and it's made by ``cluster_`` or ``import_`` test. This fixture is used
  in most of the tests.

* cluster_import_(storage_type) - fixture imports cluster and returns ``cluster``
  object. Cluster should be created and imported by this fixture.

* cluster_create_(storage_type) - fixture creates cluster and returns ``cluster``
  object. Cluster should not exist before test run.

For most cases first ``reuse`` fixture is used if test requires ``cluster`` object.
Reused ``cluster`` object has not ``teardown`` fixture.
All other objects than ``cluster`` have ``create`` fixture and ``teardown``
fixture.

.. _`PEP 8`: https://www.python.org/dev/peps/pep-0008/
.. _`python 3`: https://docs.python.org/3/whatsnew/3.0.html
.. _`usmqe/unit_tests`: https://github.com/Tendrl/usmqe-tests/tree/master/usmqe/unit_tests
.. _`tox.ini`: https://github.com/Tendrl/usmqe-tests/blob/master/tox.ini
.. _`.travis.yml`: https://github.com/Tendrl/usmqe-tests/blob/master/.travis.yml
.. _`each new pull request via Travis CI`: https://travis-ci.org/Tendrl/usmqe-tests/pull_requests
