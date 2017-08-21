"""
Some usefull model classes for common work with grafana web
"""

from webstr.core import DynamicWebstrModel
from webstr.common.dialogs.models import OkCancelDlgModel
from webstr.common.form import models as form


class GenericStatPanelModel(WebstrModel):
    """
    Generic model for displaying some data

    NOTE:
        _title (string): title of the panel
                         it has to be properly set before use
                         e.g. "Volume Utilization"
    """
    _title = None
    _root = NameRootPageElement(
        By.XPATH,
        '//grafana-panel[.//span[contains(@class, "panel-title-text") and '
        'text()="%s"]]')
    header = PageElement(
        By.XPATH,
        './/span[contains(class, "panel-title-text")]')

    def __init__(self, driver):
        """
        Save the webdriver instance to attribute.

        Parameters:
            driver: webdriver instance
        """
        self._name = self._title
        super().__init__(driver)


class GenericChartModel(GenericStatPanelModel):
    """
    auxiliary model for chart
    """
    extended_menu = PageElement(By.XPATH, './/a[@gf-dropdown="extendedMenu"]')
    export_csv = PageElement(By.XPATH, './/a[@ng-click="ctrl.exportCsv()"]')


class ExportDialogModel(OkCancelDlgModel):
    """
    model for 'Export to CSV' dialog
    """
    ok_btn = form.Button(
        By.XPATH,
        '//export-data-modal//a[@ng-click="ctrl.export();"]')
    cancel_btn = form.Button(
        By.XPATH,
        '//export-data-modal//a[@ng-click="ctrl.dismiss();"]')
    mode = form.Select(By.XPATH, '//export-data-modal//select')
    time_format = form.TextInput(By.XPATH, '//export-data-modal//input')


class SingleStatModel(GenericStatPanelModel):
    """
    A model for a single stat panel
    """
    value = PageElement(By.XPATH, './/span[@class="singlestat-panel-value"]')
