.. _qe-server-label:

====================
 Setup of QE Server
====================

:author: mbukatov
:date: 2018-06-08

QE Server is machine where ``usmqe-tests`` (along with all it's dependencies)
are installed and where the integration tests are executed from.

Requirements
============

QE Server must be a RHEL/CentOS 7 machine.

QE Server Playbook
==================

To unify and automate the deployment of QE Server machines, usmqe team
maintains `qe_server.yml`_ playbook in the `usmqe-setup repository`_. You
should use this playbook so that the same qe enviroment is used across all
qe machines.


Quick Example of QE Server deployment
=====================================

You need a RHEL 7 or CentOS 7 machine for the QE Server. For the purpose of this
example, we are going to quickly create one virtual machine via `virt-builder`_
tool (to use this tool as shown below, you need to install at least
``libguestfs-tools-c`` and ``libguestfs-xfs`` packages, see also `libguestfs
Fedora package page`_).

First we build a vm image (uploading ssh authorized keys like this would make
the machine accessible for everyone who has keys on the machine you are running
this command):

.. code-block:: console

    $ virt-builder centos-7.5 -o mbukatov.qe-server.centos7.qcow2 --size 15G --format qcow2 --mkdir /root/.ssh  --chmod 0700:/root/.ssh  --upload /root/.ssh/authorized_keys:/root/.ssh/authorized_keys --selinux-relabel --update

Note that ``virt-builder`` sets random root password, which you may like to
write down in your password manager so that you can connect to the machine
directly via console (using ``virsh console``) later in case of problems. That
said, under normal circumstances you will connect to the machine via ssh
using key based authentication.

Then we `import the new image into libvirt`_ creating new virtual machine (aka
guest) and  booting it for the first time:

.. code-block:: console

    # virt-install --import --name mbukatov --ram 2048 --os-variant rhel7 --disk path=/var/lib/libvirt/images/mbukatov.qe-server.centos7.qcow2,format=qcow2 --network default --noautoconsole

If you need change default network bridge or MAC address of the virtual
machine, update ``--network`` option of ``virt-install``, eg.: ``--network
bridge=br0_vlan4,mac=52:54:00:59:15:04``.

When the new machine is ready, specify an ip address or fqdn of the new qe
server in the inventory file:

.. code-block:: console

    $ cat qe.hosts
    [qe_server]
    10.34.126.60

And make sure you have ssh configured properly (this includes ssh keys and
local ssh client configuration) so that ansible can work with the machine:

.. code-block:: console

	$ ansible -i qe.hosts -m ping qe_server
	10.34.126.60 | SUCCESS => {
		"changed": false, 
		"ping": "pong"
	}

Then you can run the ``qe_server.yml`` playbook:

.. code-block:: console

    $ ANSIBLE_ROLES_PATH=~/projects/tendrl.org/tendrl-ansible/roles ansible-playbook -i qe.hosts qe_server.yml

Note that we have to reference `tendrl-ansible`_ here as the qe server playbook
uses `tendrl-ansible.gluster-gdeploy-copr`_ role, which installs *upstream*
build of `gdeploy`_.

When the ansible playbook run finishes, you can login to the usmqe account
on the QE Server for the first time:

.. code-block:: console

    $ ssh root@10.34.126.6
    [root@mbukatov ~]# su - usmqe
    [usmqe@mbukatov ~]$ ls
    tendrl-ansible  usmqe-setup  usmqe-tests

Note that ``rh-python36`` software collection is enabled by default in
``~/.bashrc`` file of usmqe user account and that all requirements (eg. pytest,
mrglog, ...) are already available:

.. code-block:: console

    [usmqe@qeserver ~]$ python --version
    Python 3.6.3
    [usmqe@qeserver ~]$ py.test --version
    This is pytest version 3.6.1, imported from /home/usmqe/.local/lib/python3.6/site-packages/pytest.py
    setuptools registered plugins:
      pytest-ansible-playbook-0.3.0 at /home/usmqe/.local/lib/python3.6/site-packages/pytest_ansible_playbook.py
    [usmqe@qeserver ~]$ which mrglog_demo.py
    ~/.local/bin/mrglog_demo.py

Also note that even though the default python for usmqe user is ``python3.6``
from the software collection, one can still run other system utilities which
are running on system default python2:

.. code-block:: console

    [usmqe@qeserver ~]$ ansible --version
    ansible 2.5.3
      config file = /etc/ansible/ansible.cfg
      configured module search path = [u'/home/usmqe/.ansible/plugins/modules', u'/usr/share/ansible/plugins/modules']
      ansible python module location = /usr/lib/python2.7/site-packages/ansible
      executable location = /bin/ansible
      python version = 2.7.5 (default, Apr 11 2018, 07:36:10) [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]

This is the case because all python tools packaged in Fedora/Red Hat/CentOS
uses explicit shebang:

.. code-block:: console

    [usmqe@qeserver ~]$ head -1 /usr/bin/ansible
    #!/usr/bin/python2


Related information
===================

At this point, we have a fresh QE server machine. But for us to be able to run
integration tests, we need to:

* Prepare fresh machines where Tendrl and Gluster will be installed.
  See :ref:`test-enviroment-label`.
* Configure the tests, go into ``~/usmqe-tests`` directory and
  follow :ref:`config-before-testrun-label`

For full description and examples how to run integration tests, see
:ref:`test-execution-label`.


.. _`virt-builder`: http://libguestfs.org/virt-builder.1.html
.. _`libguestfs Fedora package page`: https://apps.fedoraproject.org/packages/libguestfs
.. _`import the new image into libvirt`: https://access.redhat.com/documentation/en-US/Red_Hat_Enterprise_Linux/7/html/Virtualization_Deployment_and_Administration_Guide/sect-Guest_virtual_machine_installation_overview-Creating_guests_with_virt_install.html
.. _`qe_server.yml`: https://github.com/usmqe/usmqe-setup/blob/master/qe_server.yml
.. _`usmqe-setup repository`: https://github.com/usmqe/usmqe-setup
.. _`tendrl-ansible`: https://github.com/Tendrl/tendrl-ansible
.. _`tendrl-ansible.gluster-gdeploy-copr`: https://github.com/Tendrl/tendrl-ansible/tree/master/roles/tendrl-ansible.gluster-gdeploy-copr
.. _`gdeploy`: https://gdeploy.readthedocs.io/en/latest/
