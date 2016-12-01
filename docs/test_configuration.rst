====================
 Test Configuration
====================

Configuration of *USM QE integration tests* project piggibacks/reuses pytest
ini-options parser, so that all USM QE configuration options could be specified
in ``pytest.ini`` file. To prevent a conflict with pytest ini-option names, we
use ``usm_`` prefix in a name of every option.

Configuration Scheme
====================

Since there are `multiple ways to configure pytest`_, we defined the following
scheme:

* Main *pytest config file* `pytest.ini`_ is committed in the root directory
  of ``usmqe-tests`` repository. This file contains pytest configuration
  and *default values* for most important USM QE configuration options. Under
  normal circumstances (configuring ``usmqe-tests`` before test run) one would
  not need to change this file at all, because any default value specified here
  can be reconfigured in USM QE config file (with the exception of
  ``usm_config`` and ``usm_host_config`` options).

* *USM QE config file* is expected to contain actual configuration. See an
  example in `conf/example_usm.ini`_, while the actual path of this file is
  configured in ``usm_config`` option in main ``pytest.ini`` file. Any option
  specified there overrides the default from main ``pytest.ini``. This is the
  file one is supposed to create and change as needed. You need to provide
  all important config values in this file to be able to run the tests.

* Ansible *host inventory file* (see an example in ``conf/example.hosts``),
  which is used both by ansible and by USM QE inventory module to organize
  machines into groups by it's role in test cluster. Actual path of this file
  is configured in ``usm_host_config`` option in main ``pytest.ini`` file.

* Moreover ad hoc reconfiguration of any USM QE option is possible via pytest
  command line option ``--override-ini``. See an example how to use different
  *host inventory file* for a particular test run:

  .. code-block:: console

      $ py.test -o=usm_host_config=conf/mbukatov01.hosts usmqe_tests/foo/bar

  This is usefull for test runs started by hand during test development or
  debugging.


Details for Test Development
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


Configuration before test run
=============================

We assume that:

* *QE Server machine* has been configured as described in
  :ref:`qe-server-label`

* You have *host inventory file* for the test cluster, which has been already
  deployed (our deployment automation should generate the inventory file
  in the end of the process).

* You are logged as ``usmqe`` user on the QE Server

Now, you need to:

* Check that ``usmqe`` user has a private ssh key in ``~/.ssh/id_rsa`` file 
  (this is default location of ssh key specified in ``usm_keyfile`` option of
  ``pytest.ini``) and has it's public ssh key deployed on all machines of test
  cluster.

* Store *host inventory file* in ``conf/clustername.hosts`` and specify this
  path in ``usm_host_config`` option of ``pytest.ini``.

* Verify that ssh and ansible are configured so that one can reach all machines
  from test cluster:

  .. code-block:: console

      [usmqe@qeserver ~]$ ansible -i conf/clustername.hosts -m ping -u root all

* Initiate new *USM QE config file*: ``cp conf/example_usm.ini conf/usm.ini``
  and check that ``usm_config`` option of ``pytest.ini`` file points to this
  file.

* Provide all mandatory options in *usm config file* initialized in a previous
  step. This includes: ``username``, ``password``, ``web_url`` and ``api_url``.
  The actual list depends on the test suite you are going to run (eg. api
  tests doesn't care about ``web_url`` while LDAP integration tests would need
  to know address of the LDAP server).


.. _`multiple ways to configure pytest`: http://doc.pytest.org/en/latest/customize.html
.. _`pytest.ini`: https://github.com/Tendrl/usmqe-tests/blob/master/pytest.ini
.. _`conf/example_usm.ini`: https://github.com/Tendrl/usmqe-tests/blob/master/conf/example_usm.ini
