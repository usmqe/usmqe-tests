from widgetastic.widget import Text, TextInput
from usmqe.web.application.views.common import BaseLoggedInView
from taretto.ui.patternfly import Button, Dropdown, BreadCrumb

from usmqe.web.application.widgets import RadioGroup


class ImportClusterView(BaseLoggedInView):
    """View for cluster import page """
    page_breadcrumb = BreadCrumb()
    pagename = Text(".//h1")
    cluster_name = TextInput(name="clusterName")
    profiling = RadioGroup(".//div[@class='col-sm-12 volume-profile']")

    # TODO: fix the filter. TextInput can't be defined by placeholder as of yet
    filter_type = Dropdown("Name")
    # user_filter = TextInput(placeholder='Filter by Name')

    # TODO: try this hosts_number = Text(".//h3").split(' ')[0]
    confirm_import = Button("Import")
    cancel_button = Button("Cancel")

    @property
    def is_displayed(self):
        return self.pagename.text == "Import Cluster"


class ImportTaskSubmittedView(BaseLoggedInView):
    """View for page that confirms Import task has beed submitted"""
    pagename = Text(".//h1")
    close_button = Button("Close")
    view_progress = Button("View Task Progress")

    @property
    def is_displayed(self):
        return self.pagename.text == "Import Cluster Task Submitted"
