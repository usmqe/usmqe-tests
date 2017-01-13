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

* `tendrl-commons`_
* `tendrl-node-agent`_
* `tendrl-api`_

Note: the list presented doesn't include all roles. You would need to check
``roles`` directory in the repository to see current full list of roles.

Every ansible role of particular tendrl component has the following tasks
structure::

    tasks/
    ├── binary.yml
    ├── main.yml
    └── source.ym

Where ``main.yml`` looks like this (the example comes from ``tendrl-commons``)::

    #
    # installation
    #
    
    - include: source.yml
      when: install_from == "source"
    
    - include: binary.yml
      when: install_from == "packages"
    
    #
    # post installation configuration
    #
    
    - name: Specify etcd_connection in tendrl.conf
      ini_file:
        dest=/etc/tendrl/tendrl.conf
        section=common
        option=etcd_connection
        value="{{ groups['usm_server'][0] }}"

As you can see, there are 2 additional yaml files, one for installation from
rpm packages and other for installation from source code. The default value of
``install_from`` variable should be set to ``packages`` in ``defaults`` of each
role. File ``source.yml`` should provide feature parity with rpm package based
installation, so that the common configuration steps are icluded in ``main.yml``
file directly - as *etcd_connection in tendrl.conf* is in this case.

Package (rpm) base installation has priority and should always work. Actual
testing of a Tendrl release should be done with packages only.

Source based installation is provided as a convenience so that qe team
can work with latest and greatest code to develop new test cases or check
particular unfinished new feature. It should not be used for CI test runs or
to validate that given feature or bug is done/fixed. See more details on this
in section below.

Moreover, related Tendrl documentation (or README files) used to write the role
should be referenced in the README file of the role or in the yaml file with
tasks directly.


Details On Installation From Sources
====================================

To install Tendrl component from source code, we clone git source repository
into ``/opt/tendrl/${component_name}`` first.

Here is an example from ``tendrl-commons`` role, default values of related
variables::

    #
    # variables used when install_from == source
    #

    # url of the source repository and the branch to checkout
    tendrl_common_repo_url: 'https://github.com/Tendrl/common'
    # note that you need to change the branch in the url as well
    tendrl_common_repo_branch: master

    # directory where the git repo would be cloned into
    tendrl_common_repo: /opt/tendrl/common

... and related tasks which do the cloning::

    - name: Directory for git repository
      file:
        path="{{ tendrl_common_repo }}"
        state=directory

    - name: Clone git repository
      git:
        repo={{ tendrl_common_repo_url }}
        version={{ tendrl_common_repo_branch }}
        dest={{ tendrl_common_repo }}

When a Tendrl component is implemented in python, virtualenv is not used, but
tendrl python components are installed into the system site-packages. Since
such operation breaks system consistency, this is another reason why this
should be used only for test development only.

Virtualenv is very usefull for development and testing of particular
components, and I still suggest to use it when code changes needs to be checked
manually immediately during development (and for this reason, it's a good
thing that virtualenv is suggested in devel installation docs of tendrl
components), but for installing multiple python packages which needs to run
under root for the purposes of integration testing, automation of virtualenv
based installation is not maintenable (most ansible modules doesn't consider
this use case and additional setup would be still needed).

When source based installation is not feature complete (doesn't provide the
same level of setup as expected from package based installation), it's
necessary to include assert like this in the end of yaml file to make this
clear::

    - fail: msg="There is no systemd unit installed, we can't start and enable it"
      when: not ignore_incomplete_installation

One can still use such role, but would need to set
``ignore_incomplete_installation`` to ``true`` in the playbook. That said, in
most cases, a workaround implementing missing feature would be needed for the
role to be actually useful. For the previous example, we have `added a task to
install systemd unit files`_.

The last but not least: maintenance of source based installation like this has
it's cost and we may drop this entirely in the future.


.. _`qe_server.yml`: https://github.com/Tendrl/usmqe-setup/blob/master/qe_server.yml
.. _`usmqe-setup repository`: https://github.com/Tendrl/usmqe-setup
.. _`tendrl-commons`: https://github.com/Tendrl/usmqe-setup/tree/master/roles/tendrl-commons
.. _`tendrl-node-agent`: https://github.com/Tendrl/usmqe-setup/tree/master/roles/tendrl-node-agent
.. _`tendrl-api`: https://github.com/Tendrl/usmqe-setup/tree/master/roles/tendrl-api
.. _`added a task to install systemd unit files`: https://github.com/Tendrl/usmqe-setup/commit/75f489d850ea753582cfa8532957c2a9d153d186
.. _`Tendrl project wide documentation`: https://github.com/Tendrl/documentation/blob/master/deployment.adoc
