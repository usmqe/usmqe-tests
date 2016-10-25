=========================
 USMQE Integration Tests
=========================

This repository contains integration test code of `Tendrl project`_.

Overview of the repository structure
------------------------------------

Main top level directories:

* ``conf``: configuration files, only examples are commited in the repository
* ``plugin``: custom pytest plugins
* ``usmqe``: main usmqe python module
* ``usmqe_tests``: usmqe tests code (uses pytest framework)

In the root dir of the repository, there are also:

* various pytest files (eg. ``conftest.py``, ``pytest.ini``) with core
  configuration of the pytest framework (for running tests cases from
  ``usmqe_tests`` directory)
* ``tox.ini`` and ``setup.py`` (for testing the usmqe-tests code itself)

License
-------

Distributed under the terms of the `GNU GPL v3.0`_ license,
usmqe-tests is free and open source software.


.. _`GNU GPL v3.0`: http://www.gnu.org/licenses/gpl-3.0.txt
.. _`Tendrl project`: https://github.com/Tendrl/
