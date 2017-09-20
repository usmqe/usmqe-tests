"""
Import Cluster wizard module.
"""


import webstr.patternfly.contentviews.pages as contentviews

import usmqe.web.tendrl.mainpage.clusters.\
    import_cluster_wizard.models as m_wizard
from usmqe.web.tendrl.auxiliary.pages import ListMenu
from usmqe.web.tendrl.mainpage.clusters.pages import ViewTaskPage, check_hosts
# from usmqe.ceph import ceph_cluster
from usmqe.gluster import gluster


class ImportCluster(ListMenu):
    """
    Import Cluster page
    """
    _model = m_wizard.ImportClusterModel
    _label = 'clusters import page'
    _required_elems = [
        'label',
        'import_btn',
        'cancel_btn'
    ]

    @property
    def hosts(self):
        """
        get hosts list
        """
        return HostsList(self.driver)

    def import_click(self):
        """
        click on import button
        """
        self._model.import_btn.click()

    def cancel(self):
        """
        click on cancel button
        """
        self._model.cancel_btn.click()

    def import_cluster(self, hosts=None):
        """
        import SELECTED cluster

        Parameters:
            hosts (list): list of dictionaries
                          {'hostname': <hostname>, 'release': <release>, ...
                          for check only

        Returns:
            hosts list
        """
        import time
        if hosts is None:
            # get gluster hosts
            host = next(iter(self.hosts)).name
            storage = gluster.GlusterCommon()
            hosts = [
                {'hostname': hostname, 'release': None, 'role': 'Peer'}
                for hostname in storage.get_hosts_from_trusted_pool(host)]

# ceph variant if needed, cluster name is required
#                # get ceph hosts
#                # TODO get the cluster name from somewhere
#                #       - configuration, cluster_id param or ...
#                cluster_name = cluster_name or 'test_name'
#                # NOTE there are no full hostnames available in ceph
#                monitors = []
#                for host in self.hosts:
#                    if host.role.lower() == 'monitor':
#                        monitors.append(host.name)
#                pytest.check(
#                    monitors != [],
#                    'There has to be a host with Monitor role '
#                    'in ceph cluster')
#                storage = ceph_cluster.CephCluster(cluster_name, monitors)
#                ceph_mons = storage.mon.stat()['mons'].keys()
#                ceph_osds = []
#                ceph_all_osds = storage.osd.tree()['nodes']
#                for ceph_osd in ceph_all_osds:
#                    if ceph_osd['type'] == 'host':
#                        ceph_osds.append(ceph_osd['name'])
#                ceph_mon_osd = set(ceph_mons).intersection(ceph_osds)
#                # remove intersection
#                ceph_mons = set(ceph_mons) - ceph_mon_osd
#                ceph_osds = set(ceph_osds) - ceph_mon_osd
#                # TODO make sure how the role should look like on UI
#                mon_osd_hosts = [
#                    {'hostname': hostname,
#                     'release': release,
#                     'role': ['Monitor', 'OSD Hosts']}
#                    for hostname in ceph_mon_osd]
#                mon_hosts = [
#                    {'hostname': hostname,
#                     'release': release,
#                     'role': 'Monitor'}
#                    for hostname in ceph_mons]
#                osds_hosts = [
#                    {'hostname': hostname,
#                     'release': release,
#                     'role': 'OSD Host'}
#                    for hostname in ceph_osds]
#                hosts = mon_hosts + osds_hosts + mon_osd_hosts

        # check hosts
        check_hosts(hosts, self.hosts)

        self.import_click()
        # the page is not loaded completely, better to wait a little
        time.sleep(1)
        final_import_page = ImportClusterSummary(self.driver)
        final_import_page.view_task()
        return hosts


class ImportClusterSummary(ViewTaskPage):
    """
    Import Cluster - Review Summary page
    """
    _model = m_wizard.ImportClusterSummaryModel
    _label = 'clusters import Summary page'


class HostsItem(contentviews.ListViewRow):
    """
    An item (row) in a Hosts list.
    """
    _model = m_wizard.HostsItemModel
    _label = 'clusters import host'
    _required_elems = ['name', 'release', 'role']

    @property
    def name(self):
        """
        returns host name
        """
        return self._model.name.text

    @property
    def release(self):
        """
        returns installed ceph/gluster release
        """
        return self._model.release.text

    @property
    def role(self):
        """
        returns host role
        """
        return self._model.role.text


class HostsList(contentviews.ListView):
    """
    List of nodes/hosts.
    """
    _model = m_wizard.HostsListModel
    _label = 'clusters import hosts list'
    _row_class = HostsItem
