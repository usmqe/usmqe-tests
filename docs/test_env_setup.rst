.. _test-enviroment-label:

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


Ansible Roles for Tendrl Setup
==============================

Right now, we maintain ansible roles and playbook which automates production
like installation of all Tendrl components. `Tendrl project wide
documentation`_ is followed, but most details are based on documentation or
README files of each component.

For each Tendrl component, there is a role in `usmqe-setup repository`_. For
example, there are:

* `tendrl-node-agent`_
* `tendrl-api`_

Note: the list presented doesn't include all roles. You would need to check
``roles`` directory in the repository to see current full list of roles.

Every ansible role of particular tendrl component has the following tasks
structure::

    tasks/
    └── main.ym

Moreover, related Tendrl documentation (or README files) used to write the role
should be referenced in the README file of the role or in the yaml file with
tasks directly.


.. _`qe_server.yml`: https://github.com/Tendrl/usmqe-setup/blob/master/qe_server.yml
.. _`usmqe-setup repository`: https://github.com/Tendrl/usmqe-setup
.. _`tendrl-node-agent`: https://github.com/Tendrl/usmqe-setup/tree/master/roles/tendrl-node-agent
.. _`tendrl-api`: https://github.com/Tendrl/usmqe-setup/tree/master/roles/tendrl-api
.. _`added a task to install systemd unit files`: https://github.com/Tendrl/usmqe-setup/commit/75f489d850ea753582cfa8532957c2a9d153d186
.. _`Tendrl project wide documentation`: https://github.com/Tendrl/documentation/blob/master/deployment.adoc
