.. _qe-server-label:

====================
 Setup of QE Server
====================

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

You need a RHEL or CentOS 7 machine for the QE Server. For to purpose of this
example, we are going to quickly create virtual machine one via `virt-builder`_
tool.

First we build a vm image (uploading ssh authorized keys like this would make
the machine accessible for everyone who has keys on the machine you are running
this command):

.. code-block:: console

    $ virt-builder centos-7.2 -o mbukatov-qe-server.qcow2 --size 15G --format qcow2 --mkdir /root/.ssh  --chmod 0700:/root/.ssh  --upload /root/.ssh/authorized_keys:/root/.ssh/authorized_keys --selinux-relabel --update

Then we `import the new image into libvirt`_, creating new virtual machine (aka
guest) and  booting it for the first time:

.. code-block:: console

    # virt-install --import --name mbukatov-qe-server --ram 2048 --os-variant rhel7 --disk path=/var/lib/libvirt/images/mbukatov-qe-server.qcow2,format=qcow2 --network default --noautoconsole

When the new machine is ready, specify an ip address or fqdn of the new qe
server in the inventory file:

.. code-block:: console

    $ cat qe.hosts
    [qe_server]
    10.34.126.60

And make sure you have ssh configured properly (this includes ssh keys and
local ssh client configuration) so that ansible can work with the machine:

.. code-block:: console

	$ ansible -i qe.hosts -m ping all
	10.34.126.60 | SUCCESS => {
		"changed": false, 
		"ping": "pong"
	}

Then you can run the `qe_server` playbook:

.. code-block:: console

    $ ansible-playbook -i qe.hosts qe_server.yml

When the ansible playbook run finishes, you can login to the usmqe account
on the QE Server for the first time:

.. code-block:: console

    $ ssh root@10.34.126.6
    [root@qeserver ~]# su - usmqe
    [usmqe@qeserver ~]$ ls
    usmqe-setup  usmqe-tests

Note that ``rh-python35`` software collection is enabled by default in
``~/.bashrc`` file of usmqe user account and that all requirements (eg. pytest,
mrglog, ...) are already available:

.. code-block:: console

    [usmqe@qeserver ~]$ python --version
    Python 3.5.1
    [usmqe@qeserver ~]$ py.test --version
    This is pytest version 3.0.4, imported from /home/usmqe/.local/lib/python3.5/site-packages/pytest.py
    [usmqe@qeserver ~]$ which mrglog_demo.py
    ~/.local/bin/mrglog_demo.py

Also note that even though the default python for usmqe user is ``python3.5``
from the software collection, one can still run other system utilities which
are running on system default python2:

.. code-block:: console

    [usmqe@qeserver ~]$ ansible --version
    ansible 2.1.2.0
      config file = /etc/ansible/ansible.cfg
      configured module search path = Default w/o overrides

This is the case because all python tools packaged in Fedora/Red Hat/CentOS
uses explicit shebang:

.. code-block:: console

    [usmqe@qeserver ~]$ head -1 /usr/bin/ansible
    #!/usr/bin/python2


Related information
===================

At this point, we have a fresh QE server machine. But for us to be able to run
integration tests, we need to:

* Prepare fresh machines where Tendrl, Ceph and/or Gluster will be installed.
  See :ref:`test-enviroment-label`.
* Configure the tests, go into ``~/usmqe-tests`` directory and
  follow :ref:`config-before-testrun-label`

For full description and examples how to run integration tests, see
:ref:`test-execution-label`.


.. _`virt-builder`: http://libguestfs.org/virt-builder.1.html
.. _`import the new image into libvirt`: https://access.redhat.com/documentation/en-US/Red_Hat_Enterprise_Linux/7/html/Virtualization_Deployment_and_Administration_Guide/sect-Guest_virtual_machine_installation_overview-Creating_guests_with_virt_install.html
.. _`qe_server.yml`: https://github.com/Tendrl/usmqe-setup/blob/master/qe_server.yml
.. _`usmqe-setup repository`: https://github.com/Tendrl/usmqe-setup
