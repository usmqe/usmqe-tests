"""
Central inventory module of usmqe tests.

Author: mbukatov@redhat.com, mkudlej@redhat.com
"""


# list of machines
__hosts2roles_dict = {}
__roles2hosts_dict = {}


def add_host_entry(role, hostname):
    """
    Update host configuration.
    """
    __hosts2roles_dict.setdefault(hostname, []).append(role)
    __roles2hosts_dict.setdefault(role, []).append(hostname)


def host2roles(hostname):
    """
    Return list of roles for given host (specified by fqdn).
    """
    return __hosts2roles_dict.get(hostname)


def role2hosts(rolename):
    """
    Return list of hosts for given role.
    """
    return __roles2hosts_dict.get(rolename)


def get_all_hosts():
    """
    Return list of hostsnames of all hosts.
    """
    return __hosts2roles_dict.keys()
