from widgetastic.widget import Text, TextInput
from usmqe.base.application.views.common import BaseLoggedInView
from taretto.ui.patternfly import Button, Dropdown, BreadCrumb


class ImportClusterView(BaseLoggedInView):
    page_breadcrumb = BreadCrumb()
    pagename = Text(".//h1")
    cluster_name = TextInput(name="clusterName")
    # volume_profiling = RadioGroup(".//div[./label[@for='role']]")
    # radio group for clusters has different structure. TODO: make it work

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
    pagename = Text(".//h1")
    close_button = Button("Close")
    view_progress = Button("View Task Progress")

    @property
    def is_displayed(self):
        return self.pagename.text == "Import Cluster Task Submitted"


class ImportProgressView(BaseLoggedInView):
    status = Text(".//form/div/label[text()[normalize-space(.)]='Status:']"
                  "/following-sibling::label")
