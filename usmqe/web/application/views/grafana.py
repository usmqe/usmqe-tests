from widgetastic.widget import Text, View


class BaseGrafanaDashboard(View):
    dashboard_name = Text(".//a[@class='navbar-page-btn']")
    # It's either 'Cluster Name' or 'cluster Name'
    cluster_name = Text(".//label[contains(text(), 'luster Name')]"
                        "/parent::div/value-select-dropdown")


class GrafanaClusterDashboard(BaseGrafanaDashboard):
    cluster_health = Text(".//span[text() = 'Health']/ancestor::div[@class='panel-container']"
                          "/descendant::span[@class='singlestat-panel-value']")
    # hosts total looks like " - 5" instead of "5"
    hosts_total = Text(".//h1/a[contains(text(), 'Hosts')]/ancestor::div[@class='bottom_section']"
                       "/descendant::span[text() = 'Total']/following-sibling::span")
    # volumes total looks like " - 5" instead of "5"
    volumes_total = Text(".//h1/a[contains(text(), 'Volumes')]/ancestor::div[@class="
                         "'bottom_section']/descendant::span[text() = 'Total']"
                         "/following-sibling::span")

    @property
    def is_displayed(self):
        return (self.dashboard_name.text.find("Cluster") >= 0 and
                len(self.cluster_health.text) > 1 and
                len(self.hosts_total.text) > 1)


class GrafanaHostDashboard(BaseGrafanaDashboard):
    # in hostnames all dots are replaced with underscores
    host_name = Text(".//label[contains(text(), 'Host Name')]/parent::div/value-select-dropdown")
    host_health = Text(".//span[text() = 'Health']/ancestor::div[@class='panel-container']"
                       "/descendant::span[@class='singlestat-panel-value']")
    # brick total looks like " - 5" instead of "5"
    bricks_total = Text(".//span[text() = 'Total']/following-sibling::span")

    @property
    def is_displayed(self):
        return self.dashboard_name.text.find("Host") >= 0 and len(self.host_health.text) > 1


class GrafanaVolumeDashboard(BaseGrafanaDashboard):
    volume_name = Text(".//label[contains(text(), 'Volume Name')]"
                       "/parent::div/value-select-dropdown")
    volume_health = Text(".//span[text() = 'Health']/ancestor::div[@class='panel-container']"
                         "/descendant::span[@class='singlestat-panel-value']")
    # brick total looks like " - 5" instead of "5"
    bricks_total = Text(".//h1/a[contains(text(), 'Bricks')]/ancestor::div[@class='bottom_"
                        "section']/descendant::span[text() = 'Total']/following-sibling::span")

    @property
    def is_displayed(self):
        return (self.dashboard_name.text.find("Volume Dashboard") >= 0 and
                len(self.volume_health.text) > 1 and
                len(self.bricks_total.text) > 1)


class GrafanaBrickDashboard(BaseGrafanaDashboard):
    # in hostnames all dots are replaced with underscores
    host_name = Text(".//label[contains(text(), 'Host Name')]/parent::div/value-select-dropdown")
    path = Text(".//label[contains(text(), 'Brick Path')]/parent::div/value-select-dropdown")
    status = Text(".//span[text() = 'Status']/ancestor::div[@class='panel-container']"
                  "/descendant::span[@class='singlestat-panel-value']")

    @property
    def is_displayed(self):
        return self.dashboard_name.text.find("Brick Dashboard") >= 0 and len(self.status.text) > 1
