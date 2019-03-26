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

* ``conf``: configuration files for the tests
* ``docs``: documentation (sphinx) of the tests and it's development and setup
* ``plugin``: custom pytest plugins
* ``usmqe``: python module with common helper functions
* ``usmqe_tests``: code of the tests (uses pytest framework)

Files stored in the root dir of the repository (eg. ``.travis.yml``,
``conftest.py``, ``pytest.ini``, ...) should not be updated unless one need to
change underlying pytest, tox or CI plumbing (eg. adding new pytest plugin).

Overview of test cases
----------------------

To get a list of test cases automated in ``usmqe_tests`` (so that pytest
parametrization is taken into account), run the following command in root
directory of this repository::

    $ tox -e testcaselist

The total number of test cases is reported as ``collected X items`` line, which
is followed by a list of all test cases grouped by python source code file.

This ``testcaselist`` report is also run in Travis CI among unit tests of
``usmqe`` module, see next section for more details.

Unit and Integration Tests of usmqe module
------------------------------------------

Note that the purpose of ``tox.ini`` file in the root
directory of this repository is to run unit tests of ``usmqe`` module. Beside
unit tests there are also integration tests of usmqe module which are not
triggered by ``tox`` but by ``pytest`` command. It has nothing to do with
running of the integration tests for Tendrl.

The code and pytest configuration of the unit tests are stored in
``usmqe/unit_tests`` directory. For more details see the readme file there.

The same applies to integration tests which are stored in
``usmqe/integration_tests``.

.. image:: https://travis-ci.org/usmqe/usmqe-tests.svg?branch=master
    :target: https://travis-ci.org/usmqe/usmqe-tests

License
-------

Distributed under the terms of the `GNU GPL v3.0`_ license,
usmqe-tests is free and open source software.


.. _`GNU GPL v3.0`: http://www.gnu.org/licenses/gpl-3.0.txt
.. _`Tendrl project`: http://tendrl.org/
.. _`usm qe documentation`: https://usmqe-tests.readthedocs.io/en/latest/
.. _`Setup of QE Server role`: https://github.com/usmqe/usmqe-tests/blob/master/docs/qe_server_setup.rst
