"""
Import Cluster wizard module.
"""


# import pytest

from webstr.core import WebstrPage
import webstr.patternfly.modal.pages as modal

import usmqe.web.tendrl.mainpage.clusters.\
    create_cluster_wizard.general.models as m_general
# from usmqe.ceph import ceph_cluster
# from usmqe.gluster import gluster


class CreateCluster(modal.ModalWindow):
    """
    model for Create Cluster
    """
    _model = m_general.CreateClusterModel
    _label = 'clusters create page'
    _required_elems = ['ceph_line', 'gluster_line', 'cancel_btn', 'next_btn']

    def cancel(self):
        """
        click on cancel button
        """
        self._model.cancel_btn.click()

    def choose_ceph_creation(self):
        """
        choose ceph and click on next button
        """
        self._model.ceph_line.click()
        self._model.next_btn.click()

    def choose_gluster_creation(self):
        """
        choose gluster and click on next button
        """
        self._model.gluster_line.click()
        self._model.next_btn.click()


class StepButtons(WebstrPage):
    """
    model with common buttons for the whole create cluster workflow
    """
    _model = m_general.StepButtonsModel
    _label = 'cluster create initial page'
    _required_elems = ['cancel_btn', 'back_btn', 'next_btn']

    def cancel(self):
        """
        click on Cancel button
        """
        self._model.cancel_btn.click()

    def click_next(self):
        """
        click on Next button
        """
        self._model.next_btn.click()

    def click_back(self):
        """
        click on Back button
        """
        self._model.back_btn.click()
