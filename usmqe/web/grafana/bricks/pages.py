"""
Grafana Bricks page abstraction
"""

from usmqe.web.grafana.auxiliary.pages import GenericChart, \
    GenericDropDownList
import usmqe.web.grafana.bricks.models as m_bricks

location = ':3000/dashboard/db/tendrl-gluster-bricks'


class ClusterList(GenericDropDownList):
    """
    DropDown list of clusters
    """
    _model = m_bricks.ClusterListModel
    _label = 'Cluster select list'

    def selected_cluster(self):
        """ returns selected cluster """
        return self.value

    def choose_cluster(self, cluster_id):
        """
        Select cluster

        Parameters:
            cluster_id (string): cluster id
        """
        self.value = cluster_id


class BrickList(GenericDropDownList):
    """
    DropDown list of bricks
    """
    _model = m_bricks.BrickListModel
    _label = 'Brick select list'

    def selected_brick(self):
        """ returns selected brick """
        return self.value

    def choose_brick(self, brick_name):
        """
        Select brick

        Parameters:
            brick_name (string): brick name
        """
        self.value = brick_name


class BricksUtilization(GenericChart):
    """
    page object for Bricks Utilization panel
    """
    _model = m_bricks.BricksUtilizationModel
    _label = 'Bricks Utilization panel'


class InodeUtilization(GenericChart):
    """
    page object for Inode Utilization panel
    """
    _model = m_bricks.InodeUtilizationModel
    _label = 'Inode Utilization panel'
