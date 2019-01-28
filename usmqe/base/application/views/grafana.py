from widgetastic.widget import Text, View


class GrafanaHostDashboard(View):
    dashboard_name = Text(".//a[@class='navbar-page-btn']")
    cluster_name = Text(".//label[contains(text(), 'Cluster Name')]"
                        "/parent::div/value-select-dropdown")
    # in hostnames all dots are replaced with underscores
    host_name = Text(".//label[contains(text(), 'Host Name')]/parent::div/value-select-dropdown")
    host_health = Text(".//span[text() = 'Health']/ancestor::div[@class='panel-container']"
                       "/descendant::span[@class='singlestat-panel-value']")
    # brick total looks like " - 5" instead of "5"
    bricks_total = Text(".//span[text() = 'Total']/following-sibling::span")

    @property
    def is_displayed(self):
        return self.dashboard_name.text.find("Host") >= 0
