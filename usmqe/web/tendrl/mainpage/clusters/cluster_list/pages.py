"""
Clusters page abstraction.
"""


import copy
import pytest

from webstr.patternfly.contentviews import pages as contentviews
import webstr.patternfly.dropdown.pages as dropdown

from usmqe.gluster import gluster
from usmqe.ceph import ceph_cluster
import usmqe.web.tendrl.mainpage.clusters.cluster_list.models as m_cluster_list
from usmqe.web.tendrl.mainpage.clusters.import_cluster_wizard.pages\
    import ImportCluster, ImportClusterSummary
from usmqe.web.tendrl.auxiliary.pages import ListMenu


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

    def import_cluster(self, cluster_ident=None, name=None, hosts=None):
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
# TODO: Choose which cluster should be imported
# TODO: Change cluster name
        cluster_name = name
#       https://github.com/Tendrl/api/issues/70
        self.start_import_cluster()
        import time
        import_page = ImportCluster(self.driver)
        cluster_id = import_page.cluster_id
        if hosts is None:
            release = import_page.storage_service
            if 'Gluster' in release:
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
                mon_hosts = [
                    {'hostname': hostname,
                     'release': release,
                     'role': 'Monitor'}
                    for hostname in ceph_mons]
                ceph_osds = []
                ceph_all_osds = storage.osd.tree()['nodes']
                for ceph_osd in ceph_all_osds:
                    if ceph_osd['type'] == 'host':
                        ceph_osds.append(ceph_osd['name'])
                osds_hosts = [
                    {'hostname': hostname,
                     'release': release,
                     'role': 'OSD Host'}
                    for hostname in ceph_osds]
                hosts = mon_hosts + osds_hosts

        # check hosts
        check_hosts(hosts, import_page.hosts)

        import_page.import_click()
        # the page is not loaded completely, better to wait a little
        time.sleep(1)
        final_import_page = ImportClusterSummary(self.driver)
        final_import_page.view_import_task()
        return (cluster_name or cluster_id, hosts)

# TODO
# both ceph and gluster are imported the same way as of now
# use import_cluster method instead
    def import_gluster_cluster(self, name=None, hosts=None):
        """
        import gluster cluster

        Parameters:
            name (str): name of the cluster
                        TODO: Not used for now
                              https://github.com/Tendrl/api/issues/70
            hosts (list): list of dictionaries
                          {'hostname': <hostname>, 'release': <release>, ...
                          for check only
        """
        raise NotImplementedError('import_gluster_cluster does not exist yet')

# TODO
# both ceph and gluster are imported the same way as of now
# use import_cluster method instead
    def import_ceph_cluster(self, name=None, hosts=None):
        """
        import ceph cluster

        Parameters:
            name (str): name of the cluster
            hosts (list): list of dictionaries
                          {'hostname': <hostname>,
                           'role': <'Monitor' or 'OSD Host'>, ...
        """
        raise NotImplementedError('import_ceph_cluster does not exist yet')

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
                           'role': <'Monitor' or 'OSD Host'>, ...
        """
        raise NotImplementedError('create_ceph_cluster does not exist yet')


class ClustersMenu(ListMenu, ClustersWorkBase):
    """
    Clusters page top menu
    """
    _model = m_cluster_list.ClustersMenuModel
    _label = 'cluster page top menu'
    _required_elems = copy.deepcopy(ListMenu._required_elems)
    _required_elems.extend(['header', 'import_btn'])


class ClustersRow(contentviews.ListViewRow):
    """
    Cluster in Clusters list
    """
    _model = m_cluster_list.ClustersRowModel
    _required_elems = [
        'name_text',
        'hosts_label',
        'hosts_value',
        'alerts_label',
        'alerts_value',
        'menu_link']

    @property
    def name(self):
        """ returns cluster name """
        return self._model.name_text.text

# TODO
# Coming soon...
# waiting for the model, see models.py
#    @property
#    def status(self):
#        """ returns status on behalf of status_icon """
#        return self._model.status_icon.get_attribute('title')

    @property
    def hosts_nr(self):
        """
        returns number of hosts in the cluster as string
            text value of hosts_value field
        """
        return self._model.hosts_value.text

    @property
    def file_shares_nr(self):
        """
        returns number of file shares in the cluster as string
            text value of file_shares_value field
        """
        return self._model.file_shares_value.text

    @property
    def pools_nr(self):
        """
        returns number of pools in the cluster as string
            text value of pools_value field
        """
        return self._model.pools_value.text

    @property
    def alerts_nr(self):
        """
        returns number of alerts related to the cluster as string
            text value of alerts_value field
        """
        return self._model.alerts_value.text

    def click_on_alerts(self):
        """
        click on alerts number
        """
        self._model.alerts_value.click()

    def open_menu(self):
        """
        open a dropdown menu for the row

        Returns:
            ClustersRowMenu instance
        """
        self._model.menu_link.click()
        return ClustersRowMenu(self.driver)

    def open_details(self):
        """
        open cluster details
        click on cluster name
        """
        self._model.name.click()


# Coming soon...
class ClustersRowMenu(dropdown.DropDownMenu):
    """ menu availalble for a cluster/row """
    _model = m_cluster_list.ClustersRowMenuModel
    _required_elems = [
      'expand_link',
      'shrink_link'
    ]

# TODO use menu


class ClustersList(contentviews.ListView):
    """
    Base page object for Clusters list.

    Parameters:
      _location - initial URL to load upon instance creation
      _model - page model
    """
    _model = m_cluster_list.ClustersListModel
    _label = 'main page - clusters - list'
    _row_class = ClustersRow
