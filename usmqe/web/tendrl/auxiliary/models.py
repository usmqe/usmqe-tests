"""
Some usefull model classes for common work with tendrl web
"""

from webstr.core import WebstrModel
from webstr.common.form import models as form
from selenium.webdriver.common.by import By


class ListMenuModel(WebstrModel):
    """
    auxiliary model for list menu (filter and order fields)
    """
    filter_by = form.Select(
        By.XPATH,
        '//select[contains(@ng-model, "filterBy")]')
    filter_input = form.TextInput(By.ID, 'filter')
    order_by = form.TextInput(
        By.XPATH,
        '//select[contains(@ng-model, "orderBy")]')
    order_btn = form.Button(
        By.XPATH,
        '//button[contains(@ng-init, "Order")]')
