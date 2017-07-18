"""
Create Cluster wizard module.
"""


from webstr.core import WebstrModel, By, PageElement, RootPageElement
from webstr.common.form import models as form
import webstr.patternfly.modal.models as modal

location = '/#/create-cluster'


class CreateClusterModel(modal.ModalWindowModel):
    """
    model for Create Cluster
    """
    # NOTE: part of patternfly - custom modal
    _root = RootPageElement(by=By.XPATH,
                            locator="//div[@class='custom-modal']")
    ceph_line = PageElement(By.XPATH, locator='//li[text()="Ceph"]')
    gluster_line = PageElement(By.XPATH, locator='//li[text()="Gluster"]')
    cancel_btn = form.Button(
        By.XPATH,
        '//button[contains(text(), "Cancel")]')
    next_btn = form.Button(
        By.XPATH,
        '//button[contains(text(), "Next")]')


class StepButtonsModel(WebstrModel):
    """
    model with common buttons for the whole create cluster workflow
    """
    cancel_btn = form.Button(
        By.XPATH,
        '//a[contains(@class, "btn-cancel")]')
    back_btn = form.Button(
        By.XPATH,
        '//button[contains(@class, "wizard-pf-back")]')
    next_btn = form.Button(
        By.XPATH,
        '//button[contains(@class, "wizard-pf-next")]')
