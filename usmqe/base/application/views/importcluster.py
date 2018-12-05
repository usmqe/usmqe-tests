from widgetastic.widget import Text, TextInput

from usmqe.base.application.views.common import BaseLoggedInView
# from usmqe.base.application.widgets import BootstrapSwitch, Kebab, RadioGroup

from taretto.ui.patternfly import Button, Dropdown, BreadCrumb


class ImportClusterView(BaseLoggedInView):
    page_breadcrumb = BreadCrumb()
    pagename = Text(".//h1")
    cluster_name = TextInput(name="clusterName")
    # volume_profiling = RadioGroup(".//div[./label[@for='role']]")
    # radio group for clusters has different structure. TODO: make it work

    # TODO: check that filter works
    filter_type = Dropdown("Name")
    user_filter = TextInput(placeholder='Filter by Name')

    # TODO: try this hosts_number = Text(".//h3").split(' ')[0]
    import_button = Button("Import")
    cancel_button = Button("Cancel")

    @property
    def is_displayed(self):
        return self.pagename == "Import Cluster"
