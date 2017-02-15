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
        """ get by which elem the list is ordered

        Returns:
            order by
        """
        return self._model.order_by.value

    @order_by.setter
    def order_by(self, value):
        """ set the order by field

        Parameters:
            value (str): order by text value
        """
        self._model.order_by.value = value

    def order_order(self):
        """
        switch order of the list
        """
        self._model.order_btn.click()
