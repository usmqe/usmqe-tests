from widgetastic.exceptions import (
    NoSuchElementException, WidgetOperationFailed)


from widgetastic.widget import (
    Checkbox,
    do_not_read_this_widget,
    GenericLocatorWidget,
    ParametrizedLocator,
    Select,
    Table,
    Text,
    TextInput,
    Widget,
    ClickableMixin
)
from widgetastic.xpath import quote
from widgetastic_patternfly import (
    FlashMessage,
    FlashMessages,
    VerticalNavigation,
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

    def select(self, item, close=True):
        """Select a specific item from the kebab.
        Args:
            item: Item to be selected.
            close: Whether to close the kebab after selection. If the item is a link, you may want
                to set this to ``False``
        """
        try:
            self.open()
            self.browser.click(self.ITEM.format(quote(item)))
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
            return self.browser.text('./a/p', parent=self)
        except NoSuchElementException:
            return None

    @property
    def icon(self):
        try:
            el = self.browser.element('./a/span[contains(@class, "pficon")]', parent=self)
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
            in self.browser.elements('./ul/li[not(contains(@class, "divider"))]', parent=self)]

    def has_item(self, item):
        return item in self.items

    def item_enabled(self, item):
        if not self.has_item(item):
            raise ValueError('There is not such item {}'.format(item))
        element = self.browser.element(
            './ul/li[normalize-space(.)={}]'.format(quote(item)), parent=self)
        return 'disabled' not in self.browser.classes(element)

    def select_item(self, item):
        if not self.item_enabled(item):
            raise ValueError('Cannot click disabled item {}'.format(item))

        self.expand()
        self.logger.info('selecting item {}'.format(item))
        self.browser.click('./ul/li[normalize-space(.)={}]'.format(quote(item)), parent=self)

    def __repr__(self):
        return '{}({!r})'.format(type(self).__name__, self.locator)


