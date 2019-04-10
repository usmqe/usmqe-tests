import pytest
import time
import datetime

from usmqe.usmqeconfig import UsmConfig
from usmqe import usmssh, usmmail
from usmqe.api.tendrlapi import user as tendrlapi_user


LOGGER = pytest.get_logger('ui_user_testing', module=True)
CONF = UsmConfig()


@pytest.mark.author("ebondare@redhat.com")
@pytest.mark.parametrize("receive_alerts", [False, True])
@pytest.mark.happypath
@pytest.mark.ansible_playbook_setup('test_setup.smtp.yml')
@pytest.mark.ansible_playbook_setup('test_setup.snmp.yml')
@pytest.mark.ansible_playbook_teardown('test_teardown.smtp.yml')
@pytest.mark.ansible_playbook_teardown('test_teardown.snmp.yml')
def test_alerting_settings(application, receive_alerts, valid_normal_user_data):
    """
    Create normal user with email notifications switched on or off.
    Check that alerts appear in the mailbox according to notification settings.
    """
    """
    :step:
      Change admin's email to avoid collision.
    :result:
      Admin's email is changed
    """
    # create a user with the email address configured in ansible playbook
    new_data = {"email": "alerting_test" + str(receive_alerts) + "@example.com",
                "password": CONF.config["usmqe"]["password"],
                "confirm_password": CONF.config["usmqe"]["password"]}
    application.collections.users.edit_logged_in_user(new_data)
    """
    :step:
      Create normal user with notifications switched on or off
      and email configured in ansible playbook
    :result:
      Normal user is created
    """
    user = application.collections.users.create(
        user_id=valid_normal_user_data["username"],
        name=valid_normal_user_data["name"],
        email="root@" + CONF.inventory.get_groups_dict()["usm_client"][0],
        notifications_on=receive_alerts,
        password=valid_normal_user_data["password"],
        role=valid_normal_user_data["role"]
    )
    """
    :step:
      Stop glusterd on one of the cluster nodes.
    :result:
      After some time alerts are generated
    """

    start_time = datetime.datetime.now().timestamp()
    SSH = usmssh.get_ssh()
    host = CONF.config["usmqe"]["cluster_member"]
    stop_cmd = "systemctl stop glusterd"
    time.sleep(90)
    retcode, stdout, stderr = SSH[host].run(stop_cmd)
    if retcode != 0:
        raise OSError(stderr)
    """
    :step:
      Restart glusterd.
    :result:
      After some time alerts disappear
    """

    restart_cmd = "systemctl restart glusterd"
    time.sleep(90)
    retcode, stdout, stderr = SSH[host].run(restart_cmd)
    if retcode != 0:
        raise OSError(stderr)
    stop_time = datetime.datetime.now().timestamp()
    """
    :step:
      Gather e-mails that came after glusterd was stopped and check if there were any.
    :result:
      There should be some or no e-mails according to user settings.
    """

    messages = usmmail.get_msgs_by_time(start_timestamp=start_time,
                                        end_timestamp=stop_time)
    LOGGER.debug("Selected messages count: {}".format(len(messages)))
    alert_received = False
    for message in messages:
        LOGGER.debug("Message date: {}".format(message['Date']))
        LOGGER.debug("Message subject: {}".format(message['Subject']))
        LOGGER.debug("Message body: {}".format(message.get_payload(decode=True)))
        if message['Subject'].count("]"):
            alert_received = True
    if receive_alerts:
        pytest.check(alert_received,
                     "Check that alert has been received")
    else:
        pytest.check(not alert_received,
                     "Check that alert hasn't been recieved")
    user.delete()


@pytest.mark.author("ebondare@redhat.com")
@pytest.mark.parametrize("receive_alerts", [True, False])
@pytest.mark.happypath
@pytest.mark.testready
def test_mysettings_alerting_switch(application, receive_alerts, valid_session_credentials):
    """
    Test switching alerts on and off in My Settings.
    """
    """
    :step:
      Change alert settings in My Settings (and password as well due to BZ1654623)
    :result:
    """
    admin_data = {
        "email": "root@" + CONF.inventory.get_groups_dict()["usm_client"][0],
        "password": CONF.config["usmqe"]["password"],
        "confirm_password": CONF.config["usmqe"]["password"],
        "notifications_on": receive_alerts
        }
    application.collections.users.edit_logged_in_user(admin_data)
    """
    :step:
      Check that alert settings changed
    :result:
    """
    test = tendrlapi_user.ApiUser(auth=valid_session_credentials)
    admin_data = {
        "name": "Admin",
        "username": "admin",
        "email": "root@" + CONF.inventory.get_groups_dict()["usm_client"][0],
        "role": "admin",
        "email_notifications": receive_alerts
        }
    time.sleep(2)
    test.check_user(admin_data)


@pytest.mark.author("ebondare@redhat.com")
@pytest.mark.happypath
@pytest.mark.testready
def test_ui_alerts(application, managed_cluster):
    """
    Test UI alert appearance and disapearance.
    """
    """
    :step:
      Stop glusterd on one of the cluster nodes.
    :result:
      After some time alerts appear in UI
    """
    SSH = usmssh.get_ssh()
    host = CONF.config["usmqe"]["cluster_member"]
    stop_cmd = "systemctl stop glusterd"
    time.sleep(10)
    retcode, stdout, stderr = SSH[host].run(stop_cmd)
    if retcode != 0:
        raise OSError(stderr)
    time.sleep(40)
    alert_found = False
    alerts = application.collections.alerts.get_alerts()
    for alert in alerts:
        LOGGER.debug("Alert description: {}".format(alert.description))
        LOGGER.debug("Alert date: {}".format(alert.date))
        LOGGER.debug("Alert severity: {}".format(alert.severity))
        if alert.description.find("is Disconnected") > 0 and alert.description.find(host) > 0:
            alert_found = True
            LOGGER.debug("Alert found: {}".format(alert_found))
            pytest.check(alert.severity == "warning",
                         "Check that severity of alert about disconnection is ``warning``")
            pytest.check(int(alert.date.split(" ")[2]) > 2018,
                         "Check that the year in the alert date is integer, 2019 or greater")
    pytest.check(alert_found,
                 "Check that the alert about disconnection exists in the list of UI alerts")
    """
    :step:
      Restart glusterd.
    :result:
      After some time alerts disappear
    """
    restart_cmd = "systemctl restart glusterd"
    time.sleep(10)
    retcode, stdout, stderr = SSH[host].run(restart_cmd)
    time.sleep(50)
    if retcode != 0:
        raise OSError(stderr)
    alerts = application.collections.alerts.get_alerts()
    alert_found = False
    for alert in alerts:
        LOGGER.debug("Alert description: {}".format(alert.description))
        LOGGER.debug("Alert date: {}".format(alert.date))
        LOGGER.debug("Alert severity: {}".format(alert.severity))
        if alert.description.find("is Connected") > 0 and alert.description.find(host) > 0:
            alert_found = True
            LOGGER.debug("Alert found: {}".format(alert_found))
            pytest.check(alert.severity == "info",
                         "Check that severity of the alert about re-connection is ``info``")
            pytest.check(int(alert.date.split(" ")[2]) > 2018,
                         "Check that the year in the alert date is integer, 2019 or greater")
    pytest.check(alert_found,
                 "Check that the alert about re-connection exists in the list of UI alerts")
