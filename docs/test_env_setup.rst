==========================
 Setup of Test Enviroment
==========================

USM QE integrations tests are expected to be executed on a virtual or bare
metal machines so that for each storage role (eg. `gluster client`, `ceph
monitor`, `tendrl console`, ...) there is a dedicated machine (eg. storage
client role should not be deployed on the same machine as ceph monitor) and if
the role requires multiple machines, a minimal amount of machines needs to be
available based on the role needs (eg. having a trusted storage pool on just 2
machines is not very useful for proper integration testing because it would
prevent us from testing some important use cases).

For this reason, all post installation and test setup configuration steps
are automated via ansible playbooks and stored in a separate `usmqe-setup
repository`_. You need to deploy test machines using playbooks from there.

.. _`qe_server.yml`: https://github.com/Tendrl/usmqe-setup/blob/master/qe_server.yml
.. _`usmqe-setup repository`: https://github.com/Tendrl/usmqe-setup
