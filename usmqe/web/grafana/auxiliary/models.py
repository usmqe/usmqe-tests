"""
Some usefull model classes for common work with grafana web
"""

from webstr.core import DynamicWebstrModel
from webstr.common.dialogs.models import OkCancelDlgModel
from webstr.common.form import models as form


class GenericChartModel(DynamicWebstrModel):
    """
    auxiliary model for chart

    NOTE: id is the header name e.g. "Volume Utilization"
    """
    header = PageElement(By.XPATH, '//span[text()="%s"]')
    extended_menu = PageElement(By.XPATH, '//a[@gf-dropdown="extendedMenu"]')
    export_csv = PageElement(By.XPATH, '//a[@ng-click="ctrl.exportCsv()"]')


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
