"""
FileShares page abstraction.
"""


from webstr.patternfly.contentviews import pages as contentviews
import webstr.patternfly.dropdown.pages as dropdown

import usmqe.web.tendrl.mainpage.file_shares.models as m_file_shares
from usmqe.web.tendrl.auxiliary.pages import ListMenu


class FileSharesMenu(ListMenu):
    """
    page object for file shares top menu
    """
    _model = m_file_shares.FileSharesMenuModel
    _label = 'file shares top menu'
    _required_elems = ListMenu._required_elems
    _required_elems.append('header')


class FileSharesItem(contentviews.ListViewRow):
    """
    An item (row) in a FileShares list.
    """
    _model = m_file_shares.FileSharesItemModel
    _label = 'file shares row'
    _required_elems = [
        '_root',
        'status_icon',
        'name_label',
        'volume_type',
        'num_bricks',
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
            FileSharesRowMenu instance
        """
        self._model.menu_link.click()
        return FileSharesRowMenu(self.driver)


class FileSharesList(contentviews.ListView):
    """
    Base page object for List of nodes.
    """
    _model = m_file_shares.FileSharesListModel
    _label = 'main page - file shares'
    _row_class = FileSharesItem


class FileSharesRowMenu(dropdown.DropDownMenu):
    """
    page object for file shares row menu
    """
    _model = m_file_shares.FileSharesRowMenuModel
    _label = 'file shares row menu'
    _required_elems = ['edit_link', 'rebalance_link', 'remove_link']

# TODO use menu
