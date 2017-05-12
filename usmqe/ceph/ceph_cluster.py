"""
Library for direct access to ceph commands.

.. moduleauthor:: dahorak@redhat.com

Quick example of usage::

    from usmqe.common import ceph_cluster

    ceph_cl = ceph_cluster.CephCluster(CLUSTER_NAME)
    ceph_cl.status()
    ceph_cl.report()
    ...
    ceph_cl.mon.stat()
    ceph_cl.mon.dump()
    ...
    ceph_cl.osd.stat()
    ceph_cl.osd.df()
    ceph_cl.osd.dump()
    ...
    ceph_cl.rados.df()
    ceph_cl.rados.lspools()
    ...
"""


import json
import re

import pytest

from usmqe.ceph.commands import CephClusterCommand, RadosCommand,\
                                CephCommandErrorException
import usmqe.inventory


LOGGER = pytest.get_logger('ceph_cluster', module=True)


class CephCommon(object):
    """
    Class representing ceph cluster.
    """

    def __init__(self, cluster, mons=None):
        """
        Initialize CephCommon object.

        Args:
            cluster: cluster name or dict with ``name`` key or
                     :py:class:`CephCommon`/:py:class:`CephCluster` object
            mons: list of ceph cluster monitors
                  monitor machines hostnames or IP addresses
        """
        if isinstance(cluster, CephCommon):
            self._name = cluster.name
        elif isinstance(cluster, dict):
            self._name = cluster["name"]
        else:
            self._name = cluster

        self.cmd = CephClusterCommand(cluster=self._name)
        self._mons = mons

    @property
    def name(self):
        """
        Returns the name of the cluster.
        """
        return self._name

    def run_on_mon(self, command, mons=None, executor=None,
                   parse_output=json.loads):
        """
        Run command on ceph monitor
        """
        last_error = None
        output = None
        mons = mons or self._mons or usmqe.inventory.role2hosts("ceph_mon")
        if not executor:
            executor = self.cmd
        for mon in mons:
            try:
                output = executor.run(mon, command)
            except CephCommandErrorException as err:
                last_error = err
                continue
            break
        else:
            if last_error:
                raise CephCommandErrorException(
                    "Problem with ceph command '%s'.\n"
                    "Last command rcode: %s, stdout: %s, stderr: %s" %
                    (last_error.cmd, last_error.rcode,
                     last_error.stdout, last_error.stderr))
            else:
                raise CephCommandErrorException(
                    "Problem with ceph command '%s'.\n"
                    "Possible problem is no ceph-mon (ceph_mon list: %s)" %
                    (command, usmqe.inventory.role2hosts("ceph_mon")))

        if parse_output:
            output = parse_output(output)
        return output


class CephCluster(CephCommon):
    """
    Class representing ceph cluster.
    """

    def __init__(self, cluster, mons=None):
        """
        Initialize CephCluster object.

        Args:
            cluster: cluster name or dict with ``name`` key or
                     :py:class:`CephCommon`/:py:class:`CephCluster` object
            mons: list of ceph cluster monitors
                  monitor machines hostnames or IP addresses
        """
        super(CephCluster, self).__init__(cluster, mons)
        self._osd = None
        self._mon = None
        self._rados = None

    @property
    def osd(self):
        """
        Property osd returns initialized :py:class:`CephClusterOsd` object.
        """
        if not self._osd:
            self._osd = CephClusterOsd(self, self._mons)
        return self._osd

    @property
    def mon(self):
        """
        Property mon returns initialized :py:class:`CephClusterMon` object.
        """
        if not self._mon:
            self._mon = CephClusterMon(self, self._mons)
        return self._mon

    @property
    def rados(self):
        """
        Property rados returns initialized
        :py:class:`CephClusterStorage` object.
        """
        if not self._rados:
            self._rados = CephClusterStorage(self, self._mons)
        return self._rados

#  def foo(self):
#    """
#    Run ceph command: foo
#
#    Returns: dictionary parsed json from
#             `ceph --format json --cluster CLUSTERNAME foo` command.
#
#    Example output (only root elements):
#
#    """
#    return self.run_on_mon('foo')

    # pylint - allow short method name
    def df(self):  # pylint: disable=C0103
        """
        Run ceph command: ``df``

        Returns:
            dictionary: parsed json from
                        ``ceph --format json --cluster CLUSTERNAME df``
                        command

        Example output (only root elements)::

            { 'pools': [...],
              'stats': {...}, }
        """
        return self.run_on_mon('df')

    def fsid(self):
        """
        Run ceph command: ``fsid``

        Returns:
            dictionary: parsed json from
                        ``ceph --format json --cluster CLUSTERNAME fsid``
                        command

        Example output (only root elements)::

            {'fsid': 'aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee'}
        """
        # WORKAROUND for https://github.com/tomerfiliba/plumbum/issues/275
        # return self.run_on_mon('fsid')
        return self.run_on_mon('fsid && echo || (echo; false)')

    def health(self):
        """
        Run ceph command: ``health``

        Returns:
            dictionary: parsed json from
                        ``ceph --format json --cluster CLUSTERNAME health``
                        command

        Example output (only root elements)::

            { 'detail': [],
              'health': {...},
              'overall_status': 'HEALTH_...',
              'summary': [{...}, {...}],
              'timechecks': {...}, }
        """
        return self.run_on_mon('health')

    def mon_status(self):
        """
        Run ceph command: ``mon_status``

        Returns:
            dictionary: parsed json from
                        ``ceph --format json --cluster CLUSTERNAME mon_status``
                        command

        Example output (only root elements)::

            { 'election_epoch': 8,
              'extra_probe_peers': [...],
              'monmap': {...},
              'name': 'a',
              'outside_quorum': [],
              'quorum': [0, 1],
              'rank': 0,
              'state': 'leader',
              'sync_provider': [],}
        """
        return self.run_on_mon('mon_status')

    def quorum_status(self):
        """
        Run ceph command: ``quorum_status``

        Returns:
            dictionary: parsed json from
                ``ceph --format json --cluster CLUSTERNAME quorum_status``
                command

        Example output (only root elements)::

            { 'election_epoch': 8,
              'monmap': {...},
              'quorum': [0, 1],
              'quorum_leader_name': 'a',
              'quorum_names': ['a', 'b'],}
        """
        return self.run_on_mon('quorum_status')

    def report(self):
        """
        Run ceph command: ``report``

        Returns:
            dictionary: parsed json from
                        ``ceph --format json --cluster CLUSTERNAME report``
                        command

        Example output (only root elements)::

            { 'auth': {...},
              'cluster_fingerprint': 'aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee',
              'commit': 'abcdef0123456789abcdef0123456789abcdef01',
              'crushmap': {...},
              'health': {...},
              'mdsmap': {...},
              'mdsmap_first_committed': 1,
              'mdsmap_last_committed': 1,
              'monmap': {...},
              'monmap_first_committed': 1,
              'monmap_last_committed': 3,
              'osd_metadata': [...],
              'osdmap': {...},
              'osdmap_first_committed': 1,
              'osdmap_last_committed': 79,
              'paxos': {...},
              'pgmap': {...},
              'pgmap_first_committed': 1,
              'pgmap_last_committed': 107,
              'quorum': [0, 1, 2],
              'tag': '',
              'timestamp': '2016-04-12 15:49:13.060559',
              'version': '0.94.5-9.el7cp',}
        """
        # WORKAROUND for https://github.com/tomerfiliba/plumbum/issues/275
        # return self.run_on_mon('report')
        return self.run_on_mon('report && echo || (echo; false)')

    def status(self):
        """
        Run ceph command: ``status``

        Returns:
            dictionary: parsed json from
                        ``ceph --format json --cluster CLUSTERNAME status``
                        command

        Example output (only root elements)::

            { 'election_epoch': 6,
              'fsid': 'aaaaaaaa-bbbb-cccc-ddddddddddddddddd',
              'health': {...},
              'mdsmap': {...},
              'monmap': {...},
              'osdmap': {...},
              'pgmap': {...},
              'quorum': [0, 1, 2],
              'quorum_names': ['b', 'c', 'a'],}
        """
        return self.run_on_mon('status')


class CephClusterMon(CephCommon):
    """
    class representing ceph mon
    """

    re_ceph_mon_stat_outpt = re.compile(
        r'.* (?P<count>[0-9]*) mons at {(?P<mons>[^}]*)}, '
        r'election epoch (?P<epoch>[0-9]*), '
        r'quorum (?P<quorum_num>[0-9,]*) (?P<quorum>[a-z,]*)')

    def stat(self):
        """
        Run ceph command: ``mon stat``

        Returns:
            dictionary: parsed output from
                        ``ceph --format json --cluster CLUSTERNAME mon stat``
                        command

        Example output::

            { 'count': '3',
              'epoch': '12',
              'mons': {'a': '172.16.180.1:6789/0',
                       'b': '172.16.180.2:6789/0',
                       'c': '172.16.180.3:6789/0',},
              'quorum': ['a', 'b'],
              'quorum_num': ['0', '1'],}

        .. note::

            Please use :py:meth:`dump` method where possible,
            because this ``ceph mon stat`` command doesn't support json output.
        """
        def parse_mon_stat_output(cmd_output):
            """
            Parse ceph mon stat output.

            Returns status in dict.
            """
            cmd_output = cmd_output.strip()
            result = CephClusterMon.re_ceph_mon_stat_outpt.match(cmd_output)
            result = result.groupdict()

            output = {
                'mons': {},
                'count': result['count'],
                'epoch': result['epoch'],
                'quorum_num': result['quorum_num'].split(','),
                'quorum': result['quorum'].split(',')}
            for mon in result['mons'].split(','):
                name, addr = mon.split('=')
                output['mons'][name] = addr
            return output

        return self.run_on_mon('mon stat', parse_output=parse_mon_stat_output)

    def dump(self, epoch=None):
        """
        Run ceph command: ``mon dump``

        Returns:
            dictionary: parsed json from
                        ``ceph --format json --cluster CLUSTERNAME mon dump``
                        command

        Example output::

            { 'created': '2016-04-12 08:31:49.001225',
              'epoch': 3,
              'fsid': 'aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee',
              'modified': '2016-04-12 08:32:13.131977',
              'mons': [
                  {'addr': '172.16.180.1:6789/0', 'name': 'a', 'rank': 0},
                  {'addr': '172.16.180.2:6789/0', 'name': 'b', 'rank': 1},
                  {'addr': '172.16.180.3:6789/0', 'name': 'c', 'rank': 2},],
              'quorum': [0, 1]}
        """
        epoch_str = "{}".format(epoch) if epoch else ""
        return self.run_on_mon('mon dump {}'.format(epoch_str))


class CephClusterOsd(CephCommon):
    """
    class representing ceph osd
    """
    # pylint - allow short method name
    def df(self):  # pylint: disable=C0103
        """
        Run ceph command: ``osd df``

        Returns:
            dictionary: parsed json from
                        ``ceph --format json --cluster CLUSTERNAME osd df``
                        command

        Example output (only root elements)::

            { 'nodes': [
                { 'crush_weight': 0.0,
                  'depth': 1,
                  'id': 0,
                  'kb': 9425900,
                  'kb_avail': 9390420,
                  'kb_used': 35480,
                  'name': 'osd.0',
                  'reweight': 1.0,
                  'type': 'osd',
                  'type_id': 0,
                  'utilization': 0.37641,
                  'var': 2.25166,},
                {...}, ],
              'stray': [],
              'summary': {
                'average_utilization': 0.16717,
                'dev': 0.150601,
                'max_var': 2.25166,
                'min_var': 0.63861,
                'total_kb': 167659376,
                'total_kb_avail': 167379100,
                'total_kb_used': 280276,}}
        """
        return self.run_on_mon('osd df')

    def dump(self, epoch=None):
        """
        Run ceph command: ``osd dump``

        Returns:
            dictionary: parsed json from
                        ``ceph --format json --cluster CLUSTERNAME osd dump``
                        command

        Example output (only root elements)::

            { 'blacklist': [],
              'cluster_snapshot': '',
              'created': '2016-04-12 08:31:53.667534',
              'epoch': 81,
              'erasure_code_profiles': {...},
              'flags': '',
              'fsid': 'aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee',
              'max_osd': 8,
              'modified': '2016-04-13 11:04:14.682494',
              'osd_xinfo': [{...}, ...],
              'osds': [{...}, ...],
              'pg_temp': [],
              'pool_max': 2,
              'pools': [{...},...],
              'primary_temp': [],}
        """
        epoch_str = "{}".format(epoch) if epoch else ""
        return self.run_on_mon('osd dump {}'.format(epoch_str))

    def find(self, osd_id):
        """
        Run ceph command: ``osd find <osd_id>``

        Returns:
            dictionary: parsed json from
                ``ceph --format json --cluster CLUSTERNAME osd find <osd_id>``
                command

        Example output (only root elements)::

            { 'crush_location': {'host': 'general'},
              'ip': '172.16.180.1:6804/28484',
              'osd': 1,}
        """
        # WORKAROUND for https://github.com/tomerfiliba/plumbum/issues/275
        # return self.run_on_mon('osd find {}'.format(osd_id))
        return self.run_on_mon('osd find {} && echo || (echo; false)'.
                               format(osd_id))

    # pylint - allow short method name
    def ls(self, epoch=None):  # pylint: disable=C0103
        """
        Run ceph command: ``osd ls``

        Returns:
            list: parsed json from
                  ``ceph --format json --cluster CLUSTERNAME osd ls [epoch]``
                  command

        Example output::

            [0, 1, 2, 3]
        """
        epoch_str = "{}".format(epoch) if epoch else ""
        return self.run_on_mon('osd ls {}'.format(epoch_str))

    def lspools(self):
        """
        Run ceph command: ``osd lspools``

        Returns:
            list: parsed json from
                  ``ceph --format json --cluster CLUSTERNAME osd lspools``
                  command

        Example output (only root elements)::

          [
            {'poolname': 'foo', 'poolnum': 1},
            {'poolname': 'bar', 'poolnum': 2}
          ]
        """
        return self.run_on_mon('osd lspools')

    def metadata(self, osd_id):
        """
        Run ceph command: ``osd metadata <osd_id>``

        Returns:
            dictionary: parsed json from
                ``ceph --format json --cluster CLUSTERNAME osd
                  metadata <osd_id>``
                command

        Example output (only root elements)::

            { 'arch': 'x86_64',
              'back_addr': '172.16.180.5:6801/27461',
              'ceph_version': 'ceph version 0.94.5-9.el7cp '
                              '(deef183a81111fa5e128ec88c90a32c9587c615d)',
              'cpu': 'AMD Opteron 63xx class CPU',
              'filestore_backend': 'xfs',
              'filestore_f_type': '0x58465342',
              'front_addr': '172.16.180.56:6800/27461',
              'hb_back_addr': '172.16.180.56:6802/27461',
              'hb_front_addr': '172.16.180.56:6803/27461',
              'hostname': 'dahorak-usm2-node1.os1.phx2.redhat.com',
              'kernel_description': '#1 SMP Sat Jan 23 04:54:55 EST 2016',
              'kernel_version': '3.10.0-327.10.1.el7.x86_64',
              'mem_swap_kb': '2097148',
              'mem_total_kb': '3624372',
              'os': 'Linux',
              'osd_data': '/var/lib/ceph/osd/TestClusterA-0',
              'osd_journal': '/var/lib/ceph/osd/TestClusterA-0/journal',
              'osd_objectstore': 'filestore',}
        """
        # WORKAROUND for https://github.com/tomerfiliba/plumbum/issues/275
        # return self.run_on_mon('osd metadata {}'.format(osd_id))
        return self.run_on_mon(
            'osd metadata {} && echo || (echo; false)'.format(osd_id))

    def perf(self):
        """
        Run ceph command: ``osd perf``

        Returns:
            dictionary: parsed json from
                        ``ceph --format json --cluster CLUSTERNAME osd perf``
                        command

        Example output (only root elements)::

            { 'osd_perf_infos': [
                {'id': 0,
                 'perf_stats': {'apply_latency_ms': 103,
                                'commit_latency_ms': 11}},
                {...},...]}
        """
        return self.run_on_mon('osd perf')

    def stat(self):
        """
        Run ceph command: ``osd stat``

        Returns:
            dictionary: parsed output from
                        ``ceph --format json --cluster CLUSTERNAME osd stat``
                        command

        Example output::

            { 'epoch': 81,
              'full': False,
              'nearfull': False,
              'num_in_osds': 8,
              'num_osds': 8,
              'num_remapped_pgs': 0,
              'num_up_osds': 8}
        """
        # WORKAROUND for https://github.com/tomerfiliba/plumbum/issues/275
        # return self.run_on_mon('osd stat')
        return self.run_on_mon('osd stat && echo || (echo; false)')

    def tree(self):
        """
        Run ceph command: ``osd tree``

        Returns:
            dictionary: parsed json from
                        ``ceph --format json --cluster CLUSTERNAME osd tree``
                        command

        Example output (only root elements)::

            { 'nodes': [
                {'children': [7, 6, 5, 4, 3, 2, 1, 0],
                  'id': -6,
                  'name': 'general',
                  'type': 'host',
                  'type_id': 1},
                {'crush_weight': 0.0,
                  'depth': 1,
                  'exists': 1,
                  'id': 0,
                  'name': 'osd.0',
                  'primary_affinity': 1.0,
                  'reweight': 1.0,
                  'status': 'up',
                  'type': 'osd',
                  'type_id': 0},
                {...},...
                {'children': [-5, -4, -3, -2],
                  'id': -1,
                  'name': 'default',
                  'type': 'root',
                  'type_id': 10},
                {'children': [],
                  'id': -2,
                  'name': 'dahorak-usm2-node1',
                  'type': 'host',
                  'type_id': 1},
                {...},...],
              'stray': []}
        """
        return self.run_on_mon('osd tree')

    def pool_ls(self, detail=False):
        """
        Run ceph command: ``osd pool ls {detail}``

        Returns:
            dictionary: parsed json from
                        ``ceph --format json --cluster CLUSTERNAME osd pool ls {detail}``
                        command

        Example output (only root elements)::
        [
            "rbd"
        ]

        and with detail=True

        [
          {
             "pool_name": "rbd",
             "flags": 1,
             "flags_names": "hashpspool",
             "type": 1,
             "size": 3,
             "min_size": 2,
             "crush_ruleset": 0,
             "object_hash": 2,
             "pg_num": 64,
             "pg_placement_num": 64,
             "crash_replay_interval": 0,
             "last_change": "1",
             "last_force_op_resend": "0",
             "auid": 0,
             "snap_mode": "selfmanaged",
             "snap_seq": 0,
             "snap_epoch": 0,
             "pool_snaps": [],
             "removed_snaps": "[]",
             "quota_max_bytes": 0,
             "quota_max_objects": 0,
             "tiers": [],
             "tier_of": -1,
             "read_tier": -1,
             "write_tier": -1,
             "cache_mode": "none",
             "target_max_bytes": 0,
             "target_max_objects": 0,
             "cache_target_dirty_ratio_micro": 0,
             "cache_target_dirty_high_ratio_micro": 0,
             "cache_target_full_ratio_micro": 0,
             "cache_min_flush_age": 0,
             "cache_min_evict_age": 0,
             "erasure_code_profile": "",
             "hit_set_params": {
               "type": "none"
             },
             "hit_set_period": 0,
             "hit_set_count": 0,
             "use_gmt_hitset": true,
             "min_read_recency_for_promote": 0,
             "min_write_recency_for_promote": 0,
             "hit_set_grade_decay_rate": 0,
             "hit_set_search_last_n": 0,
             "grade_table": [],
             "stripe_width": 0,
             "expected_num_objects": 0,
             "fast_read": false,
             "options": {}
           }
         ]
        """
        if detail:
            return self.run_on_mon('osd pool ls detail')
        else:
            return self.run_on_mon('osd pool ls')


class CephClusterStorage(CephCommon):
    """
    class representing ceph object storage
    """

    def __init__(self, cluster):
        """
        Initialize CephCluster object.

        Args:
            cluster: cluster name
        """
        super(CephClusterStorage, self).__init__(cluster=cluster)
        self.cmd = RadosCommand(cluster=self._name)

    def lspools(self):
        """
        Run ceph command: ``lspools``

        Returns:
            list: parsed json from
                  ``ceph --format json --cluster CLUSTERNAME lspools`` command

        Example output::

            ['foo', 'bar']
        """
        return self.run_on_mon('lspools', parse_output=lambda x: x.split())

    # pylint - allow short method name
    def df(self, pool=None):  # pylint: disable=C0103
        """
        Run ceph command: ``df``

        Returns:
            dictionary: parsed json from
                        ``ceph --format json --cluster CLUSTERNAME df`` command

        Example output (only root elements)::

            { 'pools': [{...}, {...}],
              'total_avail': '167379100',
              'total_objects': '0',
              'total_space': '167659376',
              'total_used': '280276',}
        """
        pool_str = "--pool {}".format(pool) if pool else ""
        # WORKAROUND for https://github.com/tomerfiliba/plumbum/issues/275
        # return self.run_on_mon('df')
        return self.run_on_mon('df {} && echo || (echo; false)'.
                               format(pool_str))
