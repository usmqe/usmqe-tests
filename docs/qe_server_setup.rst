=========================
 Setup of QE Server role
=========================

QE Server is a machine where usmqe-tests (along with all it's dependencies) are
installed and where the integration tests are executed from.

Requirements
============

QE Server role requires a RHEL/CentOS 7 machine.

QE Server Playbook
==================

To unify and automate the deployment of qe server machines, usmqe team
maintains `qe_server.yml`_ playbook in the `usmqe-setup repository`_. You
should use this playbook so that the same qe enviroment is used across all
qe machines.


Quick Example of QE Server deployment
=====================================

You need a CentOS 7 machine for the qe server. We are going to quickly create 
one via `virt-builder`_ tool.

First we build a vm image (uploading ssh authorized keys like this would make
the machine accessible for everyone who has keys on the machine you are running
this command)::

    $ virt-builder centos-7.2 -o qe-server.qcow2 --size 15G --format qcow2 --mkdir /root/.ssh  --chmod 0700:/root/.ssh  --upload /root/.ssh/authorized_keys:/root/.ssh/authorized_keys --selinux-relabel --update

Then we import the new image into libvirt, booting the new virtual machine for
the first time::

    # virt-install --import --name mbukatov-qe-server --ram 2048 --os-variant rhel7 --disk path=/var/lib/libvirt/images/qe-server.qcow2,format=qcow2 --network default --noautoconsole

When the new machine is ready, specify an ip address or fqdn of the new qe
server in the inventory file::

    $ cat qe.hosts
    [qe_server]
    10.34.126.60

And make sure you have ssh configured properly (this includes ssh keys and
local ssh client configuration) so that ansible can work with the machine::

	$ ansible -i qe.hosts -m ping all
	10.34.126.60 | SUCCESS => {
		"changed": false, 
		"ping": "pong"
	}

Then you can run the `qe_server` playbook::

    $ ansible-playbook -i qe.hosts qe_server.yml

When the ansible playbook run finishes, you can login to the usmqe account
on the qe server for the first time::

    # su - usmqe
    $ ls
    usmqe-setup  usmqe-tests

To run integration tests, you would need to enable rh-python35 software
collection and you need to remember to that every time::

    $ scl enable rh-python35 bash   
    $ python --version
    Python 3.5.1
    $ py.test --version
    This is pytest version 3.0.4, imported from /home/usmqe/.local/lib/python3.5/site-packages/pytest.py
    $ which mrglog_demo.py 
    ~/.local/bin/mrglog_demo.py

TODO: we may enable the collection in the bashrc of the usmqe user in the
future (in the qe_server playbook), if we check that it doesn't break anything

The last step is to go into `~/usmqe-tests` directory and configure the pytest
there (see `conf` directory for examples). Then to run the integration tests,
one runs `py.test` there. TODO: link to other files (both topics deserves a
separate document with description and full example).


.. _`virt-builder`: http://libguestfs.org/virt-builder.1.html
.. _`qe_server.yml`: https://github.com/Tendrl/usmqe-setup/blob/master/qe_server.yml
.. _`usmqe-setup repository`: https://github.com/Tendrl/usmqe-setup
