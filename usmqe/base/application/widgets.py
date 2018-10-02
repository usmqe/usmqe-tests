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

