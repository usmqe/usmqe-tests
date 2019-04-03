.. _test-enviroment-label:

==========================
 Setup of Test Enviroment
==========================

USM QE integrations tests are expected to be executed on virtual or bare
metal machines so that for each storage role (eg. `gluster client`, `ceph
monitor`, `tendrl console`, ...) there is a dedicated machine (eg. storage
client role should not be deployed on the same machine as ceph monitor) and if
the role requires multiple machines, a minimal amount of machines needs to be
available based on the role needs (eg. having a trusted storage pool on just 2
machines is not very useful for proper integration testing because it would
prevent us from testing some important use cases).

For this reason, all post installation and test setup configuration steps
are automated via ansible playbooks or gdeploy config files, which are stored
in a separate `usmqe-setup repository`_:

* `GDeploy Config Directory`_ contains gdeploy configuration for all gluster
  volumes and configurations we test with.
* Playbooks with ``ci_`` prefix are used in CI to deploy test machines.
* Playbooks with ``qe_`` prefix automates qe procedures.
* Playbooks with ``test_setup`` or ``test_teardown`` prefix automates test
  setup or teardown. Automated test cases can use it via
  `pytest-ansible-playbook`_ pytest plugin.

.. _`qe_server.yml`: https://github.com/usmqe/usmqe-setup/blob/master/qe_server.yml
.. _`usmqe-setup repository`: https://github.com/usmqe/usmqe-setup
.. _`Tendrl project wide documentation`: https://github.com/Tendrl/documentation/blob/master/deployment.adoc
.. _`GDeploy Config Directory`: https://github.com/usmqe/usmqe-setup/tree/master/gdeploy_config
.. _`pytest-ansible-playbook`: https://gitlab.com/mbukatov/pytest-ansible-playbook
