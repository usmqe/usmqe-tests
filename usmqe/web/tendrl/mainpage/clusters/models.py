"""
Description: Simple cluster auxiliary model classes which are in common for
             several existing cluster classes

Author: ltrilety
"""


from webstr.core import WebstrModel, By
from webstr.common.form import models as form


class ViewTaskPageModel(WebstrModel):
    """
    model for page with View Task Progress button
    """
    view_task_btn = form.Button(
        By.XPATH,
        '//button[contains(@ng-click, "viewTaskProgress()")]')
