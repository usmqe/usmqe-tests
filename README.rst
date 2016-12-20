==========================
 USM QE Integration Tests
==========================

USM QE tests are concerned with automated integration testing of `Tendrl
project`_.

This README file provides just a basic overview. For more details check the
`usm qe documentation`_ (sphinx sources are stored in the ``docs`` directory of
this project).

Overview of the repository structure
------------------------------------

Main top level directories:

* ``docs``: documentation (sphinx) of usmqe integration tests and it's setup
* ``conf``: configuration files, only examples are commited in the repository
* ``plugin``: custom pytest plugins
* ``usmqe``: main usmqe python module
* ``usmqe_tests``: usmqe tests code (uses pytest framework)

In the root dir of the repository, there are also:

* main pytest ``conftest.py`` file with core configuration of the pytest
  framework (for running tests cases from ``usmqe_tests`` directory)
* ``tox.ini`` and ``setup.py`` (for testing the usmqe module itself, see
  details on unit tests of ``usmqe`` module below)


Setup
-----

USM QE integrations tests are expected to be executed on a virtual or bare
metal machines so that for each storage role (eg. gluster client, ceph monitor,
tendrl console, ...) there is a dedicated machine (eg. storage client role
should not be deployed on the same machine as ceph monitor) and if the role
requires multiple machines, a minimal amount of machines needs to be available
based on the role needs (eg. having a trusted storage pool on just 2 machines
is not very useful for proper integration testing because it would prevent us
from testing some important use cases).

For this reason, all post installation and test setup configuration steps
are automated via ansible playbooks and stored in a separate `usmqe-setup`_
repository. You need to deploy test machines using playbooks from there.

For more details, see setup documents in ``docs`` directory (eg. `Setup of QE
Server role`_).


Unit Tests of usmqe module
--------------------------

Note that the purpose of ``tox.ini`` file in the root directory of this
repository is to run unit tests of ``usmqe`` module. It has nothing to do with
running of usm qe integration tests.

The code and pytest configuration of the unit tests are stored in
``usmqe/unit_tests`` directory. For more details see the readme file there.


License
-------

Distributed under the terms of the `GNU GPL v3.0`_ license,
usmqe-tests is free and open source software.


.. _`GNU GPL v3.0`: http://www.gnu.org/licenses/gpl-3.0.txt
.. _`Tendrl project`: http://tendrl.org/
.. _`usm qe documentation`: https://usmqe-tests.readthedocs.io/en/latest/
.. _`usmqe-setup`: https://github.com/Tendrl/usmqe-setup
.. _`Setup of QE Server role`: https://github.com/Tendrl/usmqe-tests/blob/master/docs/qe_server_setup.rst
