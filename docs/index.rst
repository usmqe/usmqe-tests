.. usmqe-tests documentation master file, created by
   sphinx-quickstart on Tue Nov 22 19:12:55 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

==========================
 USM QE Integration Tests
==========================

USM QE tests are concerned with automated integration testing of `Tendrl
project`_.

This documentation provides all details needed for setting up and running the
integration tests, as well as instruction for development of automated test
cases.


Contents
========

.. toctree::
   :maxdepth: 2

   usmqe_team.rst
   repository_overview.rst
   qe_server_setup.rst
   test_env_setup.rst
   test_configuration.rst
   test_execution.rst
   test_development.rst


Quick Introduction
==================

USM QE tests are:

* *integration tests* - which means that:
   * all Tendrl components are tested together in production like
     configuration
   * separate machine for each machine role is needed, and when more machines
     are expected to be assigned to a cluster role, we need to have at
     least 2 or 4 such machines for the role (depends on the role itself)
   * user facing interfaces are tested (eg. we use `Tendrl REST API`_, but
     don't interfere with internal structure of *Tendrl Data Store*)
* used in *fully automated* enviroment (including setup of all machines, which
  is automated via `ansible`_)
* based on `pytest`_ framework, which is extended or changed via many pytest
  plugins
* written in `Python 3.5`_ only
* expected to be executed from Red Hat (or CentOS) 7 machine
* maintained by :ref:`usmqe-team-label`

There are 2 kind of test cases:

* `api tests` for `Tendrl REST API`_ (via `requests`_)
* `web ui tests` for *Tendrl Web Interface* (via `selenium`_)


License
=======

Distributed under the terms of the `GNU GPL v3.0`_ license,
`usmqe-tests`_ is free and open source software.


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. _`Tendrl project`: http://tendrl.org/
.. _`usmqe-tests`: https://github.com/Tendrl/usmqe-tests
.. _`GNU GPL v3.0`: http://www.gnu.org/licenses/gpl-3.0.txt
.. _`pytest`: http://docs.pytest.org/en/latest/index.html
.. _`Python 3.5`: https://docs.python.org/3/whatsnew/3.5.html
.. _`Tendrl REST API`: https://github.com/Tendrl/documentation/blob/master/api/overview.adoc
.. _`requests`: http://docs.python-requests.org/en/master/
.. _`selenium`: https://selenium-python.readthedocs.io/
.. _`ansible`: https://docs.ansible.com/ansible/
