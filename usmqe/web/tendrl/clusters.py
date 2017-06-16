"""
Description: Simple cluster auxiliary classes providing
             those methods and variables which are in common for
             several existing cluster classes on different pages

Author: ltrilety
"""

import copy
import pytest


IMPORT_TIMEOUT = 3600


def check_hosts(hosts_list, page_hosts_list):
    """
    check if all hosts in host_list are present on the page (in page_host_list)

    Parameters:
        hosts_list (list): list of dictionaries
                          {'hostname': <hostname>, 'role': <role>, ...
        page_hosts_list (list): list representing lines in the page hosts list
    """
    aux_list = copy.deepcopy(hosts_list)
    for host_row in page_hosts_list:
        found = False
        for host in aux_list:
            if host['hostname'] in host_row.name:
                found = True
                if type(host['role']) is list:
                    for role in host['role']:
                        pytest.check(
                            role in host_row.role,
                            "Host {} should have '{}' role it has '{}'".format(
                                host_row.name, role, host_row.role))
                else:
                    pytest.check(
                        host['role'] == host_row.role,
                        "Host {} should have '{}' role it has '{}'".format(
                            host_row.name, host['role'], host_row.role))
                aux_list.remove(host)
                break
        pytest.check(
            found,
            'A host {} should be part of the hosts list'.format(host_row.name))
    pytest.check(
        aux_list == [],
        'All cluster hosts should be listed on page '
        '(not listed: {})'.format([host['hostname'] for host in aux_list]))


class ClustersWorkBase(object):
    """
    auxiliary base class with methods for work with clusters - create/import
    """
    def start_import_cluster(self):
        """
        auxiliary method for clicking on proper import button
        """
        self._model.import_btn.click()

    def start_create_cluster(self):
        """
        auxiliary method for clicking on proper create button
        """
        self._model.create_btn.click()
