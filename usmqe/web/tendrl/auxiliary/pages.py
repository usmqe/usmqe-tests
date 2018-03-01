"""
Some usefull pages classes for common work with tendrl web
"""


from selenium.webdriver.common.keys import Keys

from webstr.core import WebstrPage

import usmqe.web.tendrl.auxiliary.models as m_auxiliary


class ListMenu(WebstrPage):
    """
    auxiliary class for work with a list menu (filter and order fields)
    """
    _model = m_auxiliary.ListMenuModel
    _label = 'list menu'
    _required_elems = [
        'filter_by',
        'filter_input',
        'order_by',
        'order_btn'
    ]

    # TODO make getter for filter_by and order_by values

    def set_filter_text(self, filter_type=None, filter_input=None):
        """
        Set filter and press ENTER key

        Parameters:
            filter_type (str) - by which type of filter hosts are filtered by
            filter_input (str) - text to be filled in the filter text field
        """
        if filter_type is not None:
            self._model.link_text = filter_type
            self._model.filter_by_value.click()
        if filter_input is not None:
            self._model.filter_input.value = filter_input
        self._model.filter_input.send_keys(Keys.RETURN)

    def set_filter_value(self, filter_type=None, filter_input=None):
        """
        Choose filter value from a list and set it

        Parameters:
            filter_type (str) - by which type of filter hosts are filtered by
            filter_input (str) - text to be filled in the filter text field
        """
        if filter_type is not None:
            self._model.link_text = filter_type
            self._model.filter_by_value.click()
        if filter_input is not None:
            self._model.link_text = filter_input
            self._model.filter_input_value.click()

    def __setattr__(self, name, value):
        """
        setter for order_by
        """
        if name == 'order_by':
            self._model.order_by.click()
            self._model.link_text = value
            self._model.order_by_value.click()
        else:
            super(ListMenu, self).__setattr__(name, value)

#    def set_order_by(self, value):
#        """ set the order by field
#
#        Parameters:
#            value (str): order by text value
#        """
#        self._model.order_by.click()
#        self._model.link_text = value
#        self._model.order_by_value.click()

    def sort_order(self):
        """
        switch order of the list
        """
        self._model.order_btn.click()

    # TODO clear just one filter

    def clear_all_filters(self):
        """
        Clear all filters, click on clear_all_filters link
        """
        self._model.clear_all_filters.click()


class UpperMenu(WebstrPage):
    """ Common page object for upper menu """
    _model = m_auxiliary.UpperMenuModel
    _label = 'upper menu'
    _required_elems = [
        # left part of upper navbar
        'user_link',
        # right part of upper navbar
    ]

    def open_user_menu(self):
        """
        Opens user drop-down menu
        """
        self._model.user_link.click()
        return UserMenu(self.driver)


class UserManagement(WebstrPage):
    """
    Base page object for user management pop-up menu

    Parameters:
      _model - page model
    """
    _model = m_auxiliary.UserManagementModel
    _label = 'user management popup menu'
    _required_elems = ['users']

    def users(self):
        """ Open Users page - click on users """
        self._model.users.click()


# TODO: Alert list is not finished
#       Most probably other classes will be inherited not just WebstrPage
#       but some List and Row classes
class AlertList(WebstrPage):
    """
    Page object for drop-down alert list
    """


class AlertRowModel(WebstrPage):
    """
    Page Object for any alert message
    """


class UserMenu(WebstrPage):
    """
    Base page object for user pop-up menu

    Parameters:
      _model - page model
    """
    _model = m_auxiliary.UserMenuModel
    _label = 'user popup menu'
    _required_elems = ['logout']

    def my_settings(self):
        """ open user settings - click on my_settings """
        self._model.my_settings.click()

    def logout(self):
        """ log out current user - click on logout """
        self._model.logout.click()
