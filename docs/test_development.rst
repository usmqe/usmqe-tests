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


.. _`PEP 8`: https://www.python.org/dev/peps/pep-0008/
.. _`python 3`: https://docs.python.org/3/whatsnew/3.0.html
.. _`usmqe/unit_tests`: https://github.com/Tendrl/usmqe-tests/tree/master/usmqe/unit_tests
.. _`tox.ini`: https://github.com/Tendrl/usmqe-tests/blob/master/tox.ini
.. _`.travis.yml`: https://github.com/Tendrl/usmqe-tests/blob/master/.travis.yml
.. _`each new pull request via Travis CI`: https://travis-ci.org/Tendrl/usmqe-tests/pull_requests
