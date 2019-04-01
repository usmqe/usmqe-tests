import attr
from navmazing import NavigateToAttribute
from wait_for import wait_for


from usmqe.web.application.entities import BaseCollection, BaseEntity
from usmqe.web.application.views.common import AlertsView
from usmqe.web.application.implementations.web_ui import TendrlNavigateStep, ViaWebUI


@attr.s
class Alert(BaseEntity):
    """
    Alert entity
    """
    alert_id = attr.ib()
    description = attr.ib()
    date = attr.ib()
    severity = attr.ib()


@attr.s
class AlertsCollection(BaseCollection):
    ENTITY = Alert

    def get_alerts(self):
        """
        Return the list of instantiated Alert objects.
        """
        view = ViaWebUI.navigate_to(self, "All")
        wait_for(lambda: view.is_displayed,
                 timeout=10,
                 delay=2,
                 message="AlertsView wasn't displayed in time\n" +
                 "Visible text: {}".format(view.browser.elements("*")[0].text))
        alert_list = []
        for alert_id in view.alerts.all_alert_ids:
            alert = self.instantiate(
                alert_id,
                view.alerts.alerts(alert_id).description.text,
                view.alerts.alerts(alert_id).date.text,
                view.alerts.alerts(alert_id).severity,
                )
            alert_list.append(alert)
        view.navbar.alerts.click()
        return alert_list


@ViaWebUI.register_destination_for(AlertsCollection, "All")
class AlertsAll(TendrlNavigateStep):
    VIEW = AlertsView
    prerequisite = NavigateToAttribute("application.web_ui", "LoggedIn")

    def step(self):
        self.parent.navbar.alerts.click()
