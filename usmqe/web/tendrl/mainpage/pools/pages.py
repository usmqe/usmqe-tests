"""
Pools page abstraction.
"""


import copy

from webstr.patternfly.contentviews import pages as contentviews
import webstr.patternfly.dropdown.pages as dropdown

import usmqe.web.tendrl.mainpage.pools.models as m_pools
from usmqe.web.tendrl.auxiliary.pages import ListMenu


class PoolsMenu(ListMenu):
    """
    page object for pools top menu
    """
    _model = m_pools.PoolsMenuModel
    _label = 'pools top menu'
    _required_elems = copy.deepcopy(ListMenu._required_elems)
    _required_elems.append('header')


class PoolsItem(contentviews.ListViewRow):
    """
    An item (row) in a Pools list.
    """
    _model = m_pools.PoolsItemModel
    _label = 'pools row'
    _required_elems = [
        '_root',
        'status_icon',
        'name_label',
        'menu_link']

    @property
    def status(self):
        """
        find status

        Returns:
            status_icon element title
        """
        return self._model.status_icon.value

    def open_menu(self):
        """
        open row menu

        Returns:
            PoolsRowMenu instance
        """
        self._model.menu_link.click()
        return PoolsRowMenu(self.driver)


class PoolsList(contentviews.ListView):
    """
    Base page object for List of nodes.
    """
    _model = m_pools.PoolsListModel
    _label = 'main page - pools'
    _row_class = PoolsItem


class PoolsRowMenu(dropdown.DropDownMenu):
    """
    page object for pools row menu
    """
    _model = m_pools.PoolsRowMenuModel
    _label = 'pools row menu'
# TODO
# change required elems when the menu will be availalble
    _required_elems = ['edit_link', 'grow_link', 'remove_link']

# TODO use menu
