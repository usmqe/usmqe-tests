"""
Import Cluster wizard module.
"""


import pytest

from webstr.core import WebstrPage
import webstr.patternfly.contentviews.pages as contentviews
import webstr.patternfly.modal.pages as modal

import usmqe.web.tendrl.mainpage.clusters.\
    create_cluster_wizard.general.models as m_general
import usmqe.web.tendrl.mainpage.clusters.\
    create_cluster_wizard.ceph.pages as ceph_create
import usmqe.web.tendrl.mainpage.clusters.\
    create_cluster_wizard.gluster.pages as gluster_create
from usmqe.web.tendrl.auxiliary.pages import ListMenu
from usmqe.ceph import ceph_cluster
from usmqe.gluster import gluster


class CreateCluster(modal.ModalWindowModel):
    """
    model for Create Cluster
    """
    _model = m_general.CreateClusterModel
    _label = 'clusters import page'
    _required_elems = ['ceph_line', 'gluster_line', 'cancel_btn', 'next_btn']

    def cancel(self):
        """
        click on cancel button
        """
        self._model.cancel_btn.click()

    def choose_ceph_creation(self, return_inst=True):
        """
        choose ceph and click on next button

        Parameters:
            return_inst (bool): returns nothing if False

        Returns:
            ceph StepGeneral instance
        """
        self._model.ceph_line.click()
        self._model.next_btn.click()
        return ceph_create.StepGeneral(self.driver)

    def choose_gluster_creation(self, return_inst=True):
        """
        choose gluster and click on next button

        Parameters:
            return_inst (bool): returns nothing if False

        Returns:
            gluster StepGeneral instance
        """
        self._model.gluster_line.click()
        self._model.next_btn.click()
        return gluster_create.StepGeneral(self.driver)
        


class StepButtons(WebstrModel):
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

    def next(self):
        """
        click on Next button
        """
        self._model.next_btn.click()

    def back(self):
        """
        click on Back button
        """
        self._model.back_btn.click()
