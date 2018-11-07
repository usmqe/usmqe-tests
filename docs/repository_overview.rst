=================================
 Overview of USM QE repositories
=================================

This document contains a brief overview of structure and purpose of all USM QE
repositories.

usmqe-tests
===========

Upstream: https://github.com/usmqe/usmqe-tests

This repository is most important, because it contains python code of automated
integration test cases and sphinx based documentation which covers tests
and it's setup (you are reading it right now).

usmqe-setup
===========

Upstream: https://github.com/usmqe/usmqe-setup

This repository contains test setup automation implemented via Ansible.

usmqe-centos-ci
===============

Upstream: https://github.com/usmqe/usmqe-centos-ci

Machine deployment for Tendrl project and jenkins jobs in CentOS CI.

.. _`main.yaml`: https://github.com/usmqe/usmqe-tests/blob/master/conf/main.yaml
.. _`defaults.yaml`: https://github.com/usmqe/usmqe-tests/blob/master/conf/defaults.yaml
