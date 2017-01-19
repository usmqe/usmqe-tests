# vim: set tabstop=2 shiftwidth=2 softtabstop=2 colorcolumn=120:
"""
Import Cluster wizard module.

Right now, the wizard contains the following pages/screens:

1. Configure Cluster
2. Select Hosts
3. Choose Networks
4. Provision Storage
5. Review Summary
"""


from selenium.webdriver.common.keys import Keys

from webstr.core import WebstrPage
import webstr.patternfly.contentviews.pages as contentviews

import usmqe.web.tendrl.mainpage.clusters.\
    import_cluster_wizard.models as m_wizard


class ImportCluster(WebstrPage):
    """
    Import Cluster page
    """
    _model = m_wizard.ImportClusterModel
    _label = 'clusters import page'
    _required_elems = [
        'label',
        'cluster',
        'refresh_btn',
        'import_btn',
        'cancel_btn'
    ]

    @property
    def hosts(self):
        """
        get hosts list
        """
        return HostsList(self.driver)

# TODO ... not ready yet, not sure what selector should be
    def choose_cluster(self, selector):
        """
        choose the cluster to be imported
        """
        pass

    def refresh_hosts(self):
        """
        click on refresh button
        """
        self._model.refresh_btn.click()

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

    def set_filter(self, filter_type=None, filter_input=None):
        """
        Set filter and press ENTER key

        Parameters:
            filter_type (str) - by which type of filter hosts are filtered by
            filter_input (str) - text to be filled in the filter text field
        """
        if filter_type is not None:
            self._model.filter_by.value = filter_type
        if filter_input is not None:
            self._model.filter_input.value = filter_input
        self._model.filter_input.send_keys(Keys.RETURN)

    @property
    def order_by(self):
        """ get by which hosts are ordered

        Returns:
            order by
        """
        return self._model.order_by.value

    @order_by.setter
    def order_by(self, value):
        """ set the order by field

        Parameters:
            value (str): cluster name
        """
        self._model.order_by.value = value

    def order_order(self):
        """
        switch order of hosts
        """
        self._model.order_btn.click()


class ImportClusterSummary(WebstrPage):
    """
    Import Cluster - Review Summary page
    """
    _model = m_wizard.ImportClusterSummaryModel
    _label = 'clusters import Summary page'
    _required_elems = ['view_task_btn']

    def view_import_task(self):
        """ click on View Task Progress button
        """
        self._model.view_task_btn.click()


class HostItem(contentviews.ListViewRow):
    """
    An item (row) in a Hosts list.
    """
    _model = m_wizard.HostItemModel
    _label = 'clusters import host'
    _required_elems = ['name']


class HostsList(contentviews.ListView):
    """
    List of nodes/hosts.
    """
    _model = m_wizard.HostsListModel
    _label = 'clusters import hosts list'
