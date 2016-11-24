===================
 Test Configuraion
===================

USM QE integration tests are configurabe via these files:

* Main *pytest config file*: ``pytest.ini`` in root directory of ``usmqe-tests``
  repository. This file contains main pytest configuration and default values
  for main USMQE configuration options. Under normal cirsumstances one would 
  edit only ``USM_CONFIG`` and ``USM_HOST_CONFIG`` options, while all the
  others usmqe default values should not be changed there.

* Ansible *host inventory file* (see an example in ``conf/example.hosts``),
  which is used both by ansible and by USMQE inventory module to organize
  machines into groups by it's role in test cluster.

* *usmqe config file* (see an example in ``conf/example_usm.ini``). You need
  to provide mandatory values in this file to be able to run the tests.
  Options configured there includes urls of web and api server, username and
  password and so on.


Implementation Details
======================

Reading of both *usmqe config file* and *host inventory file* is implemented in
``plugin/usmqe_config.py`` module.

Management of *host inventory file* is handled by ``usmqe/inventory.py``
module. See an example of it's usage:

.. code-block:: python

    import usmqe.inventory as inventory

    for host in inventory.role2hosts("ceph_osd"):
        print("check storage server {0}".format(host))


Example of test configuration
=============================

We assume that:

* *QE Server mahcine* has been configured as described in
  :ref:`qe-server-label`

* You have *host inventory file* for the test cluster, which has been already
  deployed (our deployment automation should generate the inventory file
  in the end of the process).

* You are logged as ``usmqe`` user on the QE Server

Now, you need to:

* Check that ``usmqe`` user has a private ssh key in ``~/.ssh/id_rsa`` file 
  (this is default location of ssh key specified in ``USM_KEYFILE`` option of
  ``pytest.ini``) and has it's public ssh key deployed on all machines of test
  cluster.

* Store *host inventory file* in ``conf/clustername.hosts`` and specify this
  path in ``USM_HOST_CONFIG`` option of ``pytest.ini``.

* Verify that ssh and ansible are configured so that one can reach all machines
  from test cluster:

  .. code-block:: console

      [usmqe@qeserver ~]$ ansible -i conf/clustername.hosts -m ping -u root all

* Initiate new *usmqe config file*: ``cp conf/example_usm.ini conf/usm.ini``
  and check that ``USM_CONFIG`` option of ``pytest.ini`` file points to this
  file.

* Provide all mandatory options in *usm config file* initialized in a previous
  step. This includes: ``username``, ``password``, ``web_url`` and ``api_url``.
  The actuall list depends on the test suite you are going to run (eg. api
  tests doesn't care about ``web_url`` while LDAP integration tests would need
  to know address of the LDAP server).
