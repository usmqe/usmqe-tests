"""
Description: Simple cluster auxiliary methods and classes

Author: ltrilety
"""

import copy
import pytest

from usmqe.web.tendrl.mainpage.clusters.import_cluster_wizard.pages\
    import ImportCluster, ImportClusterSummary
from usmqe.ceph import ceph_cluster
from usmqe.gluster import gluster


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

    def import_cluster(self, import_page, name=None, hosts=None):
        """
        import SELECTED cluster

        Parameters:
            import_page: ImportCluster instance
            name (str): name of the cluster
                        TODO: Not used for now
                              https://github.com/Tendrl/api/issues/70
            hosts (list): list of dictionaries
                          {'hostname': <hostname>, 'release': <release>, ...
                          for check only

        Returns:
            tuple (cluster name or id, hosts list)
        """
# TODO: Change cluster name
        cluster_name = name
#       https://github.com/Tendrl/api/issues/70

        import time
        cluster_id = import_page.cluster_id
        if hosts is None:
            release = import_page.storage_service
            if 'gluster' in release.lower():
                # get gluster hosts
                host = next(iter(import_page.hosts)).name
                storage = gluster.GlusterCommon()
                hosts = [
                    {'hostname': hostname, 'release': release, 'role': 'Peer'}
                    for hostname in storage.get_hosts_from_trusted_pool(host)]
            else:
                # get ceph hosts
                # TODO get the cluster name from somewhere
                #       - configuration, cluster_id param or ...
                cluster_name = cluster_name or 'test_name'
                # NOTE there are no full hostnames available in ceph
                monitors = []
                for host in import_page.hosts:
                    if host.role.lower() == 'monitor':
                        monitors.append(host.name)
                pytest.check(
                    monitors != [],
                    'There has to be a host with Monitor role in ceph cluster')
                storage = ceph_cluster.CephCluster(cluster_name, monitors)
                ceph_mons = storage.mon.stat()['mons'].keys()
                ceph_osds = []
                ceph_all_osds = storage.osd.tree()['nodes']
                for ceph_osd in ceph_all_osds:
                    if ceph_osd['type'] == 'host':
                        ceph_osds.append(ceph_osd['name'])
                ceph_mon_osd = set(ceph_mons).intersection(ceph_osds)
                # remove intersection
                ceph_mons = set(ceph_mons) - ceph_mon_osd
                ceph_osds = set(ceph_osds) - ceph_mon_osd
                # TODO make sure how the role should look like on UI
                mon_osd_hosts = [
                    {'hostname': hostname,
                     'release': release,
                     'role': ['Monitor', 'OSD Hosts']}
                    for hostname in ceph_mon_osd]
                mon_hosts = [
                    {'hostname': hostname,
                     'release': release,
                     'role': 'Monitor'}
                    for hostname in ceph_mons]
                osds_hosts = [
                    {'hostname': hostname,
                     'release': release,
                     'role': 'OSD Host'}
                    for hostname in ceph_osds]
                hosts = mon_hosts + osds_hosts + mon_osd_hosts

        # check hosts
        check_hosts(hosts, import_page.hosts)

        import_page.import_click()
        # the page is not loaded completely, better to wait a little
        time.sleep(1)
        final_import_page = ImportClusterSummary(self.driver)
        final_import_page.view_import_task()
        return (cluster_name or cluster_id, hosts)

    def import_generic_cluster(self, cluster_ident=None, name=None,
                               hosts=None):
        """
        import cluster

        Parameters:
            cluster_ident: cluster identificator for choosing a cluster
                           which should be imported
            name (str): name of the cluster
                        TODO: Not used for now
                              https://github.com/Tendrl/api/issues/70
            hosts (list): list of dictionaries
                          {'hostname': <hostname>, 'release': <release>, ...
                          for check only

        Returns:
            tuple (cluster name or id, hosts list)
        """
        self.start_import_cluster()

# TODO: Choose which cluster should be imported
        import_page = ImportCluster(self.driver)

        return self.import_cluster(import_page, name=name, hosts=hosts)

    def import_gluster_cluster(self, cluster_ident=None, name=None,
                               hosts=None):
        """
        import gluster cluster

        Parameters:
            cluster_ident: cluster identificator for choosing a cluster
                           which should be imported
            name (str): name of the cluster
                        TODO: Not used for now
                              https://github.com/Tendrl/api/issues/70
            hosts (list): list of dictionaries
                          {'hostname': <hostname>, 'release': <release>, ...
                          for check only
        """
        self.start_import_cluster()
# TODO: Choose which cluster should be imported

        # Select first gluster cluster in the list of available clusters
        import_page = ImportCluster(self.driver)
        for cluster in import_page.avail_clusters:
            import_page.cluster = cluster
            release = import_page.storage_service.lower()
            if 'gluster' in release:
                break
        pytest.check('gluster' in release,
                     'There should be some gluster cluster available',
                     hard=True)

        return self.import_cluster(import_page, name=name, hosts=hosts)

    def import_ceph_cluster(self, cluster_ident=None, name=None,
                            hosts=None):
        """
        import ceph cluster

        Parameters:
            cluster_ident: cluster identificator for choosing a cluster
                           which should be imported
            name (str): name of the cluster
                        TODO: Not used for now
                              https://github.com/Tendrl/api/issues/70
            hosts (list): list of dictionaries
                          {'hostname': <hostname>, 'release': <release>, ...
                          for check only
        """
        self.start_import_cluster()
# TODO: Choose which cluster should be imported

        # Select first ceph cluster in the list of available clusters
        import_page = ImportCluster(self.driver)
        for cluster in import_page.avail_clusters:
            import_page.cluster = cluster
            release = import_page.storage_service.lower()
            if 'ceph' in release:
                break
        pytest.check('ceph' in release,
                     'There should be some ceph cluster available',
                     hard=True)

        return self.import_cluster(import_page, name=name, hosts=hosts)

# TODO
    def create_gluster_cluster(self, name=None, hosts=None):
        """
        create gluster cluster

        Parameters:
            name (str): name of the cluster
                        TODO: Not used for now
                              https://github.com/Tendrl/api/issues/70
            hosts (list): list of dictionaries
                          {'hostname': <hostname>, 'release': <release>, ...
                          for check only
        """
        raise NotImplementedError('create_gluster_cluster does not exist yet')

# TODO
    def create_ceph_cluster(self, name=None, hosts=None):
        """
        create ceph cluster

        Parameters:
            name (str): name of the cluster
                        TODO: Not used for now
                              https://github.com/Tendrl/api/issues/70
            hosts (list): list of dictionaries
                          {'hostname': <hostname>,
                           'role': <'Monitor' or/and 'OSD Host'>, ...
        """
        raise NotImplementedError('create_ceph_cluster does not exist yet')
