===================================
 Acceptance tests of rpm packaging
===================================

Tests here inspects and validates rpm packages locally on usmqe server.

Related Fedora Documentation:

* https://fedoraproject.org/wiki/Packaging:Guidelines
* https://fedoraproject.org/wiki/Common_Rpmlint_issues

Related USMQE configuration options
===================================

RPM tests have following structure of configuration::

  usmqe:
    rpm_repo:
      core:
        baseurl
        gpgkey_url
      deps:
        baseurl
        gpgkey_url

RPM tests have the following options in YAML configuration:

* ``usmqe -> rpm_repo -> core -> baseurl`` - base url of ``tendrl-core``
  rpm repository, mandatory
* ``usmqe -> rpm_repo -> core -> gpgkey_url`` - url of gpg key for
  ``tendrl-core`` repo, optional
* ``usmqe -> rpm_repo -> deps -> baseurl`` - base url of ``tendrl-deps``
  rpm repository, optional
* ``usmqe -> rpm_repo -> deps -> gpgkey_url`` - url of gpg key for 
  ``tendrl-deps`` repo, optional

So that you could specify all options to test rpm packages from official
upstream copr::

    usmqe -> rpm_repo -> core -> baseurl: https://copr-be.cloud.fedoraproject.org/results/tendrl/tendrl/epel-7-x86_64/
    usmqe -> rpm_repo -> core -> gpgkey_url: https://copr-be.cloud.fedoraproject.org/results/tendrl/tendrl/pubkey.gpg
    usmqe -> rpm_repo -> deps -> baseurl: https://copr-be.cloud.fedoraproject.org/results/tendrl/dependencies/epel-7-x86_64/
    usmqe -> rpm_repo -> deps -> gpgkey_url: https://copr-be.cloud.fedoraproject.org/results/tendrl/dependencies/pubkey.gpg

When ``gpgkey_url`` options are not specified, gpg keys are not validated.
Moreover one can also use local mirror via ``file://`` protocol for base url::

    usmqe -> rpm_repo -> core -> baseurl: file://mnt/tendrl/tendrl/epel-7-x86_64/
    usmqe -> rpm_repo -> deps -> baseurl: file://mnt/tendrl/dependencies/epel-7-x86_64/

When ``baseurl`` option for ``deps`` repo is not specified, test code expects
that all tendrl pacakges are available in single ``tendrl-core`` repo
(as it used to work before introduction of new repo scheme in upstream
tendrl copr, see https://github.com/usmqe/usmqe-tests/issues/68).
