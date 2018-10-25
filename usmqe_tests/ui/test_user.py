from usmqe.base.application import Application
from usmqe.base.application.implementations.web_ui import ViaWebUI

def test_add_del_normal_user():
    app = Application(hostname="ebondare-usm1-server.usmqe.lab.eng.brq.redhat.com", scheme="http", username="admin", password="adminuser")
    #ViaWebUI.navigate_to(app.collections.users, "All")
    user = app.collections.users.adduser(user_id="auto_normal_user", name="Autotest User", email="test1@example.com", notifications_on=False, password="1234567890", role="normal")
