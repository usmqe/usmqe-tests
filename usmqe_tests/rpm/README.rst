===================================
 Acceptance tests of rpm packaging
===================================

Tests here inspects and validates rpm packages locally on usmqe server.

Related Fedora Documentation:

* https://fedoraproject.org/wiki/Packaging:Guidelines
* https://fedoraproject.org/wiki/Common_Rpmlint_issues

Related USMQE configuration options
===================================

RPM tests have the following options:

* ``usm_core_baseurl`` - base url of ``tendrl-core`` rpm repository, mandatory
* ``usm_core_gpgkey_url`` - url of gpg key for ``tendrl-core`` repo, optional
* ``usm_deps_baseurl`` - base url of ``tendrl-deps`` rpm repository, optional
* ``usm_deps_gpgkey_url`` - url of gpg key for ``tendrl-deps`` repo, optional

So that you could specify all options to test rpm packages from official
upstream copr::

    usm_core_baseurl=https://copr-be.cloud.fedoraproject.org/results/tendrl/tendrl/epel-7-x86_64/
    usm_core_gpgkey_url=https://copr-be.cloud.fedoraproject.org/results/tendrl/tendrl/pubkey.gpg
    usm_deps_baseurl=https://copr-be.cloud.fedoraproject.org/results/tendrl/dependencies/epel-7-x86_64/
    usm_deps_gpgkey_url=https://copr-be.cloud.fedoraproject.org/results/tendrl/dependencies/pubkey.gpg

When ``usm_*gpgkey_url`` options are not specified, gpg keys are not validated.
Moreover one can also use local mirror via ``file://`` protocol for base url::

    usm_core_baseurl=file://mnt/tendrl/tendrl/epel-7-x86_64/
    usm_deps_baseurl=file://mnt/tendrl/dependencies/epel-7-x86_64/

When ``usm_deps_baseurl`` is not specified, test code expects that all tendrl
pacakges are available in single ``tendrl-core`` repo (as it used to work before
introduction of new repo scheme in upstream tendrl copr, see
https://github.com/usmqe/usmqe-tests/issues/68).
