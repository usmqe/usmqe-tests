"""
RBDs page abstraction.
"""


import copy

from webstr.patternfly.contentviews import pages as contentviews
import webstr.patternfly.dropdown.pages as dropdown

import usmqe.web.tendrl.mainpage.rbds.models as m_rbds
from usmqe.web.tendrl.auxiliary.pages import ListMenu


class RBDsMenu(ListMenu):
    """
    page object for rbds top menu
    """
    _model = m_rbds.RBDsMenuModel
    _label = 'rbds top menu'
    _required_elems = copy.deepcopy(ListMenu._required_elems)
    _required_elems.append('header')


class RBDsItem(contentviews.ListViewRow):
    """
    An item (row) in a RBDs list.
    """
    _model = m_rbds.RBDsItemModel
    _label = 'rbds row'
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
            RBDsRowMenu instance
        """
        self._model.menu_link.click()
        return RBDsRowMenu(self.driver)


class RBDsList(contentviews.ListView):
    """
    Base page object for List of nodes.
    """
    _model = m_rbds.RBDsListModel
    _label = 'main page - rbds'
    _row_class = RBDsItem


class RBDsRowMenu(dropdown.DropDownMenu):
    """
    page object for rbds row menu
    """
    _model = m_rbds.RBDsRowMenuModel
    _label = 'rbds row menu'
# TODO
# change required elems when the menu will be availalble
    _required_elems = ['edit_link', 'grow_link', 'remove_link']

# TODO use menu
