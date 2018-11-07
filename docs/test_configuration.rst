====================
 Test Configuration
====================

Configuration of *USM QE integration tests* project uses `YAML configuration
files` and `ansible hosts files`.

Configuration Scheme
====================

Since there are `multiple ways to configure pytest`_, we defined the following
scheme:

* Main *pytest config file* `pytest.ini`_ is committed in the root directory
  of ``usmqe-tests`` repository. This file contains pytest configuration.

* *YAML configuration files* are expected to contain actual configuration.
  `conf/main.yaml`_ should contain list of other configuration files that are
  used as test configuration. There should be linked `conf/defaults.yaml`_ at
  first place. After this there can be more configuration files that are
  specific to testing enviroment (for more see example configuration
  `conf/usm_example.yaml`_). `conf/defaults.yaml`_ file should contain test
  configuration that is not environment specific.

* Ansible *host inventory file* (see an example in `conf/usm_example.hosts`_),
  which is used both by ansible and by USM QE inventory module to organize
  machines into groups by it's role in test cluster. Actual path of this file
  is configured in one of the `YAML configuration files`
  (see `conf/main.yaml`_).


Details for Test Development
============================

To learn how to access configuration values from code of a test case, see
:ref:`config-devel-label` for more details.


.. _config-before-testrun-label:

Configuration before test run
=============================

We assume that:

* *QE Server machine* has been configured as described in
  :ref:`qe-server-label`

* You have *host inventory file* for the test cluster, which has been already
  deployed (our deployment automation should generate the inventory file
  in the end of the process).

* You are logged as `usmqe` user on the QE Server

Now, you need to:

* Check that ``usmqe`` user can ssh to all nodes with his ssh key stored 
  in ``~/.ssh``. This can be configured in ``~/.ssh/config``.
  Public ssh key is deployed on all machines of test cluster.

* Store *host inventory file* in ``conf/clustername.hosts`` and specify this
  path in ``inventory_file`` option of `conf/main.yaml`_.

* Verify that ssh and ansible are configured so that one can reach all machines
  from test cluster:

  .. code-block:: console

      [usmqe@qeserver ~]$ ansible -i conf/clustername.hosts -m ping -u root all

* Provide all mandatory options in *usm config file*.
  This includes: ``username``, ``password``, ``web_url``, ``api_url`` and
  ``cluster_member``.
  The actual list depends on the test suite you are going to run (eg. api
  tests don't care about ``web_url`` while LDAP integration tests would need
  to know address of the LDAP server).

Configuration options
======================

* ``log_level`` - Log level. It can be one of [DEBUG, INFO, WARNING,
                  ERROR, CRITICAL, FATAL]  

* ``username`` - API and UI login

* ``password`` - API and UI password

* ``web_url`` - web UI url

* ``api_url`` - API url

* ``etcd_api_url`` - Etcd API url

* ``ca_cert`` - path to CA cert

* ``cluster_member`` - one of nodes from cluster which identifies cluster for re-use testing,
  see section :ref:`functional_tests`.

.. _`multiple ways to configure pytest`: http://doc.pytest.org/en/latest/customize.html
.. _`pytest.ini`: https://github.com/usmqe/usmqe-tests/blob/master/pytest.ini
.. _`conf/usm_example.yaml`: https://github.com/usmqe/usmqe-tests/blob/master/conf/usm_example.yaml
.. _`conf/usm_example.hosts`: https://github.com/usmqe/usmqe-tests/blob/master/conf/usm_example.hosts
.. _`conf/main.yaml`: https://github.com/usmqe/usmqe-tests/blob/master/conf/main.yaml
.. _`conf/defaults.yaml`: https://github.com/usmqe/usmqe-tests/blob/master/conf/defaults.yaml
