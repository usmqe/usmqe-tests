.. _test-execution-label:

================
 Test Execution
================

This document briefly describes how to execute USM QE tests.

Preparation for running the tests
=================================

Before running USM QE tests, you need to prepare:

* QE Server machine as described in :ref:`qe-server-label`.
  The tests are executed under ``usmqe`` user account on this QE Server
  machine.
* Machines for Tendrl/Gluster have been deployed as described in
  :ref:`test-enviroment-label`.
* Configuration of USM QE tests has been done as explained in
  :ref:`config-before-testrun-label`.

How to run the tests
====================

This is step by step description how to run the tests. First of all, login on
QE Server as ``usmqe`` user:

.. code-block:: console

   $ ssh mbukatov.usmqe.example.com
   [root@mbukatov ~]# su - usmqe
   [usmqe@mbukatov ~]$

Note that the setup playbook prepared both setup and test repositories there:

.. code-block:: console

   [usmqe@mbukatov ~]$ ls -ld usmqe-*
   drwxr-xr-x. 10 usmqe usmqe 4096 Dec 18 04:13 usmqe-setup
   drwxr-xr-x. 11 usmqe usmqe 4096 Dec 18 03:50 usmqe-tests

You may consider updating these repositories (eg. running ``git pull``) before
going on, but this depends on the task you are working on.

Go to ``usmqe-tests`` repository and check that you have already updated the
config file to match your environment (as noted in previous section):

.. code-block:: console

   [usmqe@mbukatov ~]$ cd usmqe-tests
   [usmqe@mbukatov usmqe-tests]$ git status -s conf
    M conf/main.yaml
   [usmqe@mbukatov usmqe-tests]$ cat conf/main.yaml
   # List of configuration files loaded in usmqe test framework.
   # It is recomended to keep defaults.yaml configuration file and attach more
   # configuration files.
   #
   # Each item in list overwrites previous configuration file.
   #
   configuration_files:
     - conf/defaults.yaml
     - conf/mbukatov-usm1.yaml
   inventory_file:
     - conf/mbukatov-usm1.hosts

File ``mbukatov-usm1.hosts`` is ansible inventory file, which describes my
testing machines, while ``mbukatov-usm1.yaml`` is usmqe config file, used by
the tests. I mention this here only to make it clear how it all fits together,
for full details about configuration of USM QE tests, see references in
previous section.

The tests are written in pytest_ framework, and we use custom wrapper
``pytest_cli.py`` to execute them. The wrapper is used to simplify test
configuration (so that one doesn't have to repeat the same config values
multiple times, as eg. inventory file is used by both pytest ansible plugin
and test code itself).

This means that command to run the tests looks like this:

.. code-block:: console

   [usmqe@mbukatov usmqe-tests]$ ./pytest_cli.py [pytest_options] usmqe_tests/[file_or_dir] ...

Note that running all the tests (``./pytest_cli.py usmqe_tests``) is not a good
idea (there are various types of tests, including demo, and it never makes sense
to just run them all), always specify at least directory or marker there.

Useful `pytest options`_ one can use are:

* ``-m MARKEXPR`` only run tests matching given mark expression
* ``--pdb`` start the interactive Python debugger on errors
* ``-v`` verbose mode
* ``-s`` turns off per-test capture logging, all logs are immediately
  reported on console (which is useful when developing new test code and
  immediate feedback is needed)

.. _`pytest`: http://docs.pytest.org/en/latest/index.html
.. _`pytest options`: https://docs.pytest.org/en/latest/usage.html

Examples
========

This section contains few basic examples how to run the tests.

Get familiar with logging and test reporting
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To get basic idea how usm qe test runs and error reporting looks like, one can
run ``usmqe_tests/demo`` test suite. This demo should work even with default
example configuration committed in the repository.

First of all, you can use ``--collect-only`` option of pytest_ to get list of
test cases in the demo test module:

.. code-block:: console

   [usmqe@mbukatov usmqe-tests]$ ./pytest_cli.py --collect-only usmqe_tests/demo/
   =================================== test session starts ===================================
   platform linux -- Python 3.6.3, pytest-3.6.1, py-1.5.3, pluggy-0.6.0
   rootdir: /home/usmqe/usmqe-tests, inifile: pytest.ini
   plugins: ansible-playbook-0.3.0
   collected 17 items
   <Module 'usmqe_tests/demo/test_logging.py'>
     <Function 'test_pass_one'>
     <Function 'test_pass_many'>
     <Function 'test_pass_parametrized[a-1]'>
     <Function 'test_pass_parametrized[a-2]'>
     <Function 'test_pass_parametrized[a-3]'>
     <Function 'test_pass_parametrized[b-1]'>
     <Function 'test_pass_parametrized[b-2]'>
     <Function 'test_pass_parametrized[b-3]'>
     <Function 'test_pass_parametrized_fixture[1]'>
     <Function 'test_pass_parametrized_fixture[2]'>
     <Function 'test_fail_one_check'>
     <Function 'test_fail_many_check'>
     <Function 'test_fail_one_exception'>
     <Function 'test_error_in_fixture'>
     <Function 'test_xfail_one'>
     <Function 'test_xfail_many'>
     <Function 'test_fail_anyway'>

Then the test execution of the demo:

.. code-block:: console

   [usmqe@mbukatov usmqe-tests]$ ./pytest_cli.py usmqe_tests/demo/

In this case, only short summary of the test run is reported, along with
full logs for test cases which failed. The logs here are using mrglog_ module.
The output itself is too long to be included there. Moreover for full
understanding, one is expected to check source code of the demo test module.

.. _mrglog: https://github.com/ltrilety/mrglog

.. note::

   Because of commit `Improve the error handling`_, error in the test is
   catched in mrglog statistics. However there could be a discrepancy with pytest
   results. If the error/exception originates from the test method code and there
   is no failed check, pytest says the test ``FAILED`` at the same time mrlog
   evaluates the result of the test as ``ERROR``.

.. _`Improve the error handling`: https://github.com/usmqe/usmqe-tests/commit/ef0a30eb5f68f9e32f898b02b0d473dec666660a

Run all tests for alering
~~~~~~~~~~~~~~~~~~~~~~~~~

Assuming we have the machines and configuration ready and that we want junit
xml report from the test run:

.. code-block:: console

   [usmqe@mbukatov usmqe-tests]$ ./pytest_cli.py --junit-xml=logs/result.xml usmqe_tests/alerting

The `xml junit`_ file with the full test report will be then placed in
``logs/result.xm`` even if the ``logs`` directory didn't exist before.

.. _`xml junit`: https://stackoverflow.com/questions/442556/spec-for-junit-xml-output
