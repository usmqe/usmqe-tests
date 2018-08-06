==================
 Test Development
==================

This is an overview of style and rules we follow when automating system
functional test cases.

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

    for host in inventory.role2hosts("gluster"):
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


Structure of Functional Tests
=============================

Setup of *Gluster trusted storage pool(s)* is done prior test execution, and is
fully automated via `gdeploy config files`_ in `usmqe-setup/gdeploy_config/`_.

No *pytest fixture* or *test case* creates or removes *Gluster trusted storage
pool(s)* on it's own.

The test cases are implemented as pytest functions, stored in logical chunks in
python source files (python modules).

Test cases which requires an imported cluster (aka trusted storage pool), uses
pytest fixture ``imported_cluster``, which:

* Doesn't create the cluster, but just checks if the cluster is already
  imported and tries to import it if it's not imported already. If it fails
  during the import or no suitable cluster is available for import, it
  raises an errror.
* Cluster suitable for import is identified using node defined by
  ``usm_cluster_member`` parameter in usmqe configuration file.
* Returns information about the imported cluster via value of the fixture
  passed to the test function (``cluster`` object), which includes cluster
  name, cluster id, volumes in the cluster.
* Teardown of this fixture runs cluster unmanage if the cluster was imported
  during setup phase.

Test casess are tagged by tags:

* TODO: marker for gluster related tests
* TODO: marker for volume type
* TODO: marker for happy path tests
* TODO: marker for status of gluster profiling
* TODO: marker for human readable name
* marker for working/stable test - currently ``mark.testready``
* TODO: marker for wip test?

 .. note::

    Open questions, enhancements:

    * fixture to read markers and change import accordingly
    * fixture to read markers and check if the cluster matches the
      requirements (eg. do we have specified volume type there?)
    * multiple clusters

Tagging makes it possible to run for example just tests related to particular
volume which requires profiling to be enabled.

All tests should use a proper pytest fixture for setup and teardown, if setup
or teardown is needed. All objects created during testing should be removed
after test run. The same applies for the fixtures, if something is created
during setup phase, it should be removed during teardown. There should not be
any remains after test run.

Exceptions
``````````

There are only 2 exceptions from the rules listed above.

Test cases which test import or unamanage cluster operations itself should
not use ``imported_cluster`` fixture, but handle the import itself in the code
of the test case.

Such cases should be stored in separate module (python source file) so that it
could be part of separate test runs.

The same would apply for **CRUD happy path tests**, which are stored in one
python source file where they share object created and deleted during testing
tests from file. These tests should run in same order like they are written in
the file. Such cases are run at the beginning of testing because they left
created/imported clusters for further testing. This exception exists because
cluster creation have extremly big resource needs.

.. note::

    Note that we don't have any CRUD happy path tests and are not going to have
    them untill we need to test day 1 or day 2 operations, which includes
    creating or deleting gluster clusters, volumes or other cluster components.


.. _`PEP 8`: https://www.python.org/dev/peps/pep-0008/
.. _`python 3`: https://docs.python.org/3/whatsnew/3.0.html
.. _`usmqe/unit_tests`: https://github.com/usmqe/usmqe-tests/tree/master/usmqe/unit_tests
.. _`tox.ini`: https://github.com/usmqe/usmqe-tests/blob/master/tox.ini
.. _`.travis.yml`: https://github.com/usmqe/usmqe-tests/blob/master/.travis.yml
.. _`each new pull request via Travis CI`: https://travis-ci.org/usmqe/usmqe-tests/pull_requests
.. _`gdeploy config files`: https://gdeploy.readthedocs.io/en/latest/conf.html
.. _`usmqe-setup/gdeploy_config/`: https://github.com/usmqe/usmqe-setup/tree/master/gdeploy_config
