from widgetastic.exceptions import NoSuchElementException
# from widgetastic.exceptions import WidgetOperationFailed


from widgetastic.widget import (
    BaseInput,
    # Checkbox,
    # do_not_read_this_widget,
    # GenericLocatorWidget,
    ParametrizedLocator,
    # Select,
    # Table,
    # Text,
    # TextInput,
    Widget,
    ClickableMixin
)
from widgetastic.xpath import quote
from widgetastic_patternfly import (
    BootstrapSwitch as VanillaBootstrapSwitch,
    # FlashMessage,
    # FlashMessages,
    # VerticalNavigation,
)


class Kebab(Widget):
    """The so-called "kebab" widget of Patternfly.
    <http://www.patternfly.org/pattern-library/widgets/#kebabs>
    Args:
        button_id: id of the button tag inside the kebab. If not specified, first kebab available
            will be used
    """
    ROOT = ParametrizedLocator('{@locator}')
    UL = './ul[contains(@class, "dropdown-menu")]'
    BUTTON = './button'
    ITEM = './ul/li/a[normalize-space(.)={}]'
    ITEMS = './ul/li/a'

    def __init__(self, parent, button_id=None, logger=None):
        super(Kebab, self).__init__(parent, logger=logger)
        if button_id is not None:
            self.locator = (
                './/div[contains(@class, "dropdown-kebab-pf") and ./button[@id={}]]'.format(
                    quote(button_id)))
        else:
            self.locator = './/div[contains(@class, "dropdown-kebab-pf") and ./button][1]'

    @property
    def is_opened(self):
        """Returns opened state of the kebab."""
        return self.browser.is_displayed(self.UL)

    @property
    def items(self):
        """Lists all items in the kebab.
        Returns:
            :py:class:`list` of :py:class:`str`
        """
        return [self.browser.text(item) for item in self.browser.elements(self.ITEMS)]

    def open(self):
        """Open the kebab"""
        if not self.is_opened:
            self.browser.click(self.BUTTON)

    def close(self):
        """Close the kebab"""
        if self.is_opened:
            self.browser.click(self.BUTTON)

    def select(self, item, close=True, handle_alert=None):
        """Select a specific item from the kebab.
        Args:
            item: Item to be selected.
            close: Whether to close the kebab after selection. If the item is a link, you may want
                to set this to ``False``
        """
        try:
            self.open()
            self.browser.click(self.ITEM.format(quote(item)))
            if handle_alert is not None:
                self.browser.handle_alert(cancel=not handle_alert, wait=10.0)
        finally:
            if close:
                self.close()


class NavDropdown(Widget, ClickableMixin):
    """The dropdowns used eg. in navigation. Usually located in the top navbar."""

    def __init__(self, parent, locator, logger=None):
        Widget.__init__(self, parent, logger=logger)
        self.locator = locator

    def __locator__(self):
        return self.locator

    def read(self):
        return self.text

    @property
    def expanded(self):
        return 'open' in self.browser.classes(self)

    @property
    def collapsed(self):
        return not self.expanded

    def expand(self):
        if not self.expanded:
            self.click()
#            if not self.expanded:
#                raise Exception('Could not expand {}'.format(self.locator))
#            else:
#                self.logger.info('expanded')

    def collapse(self):
        if self.expanded:
            self.click()
            if self.expanded:
                raise Exception('Could not collapse {}'.format(self.locator))
            else:
                self.logger.info('collapsed')

    @property
    def text(self):
        try:
            return self.browser.text('./a/span', parent=self)
        except NoSuchElementException:
            return None

    @property
    def icon(self):
        try:
            el = self.browser.element('./a/i[contains(@class, "pficon")]')
            for class_ in self.browser.classes(el):
                if class_.startswith('pficon-'):
                    return class_[7:]
            else:
                return None
        except NoSuchElementException:
            return None

    @property
    def items(self):
        return [
            self.browser.text(element)
            for element
            in self.browser.elements('.//a[@role="menuitem"]')]

    def has_item(self, item):
        return item in self.items

    def item_enabled(self, item):
        if not self.has_item(item):
            raise ValueError('There is not such item {}'.format(item))
        element = self.browser.element('.//a[normalize-space(.)={}]'.format(quote(item)))
        return 'disabled' not in self.browser.classes(element)

    def select_item(self, item):
        if not self.item_enabled(item):
            raise ValueError('Cannot click disabled item {}'.format(item))

        self.expand()
        self.logger.info('selecting item {}'.format(item))
        self.browser.click('.//a[@role="menuitem" and normalize-space(.)={}]'.format(quote(item)))

    def __repr__(self):
        return '{}({!r})'.format(type(self).__name__, self.locator)


class BootstrapSwitch(VanillaBootstrapSwitch):

    def __init__(self, parent, ngmodel=None, logger=None):
        self.input = '//input[@ng-model={}]'.format(quote(ngmodel))
        self.label = ''
        BaseInput.__init__(self, parent, locator=self.ROOT, logger=logger)


class RadioGroup(Widget):
    """ Radio Group Control

    .. code-block:: python

        radio_group = RadioGroup(locator=".//div[./label[@for='role']]")
        radio_group.select(radio_group.button_values()[-1])
    """

    ROOT = ParametrizedLocator('{@locator}')
    BUTTONS = './/input[@type="radio"]'
    BUTTON = './/input[@type="radio" and @value={}]'

    def __init__(self, parent, locator, logger=None):
        Widget.__init__(self, parent=parent, logger=logger)
        self.locator = locator

    @property
    def button_values(self):
        return [btn.get_attribute("value") for btn in self.browser.elements(self.BUTTONS)]

    @property
    def selected(self):

        for btn in self.browser.elements(self.BUTTONS):
            if (
                "ng-valid-parse" in self.browser.classes(btn) or
                btn.get_attribute("checked") is not None
            ):
                return btn.get_attribute("value")

        else:
            # radio button doesn't have any marks to make out which button is selected by default.
            # so, returning first radio button's name
            return self.button_values[0]

    def select(self, value):
        if self.selected != value:
            self.browser.element(self.BUTTON.format(quote(value))).click()
            return True
        return False

    def read(self):
        return self.selected

    def fill(self, name):
        return self.select(name)


'''
class ListGroupItem(Widget, ClickableMixin):
    """
    Represents one item in the list-group widget.

    Args:
        index: Position of the item in the list-group.
    """

    def __init__(self, parent, index, logget=None):
        Widget.__init__(self, parent, loggetr=logger)
        self.index = index


    @property
    def listgroup(self):
        return self.parent


    def get_actions(self):
        pass
'''


class ListGroup(Widget, ClickableMixin):
    """
    Represents the patternfly list-group widget.
    """
    ROOT = '//div[@class="list-group list-view-pf list-view-pf-view ng-scope"]'
    ITEMS_LOC = './div[@class="list-group-item"]'
    ACTIONS_LOC = './/div[@class="list-view-pf-actions"]/*'
    DESCRIPTION_LOC = './/div[@class="list-view-pf-description"]/div/span'
    ADDITIONAL_INFO_LOC = './/div[@class="list-view-pf-additional-info-item"]'
    INFO_LABEL_LOC = './div[@class="bold-text"]'
    INFO_ITEM_LOC = './h5|./p'

    def get_items(self):
        items = {}
        list_items = self.browser.elements(self.ITEMS_LOC, parent=self)
        for item in list_items:
            actions = self.browser.elements(self.ACTIONS_LOC, parent=item)
            description = self.browser.text(self.DESCRIPTION_LOC, parent=item)
            additional_info = self.browser.elements(self.ADDITIONAL_INFO_LOC, parent=item)
            # unnamed_info_counter = 0
            # for info_item in additional_info:
            #    try
            items.update({description: (actions, additional_info)})
        return items
