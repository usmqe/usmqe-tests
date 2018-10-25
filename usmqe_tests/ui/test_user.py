from usmqe.base.application import Application
from usmqe.base.application.implementations.web_ui import ViaWebUI

def test_add_del_normal_user():
    app = Application(hostname="ebondare-usm1-server.usmqe.lab.eng.brq.redhat.com", scheme="http", username="admin", password="adminuser")
    normal_user = app.collections.users.adduser(user_id="normal_user_auto",
                                                name="Autotest Normal User",
                                                email="normal_user@tendrl.org",
                                                notifications_on=True,
                                                password="1234567890",
                                                role="normal")
    limited_user = app.collections.users.adduser(user_id="limited_user_auto",
                                                name="Autotest Read-Only User",
                                                email="limited_user@tendrl.org",
                                                notifications_on=True,
                                                password="1234567890",
                                                role="limited")
