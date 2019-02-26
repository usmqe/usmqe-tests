import attr
import time
from navmazing import NavigateToAttribute


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

    def get_all_alert_ids(self):
        """
        Return the list of alert ids of all alerts in UI.
        """
        view = self.application.web_ui.create_view(AlertsView)
        time.sleep(2)
        return view.alerts.all_alert_ids

    def get_alerts(self):
        """
        Return the list of instantiated Alert objects.
        """
        view = ViaWebUI.navigate_to(self, "All")
        alert_list = []
        for alert_id in self.get_all_alert_ids():
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
        time.sleep(1)
        self.parent.navbar.alerts.click()
